import pandas as pd
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from skl2onnx import to_onnx
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import r_regression

FOLDER_PATHS = ["../data/training_data/video-144821", "../data/training_data/video-145043", "../data/training_data/video-145233", "../data/training_data/video-145641", "../data/training_data/video-150001"]

with open("../data/config/sensor_whitelist.txt") as f:
    SENSOR_WHITELIST = f.read().splitlines()

def preprocess(folder_path):
    preprocessed_df = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv") and "ImageReading" not in file_name:
            file_path = os.path.join(folder_path, file_name)
            dataframe = pd.read_csv(file_path, sep=";")
            dataframe = dataframe.groupby(['sampleTimeStamp.seconds']).mean().reset_index()
            dataframe.reset_index(drop=True, inplace=True)
            dataframe = dataframe.filter(SENSOR_WHITELIST + ["sampleTimeStamp.seconds", "groundSteering"], axis=1)
            preprocessed_df.append(dataframe)
    result = preprocessed_df[0]
    for df in preprocessed_df[1:]:
        result = pd.merge(result, df, on=['sampleTimeStamp.seconds'], how="outer")

    return result

dfs = [preprocess(path) for path in FOLDER_PATHS]
merged_data = pd.concat(dfs, axis=0, ignore_index=True)
merged_data.fillna(merged_data.mean(), inplace=True)

X = merged_data
y = X["groundSteering"]
X = X.filter(SENSOR_WHITELIST, axis=1)
X = X.dropna(axis=1)
print("Columns used (sorted):")
print(sorted(X.columns))

param_grid = {
    'n_estimators': [100, 250, 500, 750],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

X = X.to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

clr = RandomForestRegressor(random_state=42)

grid_search = GridSearchCV(estimator=clr, param_grid=param_grid, cv=2, scoring='r2', verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)


# export model to disk
onx = to_onnx(grid_search, X)
with open("clr.onnx", "wb") as f:
    f.write(onx.SerializeToString())

best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)
print("Best Score (R^2):", best_score)

best_rf_model = grid_search.best_estimator_
y_pred = best_rf_model.predict(X_test)


accuracy = best_rf_model.score(X_test, y_test)
print("Accuracy:", accuracy)

in_bounds_counter = 0
for pred, actual in zip(y_pred, y_test):
    if actual == 0.0:
        continue

    lower_bound = min(actual * 0.75, actual * 1.25)
    upper_bound = max(actual * 0.75, actual * 1.25)

    if lower_bound < pred < upper_bound:
        in_bounds_counter += 1

print("====================")
print(f"{in_bounds_counter}/{len(y_test)} ({round(in_bounds_counter/len(y_test)*100, 2)}%) of predictions (!= 0) are within 25% of the actual value")
print("====================")


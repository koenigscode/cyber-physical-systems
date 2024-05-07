import pandas as pd
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor

FOLDER_PATHS = ["../training_data/video-144821", "../training_data/video-145043", "../training_data/video-145233"]

def preprocess(folder_path):
    preprocessed_df = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv") and "ImageReading" not in file_name:
            file_path = os.path.join(folder_path, file_name)
            dataframe = pd.read_csv(file_path, sep=";")
            dataframe.drop(dataframe.columns[len(dataframe.columns) -1], axis=1, inplace=True)
            dataframe = dataframe.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
            dataframe = dataframe.groupby(['sampleTimeStamp.seconds']).mean().reset_index()
            dataframe.reset_index(drop=True, inplace=True)
            preprocessed_df.append(dataframe)
    result = pd.concat(preprocessed_df, axis=0, ignore_index=True)
    return result

dfs = [preprocess(path) for path in FOLDER_PATHS]

merged_data = dfs[0]
for df in dfs[1:]:
    merged_data = pd.merge(merged_data, df, on=['sampleTimeStamp.seconds'], how="outer")
merged_data.fillna(merged_data.mean(), inplace=True)


X = merged_data.drop(columns=['sampleTimeStamp.seconds'])

print(X.head())
y = X["groundSteering"]
print("X shape:", X.shape)
print("y shape:", y.shape)


param_grid = {
    'n_estimators': [100, 250, 500, 750],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(random_state=42)

grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=5, scoring='r2', verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)
print("Best Score (R^2):", best_score)

best_rf_model = grid_search.best_estimator_
y_pred = best_rf_model.predict(X_test)

accuracy = best_rf_model.score(X_test, y_test)
print("Accuracy:", accuracy)
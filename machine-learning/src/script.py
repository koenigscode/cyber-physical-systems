import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor

def preprocess(path):
    dataframe = pd.read_csv(path, sep=";")
    dataframe.drop(dataframe.columns[len(dataframe.columns) -1], axis=1, inplace=True)
    dataframe = dataframe.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
    dataframe = dataframe.groupby(['sampleTimeStamp.seconds']).mean().reset_index()
    dataframe.reset_index(drop=True, inplace=True)
    return dataframe


geolocation_data_144821 = preprocess("../training_data/video-144821/opendlv.logic.sensation.Geolocation-0.csv")
geolocation_data_145233 = preprocess("../training_data/video-145233/opendlv.logic.sensation.Geolocation-0.csv")
geolocation_data_145043 = preprocess("../training_data/video-145043/opendlv.logic.sensation.Geolocation-0.csv")

geolocation_data = pd.concat([geolocation_data_145043, geolocation_data_144821, geolocation_data_145233], axis=0, ignore_index=True)


acceleration_data_144821 = preprocess("../training_data/video-144821/opendlv.proxy.AccelerationReading-0.csv")
acceleration_data_145233 = preprocess("../training_data/video-145233/opendlv.proxy.AccelerationReading-0.csv")
acceleration_data_145043 = preprocess("../training_data/video-145043/opendlv.proxy.AccelerationReading-0.csv")

acceleration_data = pd.concat([acceleration_data_144821, acceleration_data_145043, acceleration_data_145233], axis = 0, ignore_index=True)

angular_velocity_data_144821 = preprocess("../training_data/video-144821/opendlv.proxy.AngularVelocityReading-0.csv")
angular_velocity_data_145233 = preprocess("../training_data/video-145233/opendlv.proxy.AngularVelocityReading-0.csv")
angular_velocity_data_145043 = preprocess("../training_data/video-145043/opendlv.proxy.AngularVelocityReading-0.csv")
angular_velocity_data = pd.concat([angular_velocity_data_144821, angular_velocity_data_145043, angular_velocity_data_145233], axis=0, ignore_index=True)

distance_data1_144821 = preprocess("../training_data/video-144821/opendlv.proxy.DistanceReading-0.csv")
distance_data1_145233 = preprocess("../training_data/video-145233/opendlv.proxy.DistanceReading-0.csv")
distance_data1_145043 = preprocess("../training_data/video-145043/opendlv.proxy.DistanceReading-0.csv")

distance_data1 = pd.concat([distance_data1_144821, distance_data1_145043, distance_data1_145233], axis=0, ignore_index=True)


distance_data2_144821 = preprocess("../training_data/video-144821/opendlv.proxy.DistanceReading-2.csv")
distance_data2_145233 = preprocess("../training_data/video-145233/opendlv.proxy.DistanceReading-2.csv")
distance_data2_145043 = preprocess("../training_data/video-145043/opendlv.proxy.DistanceReading-2.csv")

distance_data2 = pd.concat([distance_data2_144821, distance_data2_145043, distance_data2_145233], axis=0, ignore_index=True)


steering_data_144821 = preprocess("../training_data/video-144821/opendlv.proxy.GroundSteeringRequest-0.csv")
steering_data_145043 = preprocess("../training_data/video-145043/opendlv.proxy.GroundSteeringRequest-0.csv")
steering_data_145233 = preprocess("../training_data/video-145233/opendlv.proxy.GroundSteeringRequest-0.csv")

steering_data = pd.concat([steering_data_144821, steering_data_145043, steering_data_145233], axis=0, ignore_index=True)

magnetic_field_data_144821 = preprocess("../training_data/video-144821/opendlv.proxy.MagneticFieldReading-0.csv")
magnetic_field_data_145233 = preprocess("../training_data/video-145233/opendlv.proxy.MagneticFieldReading-0.csv")
magnetic_field_data_145043 = preprocess("../training_data/video-145043/opendlv.proxy.MagneticFieldReading-0.csv")

magnetic_field_data = pd.concat([magnetic_field_data_144821, magnetic_field_data_145043, magnetic_field_data_145233], axis = 0, ignore_index=True)

pedal_pos_data_144821 = preprocess("../training_data/video-144821/opendlv.proxy.PedalPositionRequest-0.csv")
pedal_pos_data_145233 = preprocess("../training_data/video-145233/opendlv.proxy.PedalPositionRequest-0.csv")

pedal_pos_data_145043 = preprocess("../training_data/video-145043/opendlv.proxy.PedalPositionRequest-0.csv")

pedal_pos_data = pd.concat([pedal_pos_data_144821, pedal_pos_data_145043, pedal_pos_data_145233], axis=0, ignore_index=True)


merged_data = pd.merge(geolocation_data, acceleration_data, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, angular_velocity_data, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, distance_data1, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, distance_data2, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, magnetic_field_data, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, pedal_pos_data, on=['sampleTimeStamp.seconds'], how="outer")
merged_data.fillna(merged_data.mean(), inplace=True)


X = merged_data.drop(columns=['sampleTimeStamp.seconds'])

print(X.head())
y = steering_data["groundSteering"]
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
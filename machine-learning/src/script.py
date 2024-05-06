import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor


geolocation_data_144821 = pd.read_csv("../training_data/video-144821/opendlv.logic.sensation.Geolocation-0.csv", sep=";")
geolocation_data_144821.drop(geolocation_data_144821.columns[len(geolocation_data_144821.columns)-1], axis=1, inplace=True)
geolocation_data_144821['video-id'] = 144821

geolocation_data_145233 = pd.read_csv("../training_data/video-145233/opendlv.logic.sensation.Geolocation-0.csv", sep=";")
geolocation_data_145233.drop(geolocation_data_145233.columns[len(geolocation_data_145233.columns)-1], axis=1, inplace=True)
geolocation_data_145233['video-id'] = 145233

geolocation_data_145043 = pd.read_csv("../training_data/video-145043/opendlv.logic.sensation.Geolocation-0.csv", sep=";")
geolocation_data_145043.drop(geolocation_data_145043.columns[len(geolocation_data_145043.columns)-1], axis=1, inplace=True)
geolocation_data_145043['video-id'] = 145043

geolocation_data = pd.concat([geolocation_data_145043, geolocation_data_144821, geolocation_data_145233], axis=0, ignore_index=True)



acceleration_data_144821 = pd.read_csv("../training_data/video-144821/opendlv.proxy.AccelerationReading-0.csv", sep=";")
acceleration_data_144821.drop(acceleration_data_144821.columns[len(acceleration_data_144821.columns)-1], axis=1, inplace=True)
acceleration_data_144821['video-id'] = 144821

acceleration_data_145233 = pd.read_csv("../training_data/video-145233/opendlv.proxy.AccelerationReading-0.csv", sep=";")
acceleration_data_145233.drop(acceleration_data_145233.columns[len(acceleration_data_145233.columns)-1], axis=1, inplace=True)
acceleration_data_145233['video-id'] = 145233

acceleration_data_145043 = pd.read_csv("../training_data/video-145043/opendlv.proxy.AccelerationReading-0.csv", sep=";")
acceleration_data_145043.drop(acceleration_data_145043.columns[len(acceleration_data_145043.columns)-1], axis=1, inplace=True)
acceleration_data_145043['video-id'] = 145043

acceleration_data = pd.concat([acceleration_data_144821, acceleration_data_145043, acceleration_data_145233], axis = 0, ignore_index=True)

angular_velocity_data_144821 = pd.read_csv("../training_data/video-144821/opendlv.proxy.AngularVelocityReading-0.csv", sep=";")
angular_velocity_data_144821.drop(angular_velocity_data_144821.columns[len(angular_velocity_data_144821.columns)-1], axis=1, inplace=True)
angular_velocity_data_144821['video-id']=144821

angular_velocity_data_145233 = pd.read_csv("../training_data/video-145233/opendlv.proxy.AngularVelocityReading-0.csv", sep=";")
angular_velocity_data_145233.drop(angular_velocity_data_145233.columns[len(angular_velocity_data_145233.columns)-1], axis=1, inplace=True)
angular_velocity_data_145233['video-id']=145233

angular_velocity_data_145043 = pd.read_csv("../training_data/video-145043/opendlv.proxy.AngularVelocityReading-0.csv", sep=";")
angular_velocity_data_145043.drop(angular_velocity_data_145043.columns[len(angular_velocity_data_145043.columns)-1], axis=1, inplace=True)
angular_velocity_data_145043['video-id']=145043

angular_velocity_data = pd.concat([angular_velocity_data_144821, angular_velocity_data_145043, angular_velocity_data_145233], axis=0, ignore_index=True)

distance_data1_144821 = pd.read_csv("../training_data/video-144821/opendlv.proxy.DistanceReading-0.csv", sep=";")
distance_data1_144821.drop(distance_data1_144821.columns[len(distance_data1_144821.columns)-1], axis=1, inplace=True)
distance_data1_144821['video-id']=144821

distance_data1_145233 = pd.read_csv("../training_data/video-145233/opendlv.proxy.DistanceReading-0.csv", sep=";")
distance_data1_145233.drop(distance_data1_145233.columns[len(distance_data1_145233.columns)-1], axis=1, inplace=True)
distance_data1_145233['video-id']=145233

distance_data1_145043 = pd.read_csv("../training_data/video-145043/opendlv.proxy.DistanceReading-0.csv", sep=";")
distance_data1_145043.drop(distance_data1_145043.columns[len(distance_data1_145043.columns)-1], axis=1, inplace=True)
distance_data1_145043['video-id']=145043

distance_data1 = pd.concat([distance_data1_144821, distance_data1_145043, distance_data1_145233], axis=0, ignore_index=True)


distance_data2_144821 = pd.read_csv("../training_data/video-144821/opendlv.proxy.DistanceReading-2.csv", sep=";")
distance_data2_144821.drop(distance_data2_144821.columns[len(distance_data2_144821.columns)-1], axis=1, inplace=True)
distance_data2_144821['video-id']=144821

distance_data2_145233 = pd.read_csv("../training_data/video-145233/opendlv.proxy.DistanceReading-2.csv", sep=";")
distance_data2_145233.drop(distance_data2_145233.columns[len(distance_data2_145233.columns)-1], axis=1, inplace=True)
distance_data2_145233['video-id']=145233

distance_data2_145043 = pd.read_csv("../training_data/video-145043/opendlv.proxy.DistanceReading-2.csv", sep=";")
distance_data2_145043.drop(distance_data2_145043.columns[len(distance_data2_145043.columns)-1], axis=1, inplace=True)
distance_data2_145043['video-id']=145043

distance_data2 = pd.concat([distance_data2_144821, distance_data2_145043, distance_data2_145233], axis=0, ignore_index=True)

# Read the data for video-144821
steering_data_144821 = pd.read_csv("../training_data/video-144821/opendlv.proxy.GroundSteeringRequest-0.csv", sep=";")
steering_data_144821.drop(steering_data_144821.columns[len(steering_data_144821.columns)-1], axis=1, inplace=True)
steering_data_144821['video-id'] = 144821

# Read the data for video-145043
steering_data_145043 = pd.read_csv("../training_data/video-145043/opendlv.proxy.GroundSteeringRequest-0.csv", sep=";")
steering_data_145043.drop(steering_data_145043.columns[len(steering_data_145043.columns)-1], axis=1, inplace=True)
steering_data_145043['video-id'] = 145043

steering_data_145233 = pd.read_csv("../training_data/video-145233/opendlv.proxy.GroundSteeringRequest-0.csv", sep=";")
steering_data_145233.drop(steering_data_145233.columns[len(steering_data_145233.columns)-1], axis=1, inplace=True)
steering_data_145233['video-id'] = 145233

# Concatenate the DataFrames
steering_data = pd.concat([steering_data_144821, steering_data_145043, steering_data_145233], axis=0, ignore_index=True)

# Group by sampleTimeStamp.seconds and add video-id column
steering_data = steering_data.groupby(['sampleTimeStamp.seconds', 'video-id']).mean().reset_index()

# Reset index
steering_data.reset_index(drop=True, inplace=True)



magnetic_field_data_144821 = pd.read_csv("../training_data/video-144821/opendlv.proxy.MagneticFieldReading-0.csv", sep=";")
magnetic_field_data_144821.drop(magnetic_field_data_144821.columns[len(magnetic_field_data_144821.columns)-1], axis=1, inplace=True)
magnetic_field_data_144821['video-id']=144821


magnetic_field_data_145233 = pd.read_csv("../training_data/video-145233/opendlv.proxy.MagneticFieldReading-0.csv", sep=";")
magnetic_field_data_145233.drop(magnetic_field_data_145233.columns[len(magnetic_field_data_145233.columns)-1], axis=1, inplace=True)
magnetic_field_data_145233['video-id']=145233

magnetic_field_data_145043 = pd.read_csv("../training_data/video-145043/opendlv.proxy.MagneticFieldReading-0.csv", sep=";")
magnetic_field_data_145043.drop(magnetic_field_data_145043.columns[len(magnetic_field_data_145043.columns)-1], axis=1, inplace=True)
magnetic_field_data_145043['video-id']=145043

magnetic_field_data = pd.concat([magnetic_field_data_144821, magnetic_field_data_145043, magnetic_field_data_145233], axis = 0, ignore_index=True)

pedal_pos_data_144821 = pd.read_csv("../training_data/video-144821/opendlv.proxy.PedalPositionRequest-0.csv", sep=";")
pedal_pos_data_144821.drop(pedal_pos_data_144821.columns[len(pedal_pos_data_144821.columns)-1], axis=1, inplace=True)
pedal_pos_data_144821['video-id'] = 144821

pedal_pos_data_145233 = pd.read_csv("../training_data/video-145233/opendlv.proxy.PedalPositionRequest-0.csv", sep=";")
pedal_pos_data_145233.drop(pedal_pos_data_145233.columns[len(pedal_pos_data_145233.columns)-1], axis=1, inplace=True)
pedal_pos_data_145233['video-id'] = 145233

pedal_pos_data_145043 = pd.read_csv("../training_data/video-145043/opendlv.proxy.PedalPositionRequest-0.csv", sep=";")
pedal_pos_data_145043.drop(pedal_pos_data_145043.columns[len(pedal_pos_data_145043.columns)-1], axis=1, inplace=True)
pedal_pos_data_145043['video-id'] = 145043

pedal_pos_data = pd.concat([pedal_pos_data_144821, pedal_pos_data_145043, pedal_pos_data_145233], axis=0, ignore_index=True)

geolocation_data = geolocation_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds'])
geolocation_data = geolocation_data.groupby(['sampleTimeStamp.seconds', 'video-id']).mean().reset_index()
geolocation_data.reset_index(drop=True, inplace=True)



acceleration_data = acceleration_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
acceleration_data = acceleration_data.groupby(['sampleTimeStamp.seconds', 'video-id']).mean().reset_index()
acceleration_data.reset_index(drop=True, inplace=True)

angular_velocity_data = angular_velocity_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
angular_velocity_data= angular_velocity_data.groupby(['sampleTimeStamp.seconds', 'video-id']).mean().reset_index()
angular_velocity_data.reset_index(drop=True, inplace=True)

distance_data1 = distance_data1.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
distance_data1 = distance_data1.groupby(['sampleTimeStamp.seconds', 'video-id']).mean().reset_index()
distance_data1.reset_index(drop=True, inplace=True)

distance_data2 = distance_data2.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
distance_data2 = distance_data2.groupby(['sampleTimeStamp.seconds', 'video-id']).mean().reset_index()
distance_data2.reset_index(drop=True, inplace=True)



magnetic_field_data = magnetic_field_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
magnetic_field_data = magnetic_field_data.groupby(['sampleTimeStamp.seconds', 'video-id']).mean().reset_index()
magnetic_field_data.reset_index(drop=True, inplace=True)

pedal_pos_data = pedal_pos_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
pedal_pos_data = pedal_pos_data.groupby(['sampleTimeStamp.seconds', 'video-id']).mean().reset_index()
pedal_pos_data.reset_index(drop=True, inplace=True)







merged_data = pd.merge(geolocation_data, acceleration_data, on=['sampleTimeStamp.seconds', 'video-id'], how="outer")
merged_data = pd.merge(merged_data, angular_velocity_data, on=['sampleTimeStamp.seconds', 'video-id'], how="outer")
merged_data = pd.merge(merged_data, distance_data1, on=['sampleTimeStamp.seconds', 'video-id'], how="outer")
merged_data = pd.merge(merged_data, distance_data2, on=['sampleTimeStamp.seconds', 'video-id'], how="outer")
merged_data = pd.merge(merged_data, magnetic_field_data, on=['sampleTimeStamp.seconds', 'video-id'], how="outer")
merged_data = pd.merge(merged_data, pedal_pos_data, on=['sampleTimeStamp.seconds', 'video-id'], how="outer")
merged_data.fillna(merged_data.mean(), inplace=True)









X = merged_data.drop(columns=['sampleTimeStamp.seconds', 'sampleTimeStamp.microseconds'])

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
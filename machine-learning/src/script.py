import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


geolocation_data = pd.read_csv("../training_data/opendlv.logic.sensation.Geolocation-0.csv", sep=";")
geolocation_data.drop(geolocation_data.columns[len(geolocation_data.columns)-1], axis=1, inplace=True)

acceleration_data = pd.read_csv("../training_data/opendlv.proxy.AccelerationReading-0.csv", sep=";")
acceleration_data.drop(acceleration_data.columns[len(acceleration_data.columns)-1], axis=1, inplace=True)

angular_velocity_data = pd.read_csv("../training_data/opendlv.proxy.AngularVelocityReading-0.csv", sep=";")
angular_velocity_data.drop(angular_velocity_data.columns[len(angular_velocity_data.columns)-1], axis=1, inplace=True)

distance_data1 = pd.read_csv("../training_data/opendlv.proxy.DistanceReading-0.csv", sep=";")
distance_data1.drop(distance_data1.columns[len(distance_data1.columns)-1], axis=1, inplace=True)

distance_data2 = pd.read_csv("../training_data/opendlv.proxy.DistanceReading-2.csv", sep=";")
distance_data2.drop(distance_data2.columns[len(distance_data2.columns)-1], axis=1, inplace=True)

steering_data = pd.read_csv("../training_data/opendlv.proxy.GroundSteeringRequest-0.csv", sep=";")
steering_data.drop(steering_data.columns[len(steering_data.columns)-1], axis=1, inplace=True)
steering_data = steering_data.groupby('sampleTimeStamp.seconds').mean().reset_index()
steering_data.reset_index(drop=True, inplace=True)


magnetic_field_data = pd.read_csv("../training_data/opendlv.proxy.MagneticFieldReading-0.csv", sep=";")
magnetic_field_data.drop(magnetic_field_data.columns[len(magnetic_field_data.columns)-1], axis=1, inplace=True)

pedal_pos_data = pd.read_csv("../training_data/opendlv.proxy.PedalPositionRequest-0.csv", sep=";")
pedal_pos_data.drop(pedal_pos_data.columns[len(pedal_pos_data.columns)-1], axis=1, inplace=True)

geolocation_data = geolocation_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds'])
geolocation_data= geolocation_data.groupby('sampleTimeStamp.seconds').mean().reset_index()
geolocation_data.reset_index(drop=True, inplace=True)



acceleration_data = acceleration_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
acceleration_data = acceleration_data.groupby('sampleTimeStamp.seconds').mean().reset_index()
acceleration_data.reset_index(drop=True, inplace=True)

angular_velocity_data = angular_velocity_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
angular_velocity_data= angular_velocity_data.groupby('sampleTimeStamp.seconds').mean().reset_index()
angular_velocity_data.reset_index(drop=True, inplace=True)

distance_data1 = distance_data1.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
distance_data1 = distance_data1.groupby('sampleTimeStamp.seconds').mean().reset_index()
distance_data1.reset_index(drop=True, inplace=True)

distance_data2 = distance_data2.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
distance_data2 = distance_data2.groupby('sampleTimeStamp.seconds').mean().reset_index()
distance_data2.reset_index(drop=True, inplace=True)



magnetic_field_data = magnetic_field_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
magnetic_field_data = magnetic_field_data.groupby('sampleTimeStamp.seconds').mean().reset_index()
magnetic_field_data.reset_index(drop=True, inplace=True)

pedal_pos_data = pedal_pos_data.drop(columns=['received.seconds', 'received.microseconds', 'sent.seconds', 'sent.microseconds', 'sampleTimeStamp.microseconds'])
pedal_pos_data = pedal_pos_data.groupby('sampleTimeStamp.seconds').mean().reset_index()
pedal_pos_data.reset_index(drop=True, inplace=True)







merged_data = pd.merge(geolocation_data, acceleration_data, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, angular_velocity_data, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, distance_data1, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, distance_data2, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, magnetic_field_data, on=['sampleTimeStamp.seconds'], how="outer")
merged_data = pd.merge(merged_data, pedal_pos_data, on=['sampleTimeStamp.seconds'], how="outer")
merged_data.fillna(merged_data.mean(), inplace=True)









X = merged_data.drop(columns=['sampleTimeStamp.seconds', 'sampleTimeStamp.microseconds'])

print(X.head())
y = steering_data["groundSteering"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
print("Predictions of the steering wheel angle: ", y_pred)
print("Actual values: ", y_test)
print("accuracy is", rf_model.score(X_test, y_test))
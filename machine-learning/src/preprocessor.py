import pandas as pd
import os


def preprocess(folder_path):
    with open("../data/config/sensor_whitelist.txt") as f:
        SENSOR_WHITELIST = f.read().splitlines()

    preprocessed_df = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv") and "ImageReading" not in file_name:
            file_path = os.path.join(folder_path, file_name)
            dataframe = pd.read_csv(file_path, sep=";")
            dataframe["sampleTimeStamp.microseconds"] = pd.qcut(dataframe["sampleTimeStamp.microseconds"], q=1, labels=False)
            dataframe = dataframe.groupby(
                ['sampleTimeStamp.seconds', "sampleTimeStamp.microseconds"]).mean().reset_index()
            dataframe.reset_index(drop=True, inplace=True)
            dataframe = dataframe.filter(
                SENSOR_WHITELIST + ["sampleTimeStamp.seconds", "sampleTimeStamp.microseconds", "groundSteering"], axis=1)
            preprocessed_df.append(dataframe)
    result = preprocessed_df[0]
    for df in preprocessed_df[1:]:
        result = pd.merge(
            result, df, on=['sampleTimeStamp.seconds', "sampleTimeStamp.microseconds"], how="outer")

    result = result[result["groundSteering"] != 0]
    return result

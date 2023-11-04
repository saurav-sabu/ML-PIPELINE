# Import the necessary libraries
import os
import sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:

    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts","test.csv")
    raw_data_path = os.path.join("artifacts","raw.csv")


class DataIngestion:

    def __init__(self):
        # Initialize data ingestion configuration
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            # Log that data is being read using Pandas
            logging.info("Data read using Pandas")

            # Read the data from a CSV file
            data = pd.read_csv(os.path.join("notebook/data","income_cleandata.csv"))

            # Create directories if they don't exist and save the data to the raw data path
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)

            # Log that data is being split into train and test sets
            logging.info("Data splitted in train and test")

            # Split the data into train and test sets
            train_set,test_set = train_test_split(data,test_size=0.3,random_state=42)

            # Save the train and test sets to their respective paths
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            # Log that data ingestion is completed
            logging.info("Data Ingestion Completed")

            # Return the paths to the train and test data
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # Log an error message and raise a CustomException in case of an error
            logging.info("Error occured in Data Ingestion")
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    # Create an instance of the DataIngestion class and initiate data ingestion
    obj = DataIngestion()
    obj.initiate_data_ingestion()

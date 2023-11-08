# Import the necessary libraries
import os
import sys

# Custom module imports
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from dataclasses import dataclass


if __name__ == "__main__":

    # Initialize the DataIngestion component
    obj = DataIngestion()
    # Initiate data ingestion and obtain train and test data paths
    train_data_path, test_data_path = obj.initiate_data_ingestion()
    # Initialize the DataTransformation component
    data_transformation = DataTransformation()
    # Initiate data transformation and obtain train and test data arrays
    train_array,test_array,_ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
    # Initialize the ModelTrainer component
    model_training = ModelTrainer()
    # Initiate model training using the transformed data
    model_training.initiate_model_trainer(train_array,test_array)
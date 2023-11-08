# Import the necessary libraries
import os
import sys
import numpy as np
import pandas as pd

# Custom module imports
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object
from dataclasses import dataclass

# Define a class for making predictions
class PredictionPipeline:

    def __init__(self):
        pass

    # Method for making predictions
    def predict(self,features):

        # Define file paths for loading preprocessor and model
        preprocessor_path = os.path.join("artifacts/data_transformation","preprocessor.pkl")
        model_path = os.path.join("artifacts/model_trainer","model.pkl")

        # Load preprocessor and model from pickle files
        processor = load_object(preprocessor_path)
        model = load_object(model_path)

        # Transform input features using the preprocessor
        scaled = processor.transform(features)

        # Make predictions using the model
        pred = model.predict(scaled)

        return pred

# Define a custom class for storing attributes and generating DataFrames  
class CustomClass:

    def __init__(self,age:int,workclass:int,education_num:int,marital_status:int,occupation:int
                                      ,relationship:int,race:int,sex:int,capital_gain:int,capital_loss:int,hours_per_week:int,native_country:int):
        
        # Initialize the object with provided attributes
        self.age = age
        self.workclass = workclass
        self.education_num = education_num
        self.marital_status = marital_status
        self.occupation = occupation
        self.relationship = relationship
        self.race = race
        self.sex = sex
        self.capital_gain = capital_gain
        self.capital_loss = capital_loss
        self.hours_per_week = hours_per_week
        self.native_country = native_country

    # Method to create a DataFrame from object attributes
    def get_dataframe(self):

        try:
            custom_input = {
                "age":[self.age],
                "workclass":[self.workclass],
                "education_num":[self.education_num],
                "marital_status":[self.marital_status],
                "occupation":[self.occupation],
                "relationship":[self.relationship],
                "race":[self.race],
                "sex":[self.sex],
                "capital_gain":[self.capital_gain],
                "capital_loss":[self.capital_loss],
                "hours_per_week":[self.hours_per_week],
                "native_country":[self.native_country]
            }

            # Create a DataFrame from the dictionary
            data = pd.DataFrame(custom_input)
            
            return data
        except Exception as e:
            # Catch exceptions and raise a custom exception
            raise CustomException(e,sys)
        



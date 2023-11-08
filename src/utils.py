# Import the necessary libraries
import os
import sys
import pickle

# Custom module imports
from src.logger import logging
from src.exception import CustomException

# Function to save a Python object to a file using pickle
def save_object(file_path,obj):

    try:
        # Extract the directory path from the provided file path
        dir_path = os.path.dirname(file_path)
        # Create the directory if it doesn't exist (and ignore if it already exists)
        os.makedirs(dir_path,exist_ok=True)

        # Open the file in binary write mode and save the object using pickle
        with open(file_path,"wb") as f:
            pickle.dump(obj,f)

    except Exception as e:
        # Raise a custom exception with logging and error information
        raise CustomException(e,sys)
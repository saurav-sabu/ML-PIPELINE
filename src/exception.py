# Import the necessary libraries
import os
import sys
from src.logger import logging

# Define a function to generate a detailed error message
def error_message_detailed(error,error_detailed:sys):

    # Get the information about the exception
    _,_,exc_tb = error_detailed.exc_info()

    # Extract the filename and line number from the exception
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message [{str(error)}]"

    return error_message

# Define a custom exception class
class CustomException (Exception):

    def __init__(self,error_message,error_detailed:str):
        super().__init__(error_message)
        
        # Generate a detailed error message using the provided information
        self.error_message = error_message_detailed(error_message,error_detailed=error_detailed)

    def __str__(self):
        # Return the detailed error message as a string
        return self.error_message
    

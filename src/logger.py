# Import the necessary libraries
import logging
import sys
import os
from datetime import datetime

# Define a log file name with a timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the log path
# - Join the current working directory with a "logs" directory and the LOG_FILE
# - Ensure that the "logs" directory is created if it doesn't exist
log_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(log_path,exist_ok=True)

# Set the full path to the log file
LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH, # Specify the log file for log messages
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", # Define the log message format
    level=logging.INFO # Set the minimum log level to INFO
)



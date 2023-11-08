# Import the necessary libraries
import os
import sys
import pickle

# Custom module imports
from src.logger import logging
from src.exception import CustomException

# scikit-learn imports
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score,classification_report,precision_score,recall_score
from sklearn.model_selection import GridSearchCV

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
    
def evaluate_model(X_train,y_train,X_test,y_test,models,params):
    try:
        # Create an empty dictionary to store model evaluation results
        report = {

        }

        # Loop through each model to be evaluated
        for i in range(len(list(models))):
            
            # Get the model and its associated hyperparameters
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]
            
            # Perform grid search with cross-validation to find the best hyperparameters
            grid = GridSearchCV(model,param_grid=para,cv=5,scoring="accuracy")
            grid.fit(X_train,y_train)

            # Set the model's hyperparameters to the best parameters found by grid search
            model.set_params(**grid.best_params_)

            # Train the model on the training data
            model.fit(X_train,y_train)

            # Make predictions on the test data
            y_pred = model.predict(X_test)

            # Calculate the accuracy of the model on the test data
            test_model_accuracy = accuracy_score(y_test,y_pred)

            # Store the test accuracy in the report dictionary with the model as the key
            report[list(models.values())[i]] = test_model_accuracy

            # Return the report containing test accuracies for each model
            return report

    except Exception as e:
        logging.info("Error occurred in utils file")
        # Handle any exceptions that may occur during model evaluation
        raise CustomException(e,sys)


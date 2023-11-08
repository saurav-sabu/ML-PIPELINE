# Import the necessary libraries
import os
import sys
import pandas as pd
import numpy as np

# Custom module imports
from src.utils import save_object
from src.logger import logging
from src.exception import CustomException
from src.utils import evaluate_model

# scikit-learn imports
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

from dataclasses import dataclass


@dataclass
class ModelTrainerConfig:

    train_model_file_path = os.path.join("artifacts/model_trainer","model.pkl")

class ModelTrainer:

    def __init__(self):
        # Define configuration parameters for the ModelTrainer
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):

        try:
            # Log information about the process
            logging.info("Splitting into X_train,X_test,y_train,y_test")
            
            # Split the data into training and testing sets
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1])
            
            # Define a dictionary of models to be evaluated
            model = {
                "Random Forest":RandomForestClassifier(),
                "Decision Tree":DecisionTreeClassifier(),
                "Logistic Regression":LogisticRegression()
            }

            # Define parameters to be used in grid search for each model
            params = {"Random Forest":
                      {
                            "class_weight":["balanced"],
                            "max_depth":[10,8,5],
                            "n_estimators":[20,50,30],
                            "min_samples_split":[2,5,10],
                      },
                      "Logistic Regression":{
                            "class_weight":["balanced"],
                            "penalty":["l1","l2"],
                            "C":[0.001,0.01,0.1,1,10,100],
                            "solver":["liblinear","saga"]
                      },
                      "Decision Tree":{
                            "class_weight":["balanced"],
                            "criterion":["gini","entropy","log_loss"],
                            "splitter":["best","random"],
                            "max_depth":[3,4,5,6],
                            "min_samples_split":[2,3,4,5],
                            "min_samples_leaf":[1,2,3],
                            "max_features":["auto","sqrt","log2"]
                      }}
            
            # Evaluate the models and store the results in model_report
            model_report:dict = evaluate_model(X_train=X_train,y_train = y_train,X_test= X_test,y_test=y_test,models=model,params=params)

            # Find the best-performing model
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model.keys())[list(model_report.values()).index(best_model_score)]
            best_model = model[best_model_name]

            # Log information about the best model found
            logging.info(f"Best model found, Model Name:{best_model_name}, Accuracy:{best_model_score}")
            
            # Save the best model to a file
            save_object(file_path=self.model_trainer_config.train_model_file_path,obj=best_model)
            
            
        except Exception as e:
            logging.info("Error occurred in Model Training")
            raise CustomException(e,sys)
        




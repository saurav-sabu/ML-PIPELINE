# Import the necessary libraries
import os
import sys
import pandas as pd
import numpy as np

# Custom module imports
from src.utils import save_object
from src.logger import logging
from src.exception import CustomException

# scikit-learn imports
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from dataclasses import dataclass


# Configuration data class for data transformation
@dataclass
class DataTransformationConfig:
    # Define the path to save the preprocessor object
    preprocess_obj_path = os.path.join("artifacts/data_transformation","preprocessor.pkl")

# DataTransformation class for data preprocessing
class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    # Create a data preprocessing object using scikit-learn
    def get_data_transformation_obj(self):

        try:
            logging.info("Data Transformation started")

            numerical_features = ["age","workclass","education_num","marital_status","occupation"
                                      ,"relationship","race","sex","capital_gain","capital_loss","hours_per_week","native_country"]
            
            # Define a numeric feature pipeline with imputation and scaling    
            num_pipeline = Pipeline(
                    [
                        ("Imputer",SimpleImputer(strategy="median")),
                        ("Scaling",StandardScaler())
                    ]
                )
            
            # Create a ColumnTransformer to apply the numeric feature pipeline to specific features
            preprocessor = ColumnTransformer(
                    [
                        ("Num_pipeline",num_pipeline,numerical_features)
                    ]
                )

            return preprocessor
            
        except Exception as e:
            # Raise a custom exception with logging and error information
            raise CustomException(e,sys)
            
    
    # Remove outliers using the Interquartile Range (IQR) method for a specified column
    def remove_outliers_iqr(self,col,df):

        try:
            logging.info("Handling Outliers")
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)

            iqr = Q3 - Q1
            upper_limit = Q3 + 1.5 * iqr
            lower_limit = Q1 - 1.5 * iqr

            # Replace values above the upper limit with the upper limit and values below the lower limit with the lower limit
            df.loc[(df[col]>upper_limit),col] = upper_limit
            df.loc[(df[col]<lower_limit),col] = lower_limit

            return df

        except Exception as e:
            logging.info("Error occurred in handling outliers")
            # Raise a custom exception with logging and error information
            raise CustomException(e,sys)
        
    # Perform the data transformation process
    def initiate_data_transformation(self,train_path,test_path):

        try:
            logging.info("Data Transformation started")
            # Read training and test data from CSV files
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            numerical_features = ["age","workclass","education_num","marital_status","occupation"
                                      ,"relationship","race","sex","capital_gain","capital_loss","hours_per_week","native_country"]
            
            # Remove outliers from the training data
            logging.info("Outliers removed from train data")
            for col in numerical_features:
                self.remove_outliers_iqr(col=col,df=train_data)

            # Remove outliers from the test data
            logging.info("Outliers removed from test data")
            for col in numerical_features:
                self.remove_outliers_iqr(col=col,df=test_data)
            
            # Get the data preprocessor object
            preprocess_obj = self.get_data_transformation_obj()

            # Define the target column and columns to drop
            target_cols = "income"
            drop_cols = [target_cols]

            # Split the training data into dependent and independent features
            logging.info("Splitting train data into dependent and independent features")
            input_feature_train_data = train_data.drop(drop_cols,axis=1)
            target_feature_train_data = train_data[target_cols]

            # Split the test data into dependent and independent features
            logging.info("Splitting test data into dependent and independent features")
            input_feature_test_data = test_data.drop(drop_cols,axis=1)
            target_feature_test_data = test_data[target_cols]

            # Apply the data preprocessor to the independent features
            input_train_arr = preprocess_obj.fit_transform(input_feature_train_data)
            input_test_arr = preprocess_obj.transform(input_feature_test_data)

            # Combine the preprocessed features with the target variable
            train_array = np.c_[input_train_arr,np.array(target_feature_train_data)]
            test_array = np.c_[input_test_arr,np.array(target_feature_test_data)]

            # Save the data preprocessor object to a specified file path
            save_object(file_path=self.data_transformation_config.preprocess_obj_path,
                        obj = preprocess_obj)
            
            # Return the transformed training and test data along with the path to the preprocessor object
            return (train_array,
                    test_array,
                    self.data_transformation_config.preprocess_obj_path)

        except Exception as e:
            logging.info("Error occurred in data transformation")
            # Raise a custom exception with logging and error information
            raise CustomException(e,sys)





import os 
import pandas as pd
import sys
import numpy as np
from src.logging.logger import logging
from src.exception.customexception import NetworkSecurityException
from src.constant import trainpipeline
from src.constant.trainpipeline import shema, TARGET_COLUMN, DATA_IMPUTER_PARAMS
from src.entity.config import DATATRANSFORMATION_CONFIG
from src.entity.artifects import DATA_VALIDATION_AR, DataTransformationArtifact
from src.utilsfile.util import read_shema, write_yaml_file, save_numpy_array_data, save_object
from sklearn.impute import SimpleImputer,KNNImputer
from sklearn.pipeline import Pipeline

class DATA_TRANSFORM:
    def __init__(self, data_validation: DATA_VALIDATION_AR,data_transform_config: DATATRANSFORMATION_CONFIG):
        try:
            self.data_validation: DATA_VALIDATION_AR = data_validation
            self.data_transform_config: DATATRANSFORMATION_CONFIG = data_transform_config
        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

    @staticmethod
    def read_shema(filepath) -> pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

    def get_preprocessing(cls)-> Pipeline:
        try:
            # Only numeric columns → median works
            imputer:KNNImputer=KNNImputer(**DATA_IMPUTER_PARAMS)
            #imputer = SimpleImputer(strategy="median")
            perpoce:KNNImputer= Pipeline([('imputer', imputer)])
            return perpoce
        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

    def initiate_Transform(self)-> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            # Load train/test CSV
            train_df = DATA_TRANSFORM.read_shema(self.data_validation.data_valid_train)
            test_df = DATA_TRANSFORM.read_shema(self.data_validation.data_valid_test)

            # Separate features and target
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

            # ✅ Keep only numeric features
            input_feature_train_df = input_feature_train_df.select_dtypes(include=[np.number])
            input_feature_test_df = input_feature_test_df.select_dtypes(include=[np.number])

            logging.info(f"Numeric features used for transformation: {list(input_feature_train_df.columns)}")

            # Build preprocessing pipeline
            preprocessor = self.get_preprocessing()

            # Fit and transform
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            # Combine features + target
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # Save numpy arrays
            save_numpy_array_data(self.data_transform_config.data_training_file_trans, array=train_arr,)
            save_numpy_array_data(self.data_transform_config.data_testing_file_trans, array=test_arr,)

            # Save preprocessor object
            save_object(self.data_transform_config.data_trans_pre, preprocessor_object,)
            save_object("final_model/preprocessor.pkl", preprocessor_object,)

            # Build artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transform_config.data_trans_pre,
                transformed_train_file_path=self.data_transform_config.data_training_file_trans,
                transformed_test_file_path=self.data_transform_config.data_testing_file_trans
            )

            logging.info("Data transformation completed successfully ✅")
            return data_transformation_artifact

        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

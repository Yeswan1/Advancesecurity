
import os 
import sys
import pandas as pd
import numpy as np
from src.exception.customexception import NetworkSecurityException
from src.logging.logger import logging
TARGET_COLUMN='Result'
train_data_csv:str='train.csv'
test_data_csv:str='test.csv'
artifects:str='artifects'
pipline:str='networksecuritypipline'
Filename:str="phisingData_clean.csv"

MODEL_FILE_PATH=os.path.join('save_model')
MODEL_FILE='model.pkl'

shema=os.path.join('shemafile','shema.yaml')
#dataingestion constent

DATA_INGESTION_DATABASE:str='sample_mflix'
DATA_INGESTION_COLLECTION:str="comments"
DATA_INGESTION_DIR:str="data_ingestion"
DATA_INGESTION_FEATURESTORE:str='rawdata'
DATA_INGESTION_DIR_FILE:str='ingestion'
DATA_INGESTION_TEST_TRAIN_SPILT:float=0.2

## Data  validation

DATA_VALIDATION_FILE_DIR:str='data_valudation'
DATA_VALIDATION_VALID_DIR:str='valid'
DATA_VALIDATION_INVALID_DIR:str='in_valid'
DATA_VALUDATION_SCHEMA_FILE:str='schema_Report'
DATA_VALUDATION_SCHEMA_DIR:str='schema.yaml'
DATA_VALUDATION_PREPROCSSING='preprocessing.pkl'

##Data Transformation
DATA_TRANSFORMATION_FILE_DIR:str='data_transformation'
DATA_TRANSFORMATION_DIR:str='transformation'
DATA_TRANSFORMATION_OBJ:str='pickle_trans'
DATA_IMPUTER_PARAMS:dict={
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",

}
DATA_TRANSFORMATION_TRAINING_PATH:str='train.npy'
DATA_TRANSFORMATION_TESTING_PATH:str='test.npy'

##model Training
MODEL_TRAIN_DIR:str='modelTrain'
MODEL_TRAIN_DIR_FILE:str='model'
MODEL_TRAIN_MODEL_DIR:str='modle.pkl'
MODEL_EXCPECTED_SCORE:float=0.6
MODEL_UNDERFITTED_VALUE:float=0.05




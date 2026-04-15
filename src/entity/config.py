import os 
import sys
from src.exception.customexception import NetworkSecurityException
from src.logging.logger import logging
from src.constant import trainpipeline
from dataclasses import dataclass
from datetime import datetime
#print(trainpipeline.artifects)

class TRAINING_PIPLINE:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline=trainpipeline.pipline
        self.artifects=trainpipeline.artifects
        self.artifects_dir=os.path.join(self.artifects,timestamp)
        self.model=os.path.join("model")
        self.timestamp:str=timestamp

class TRAINING_DATA_INGESTION_CONFIG:
    def __init__(self,training_config:TRAINING_PIPLINE):
        self.dataingestion_config:str=os.path.join(
            training_config.artifects_dir,trainpipeline.DATA_INGESTION_DIR_FILE
        )
        self.feature_score:str=os.path.join(
            self.dataingestion_config,trainpipeline.DATA_INGESTION_FEATURESTORE,trainpipeline.Filename
        
        )
        self.training_csv:str=os.path.join(
            self.dataingestion_config,trainpipeline.DATA_INGESTION_DIR_FILE,trainpipeline.train_data_csv
        )
        self.testing_csv:str=os.path.join(
            self.dataingestion_config,trainpipeline.DATA_INGESTION_DIR_FILE,trainpipeline.test_data_csv
        )
        self.test_train_spilt:float=trainpipeline.DATA_INGESTION_TEST_TRAIN_SPILT
        self.database_name:str=trainpipeline.DATA_INGESTION_DATABASE
        self.collection_name:str=trainpipeline.DATA_INGESTION_COLLECTION



class DATAVALIDATION_CONFIG:
    def __init__(self,data_validation_dir:TRAINING_PIPLINE):
        self.data_valudation_config:str=os.path.join(data_validation_dir.artifects_dir,trainpipeline.DATA_VALIDATION_FILE_DIR)
        self.validation:str=os.path.join(self.data_valudation_config,trainpipeline.DATA_VALIDATION_VALID_DIR)
        self.invalidation:str=os.path.join(self.data_valudation_config,trainpipeline.DATA_VALIDATION_INVALID_DIR)
        self.train_valid:str=os.path.join(self.validation,trainpipeline.train_data_csv)
        self.train_invalid:str=os.path.join(self.invalidation,trainpipeline.train_data_csv)
        self.test_valid:str=os.path.join(self.validation,trainpipeline.test_data_csv)
        self.test_invalid:str=os.path.join(self.invalidation,trainpipeline.test_data_csv)
        self.shema_file= os.path.join(
            self.data_valudation_config,
            trainpipeline.DATA_VALUDATION_SCHEMA_FILE,
            trainpipeline.DATA_VALUDATION_SCHEMA_DIR
        )
        self.preproc = os.path.join(
            self.data_valudation_config,
            trainpipeline.DATA_VALUDATION_PREPROCSSING
        )
class DATATRANSFORMATION_CONFIG:
    def __init__(self,datatransformation:TRAINING_PIPLINE):
        self.data_transformation_config:str=os.path.join(datatransformation.artifects_dir,trainpipeline.DATA_TRANSFORMATION_FILE_DIR)
        self.data_training_file_trans:str=os.path.join(self.data_transformation_config,trainpipeline.DATA_TRANSFORMATION_DIR,
            trainpipeline.train_data_csv.replace('csv','npy'),)
        self.data_testing_file_trans:str=os.path.join(self.data_transformation_config,trainpipeline.DATA_TRANSFORMATION_DIR,
            trainpipeline.test_data_csv.replace('csv','npy'),)
        self.data_trans_pre:str=os.path.join(self.data_transformation_config,trainpipeline.DATA_TRANSFORMATION_OBJ,
            trainpipeline.DATA_VALUDATION_PREPROCSSING,)
        
class MODELTRAINING_CONFIG:
    def __init__(self,modeltraining:TRAINING_PIPLINE):
        self.model_train_config:str=os.path.join(modeltraining.artifects_dir,trainpipeline.MODEL_TRAIN_DIR)
        self.model_train_save:str=os.path.join(self.model_train_config,trainpipeline.MODEL_TRAIN_DIR_FILE,trainpipeline.MODEL_FILE)
        self.model_eximate_score:float=trainpipeline.MODEL_EXCPECTED_SCORE
        self.model_underfitted=trainpipeline.MODEL_UNDERFITTED_VALUE
import os
import sys
from src.logging.logger import logging
from src.exception.customexception import NetworkSecurityException
from src.constant import trainpipeline
from src.entity.config import(
    TRAINING_PIPLINE,TRAINING_DATA_INGESTION_CONFIG,DATAVALIDATION_CONFIG,
    DATATRANSFORMATION_CONFIG,MODELTRAINING_CONFIG
    )
from src.entity.artifects import(
    DATA_INGESTION_AR,DATA_VALIDATION_AR,DataTransformationArtifact,
    ModeltrainArtifects
)
from src.components.data_ingestion import complete_dataingestion
from src.components.data_validation import datavalidation
from src.components.data_transform import DATA_TRANSFORM
from src.components.model_training import ModelTrainer

class complete_train_pipline:
    def __init__(self):
        self.data_training_config=TRAINING_PIPLINE()

    def strat_data_ingestion(self):
        try:
            self.data_ingestion_config=TRAINING_DATA_INGESTION_CONFIG(data_ingestion_config=self.data_training_config)
            data_ingestion=complete_dataingestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifects=data_ingestion_artifects.final_convert()
            return data_ingestion_artifects

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def start_data_validation(self,data_ingestion_artifects:DATA_INGESTION_AR):
        try:
            data_validation_config=DATAVALIDATION_CONFIG(data_ingestion_config=self.data_training_config)
            data_validation_artifects=datavalidation(data_ingestion_artifects=data_ingestion_artifects,data_validation_config=data_validation_config)
            data_validation_artifact=data_ingestion_artifects.final_convert()
            return data_validation_artifact
            
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
    
    def start_data_transform(self,data_validation_artifects:DATA_VALIDATION_AR):
        try:
            data_transform_config=DATATRANSFORMATION_CONFIG(data_ingestion_config=self.data_training_config)
            data_transform_artifects=DATA_TRANSFORM(data_validation_artifects=data_validation_artifects,data_transform_config=data_transform_config)
            data_transform_artifact=data_transform_artifects.initiate_Transform()
            return data_transform_artifact
            
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def start_model_trainer(self,data_transform_artifact:DataTransformationArtifact)->ModeltrainArtifects:
        try:
            self.model_trainer_config:MODELTRAINING_CONFIG = MODELTRAINING_CONFIG(
                data_ingestion_config=self.data_training_config
            )

            model_trainer = ModelTrainer(
                data_transform_artifact=data_transform_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.strat_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transform(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
        
            return model_trainer_artifact
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)


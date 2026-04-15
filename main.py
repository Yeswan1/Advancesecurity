import os 
import pandas as pd
import sys
import numpy as np
from src.logging.logger import logging
from src.exception.customexception import NetworkSecurityException
from src.entity.config import TRAINING_PIPLINE,TRAINING_DATA_INGESTION_CONFIG,DATAVALIDATION_CONFIG,DATATRANSFORMATION_CONFIG,MODELTRAINING_CONFIG
from src.entity.artifects import DATA_INGESTION_AR,DATA_VALIDATION_AR,DataTransformationArtifact,Modelmetricsevalutor,ModeltrainArtifects
from src.constant import trainpipeline
from src.components.data_ingestion import complete_dataingestion
from src.components.data_validation import datavalidation
from src.components.data_transform import DATA_TRANSFORM
from src.components.model_training import ModelTrainer
if __name__=='__main__':
        trainingpipelineconfig=TRAINING_PIPLINE()
        dataingestionconfig=TRAINING_DATA_INGESTION_CONFIG(trainingpipelineconfig)
        data_ingestion=complete_dataingestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.final_convert()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)
        data_validation_config=DATAVALIDATION_CONFIG(trainingpipelineconfig)
        data_validation=datavalidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.intiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)
        data_transformation_config=DATATRANSFORMATION_CONFIG(trainingpipelineconfig)
        logging.info("data Transformation started")
        data_transformation=DATA_TRANSFORM(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_Transform()
        print(data_transformation_artifact)
        logging.info("data Transformation completed")

        logging.info("Model Training sstared")
        model_trainer_config=MODELTRAINING_CONFIG(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")
   











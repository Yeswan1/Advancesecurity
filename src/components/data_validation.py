import os 
import pandas as pd
import sys
import numpy as np
from src.logging.logger import logging
from src.exception.customexception import NetworkSecurityException
from src.constant import trainpipeline
from src.constant.trainpipeline import shema
from src.entity.config import TRAINING_DATA_INGESTION_CONFIG,DATAVALIDATION_CONFIG
from src.entity.artifects import DATA_INGESTION_AR,DATA_VALIDATION_AR
from src.utilsfile.util import read_shema,write_yaml_file
from scipy.stats import ks_2samp
class datavalidation:
    def __init__(self,training_data_ingestion:DATA_INGESTION_AR,
                 data_validation:DATAVALIDATION_CONFIG):
        try:
            self.training_data_ingestion=training_data_ingestion
            self.data_validation=data_validation
            self._shema_file=read_shema(shema)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def data_from(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def fill_dection(self,dataframe:pd.DataFrame)->bool:
        try:
            lenofshema=self._shema_file
            lenofdata=len(dataframe.columns)
            if lenofdata==lenofshema:
                return True
            return False
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def detect_file(self,base_df,constent_df,thershold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
    
                d1=base_df[column]
                d2=constent_df[column]
                combind=ks_2samp(d1,d2)
                if thershold<=combind.pvalue:
                 is_Found=False
            else:
                status=False
                is_Found=True
                report.update({column:{
                    'p_value':float(combind.pvalue),
                    'shema_drift':is_Found
                }})

            drift_report_file_path = self.data_validation.shema_file
            file=os.path.dirname(drift_report_file_path)
            os.makedirs(file,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)





        except Exception as ex:
            raise NetworkSecurityException(ex,sys)


    


    def intiate_data_validation(self)->DATA_VALIDATION_AR:
        try:
            training=self.training_data_ingestion.train_data_csv
            testing=self.training_data_ingestion.test_data_csv


            train_df=datavalidation.data_from(training)
            test_df=datavalidation.data_from(testing)

            status=self.fill_dection(dataframe=train_df)
            if not status:
                logging.info('error meassage')

            status=self.fill_dection(dataframe=test_df)
            if not status:
                logging.info('error meassage')

            status=self.detect_file(base_df=train_df,constent_df=test_df)
            dir_path=os.path.dirname(self.data_validation.train_valid)

            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(self.data_validation.train_valid,index=False, header=True)
            train_df.to_csv(self.data_validation.test_valid,index=False, header=True)

            data_validation_artifects=DATA_VALIDATION_AR(
                data_validation_staus=status,
                data_valid_train=self.training_data_ingestion.train_data_csv,
                data_invalid_train=None,
                data_valid_test=self.training_data_ingestion.test_data_csv,
                data_invalid_test=None,
                data_shema_file=self.data_validation.shema_file,
            )

            return data_validation_artifects


        except Exception as ex:
            raise NetworkSecurityException(ex,sys)

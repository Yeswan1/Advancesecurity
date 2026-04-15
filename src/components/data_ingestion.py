import os 
import pandas as pd
import sys
import numpy as np
from src.logging.logger import logging
from src.exception.customexception import NetworkSecurityException
from src.constant import trainpipeline
from src.entity.config import TRAINING_DATA_INGESTION_CONFIG
from src.entity.artifects import DATA_INGESTION_AR
from typing import List
import pymongo
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')

class complete_dataingestion:
    def __init__(self,data_ingestion_dir:TRAINING_DATA_INGESTION_CONFIG):
        try:
            self.data_ingestion_dir=data_ingestion_dir
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def read_dataset_db(self):
        try:
            database_name=self.data_ingestion_dir.database_name
            collection_name=self.data_ingestion_dir.collection_name
            self.pymongo=pymongo.MongoClient(MONGO_DB_URL)
            records=self.pymongo[database_name][collection_name]
            
            df=pd.DataFrame(list(records.find()))
            if '_id' in df.columns.to_list():
                df.drop(columns=['_id'],axis=1)

            df.replace({'nan':np.nan},inplace=True)
            return df
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    
    def covert_raw(self,dataframe:pd.DataFrame):
        try:
          feature_store_file_path=self.data_ingestion_dir.feature_score
          feature_path=os.path.dirname(feature_store_file_path)
          os.makedirs(feature_path,exist_ok=True)
          dataframe.to_csv(feature_store_file_path,index=False,header=True)
          return dataframe

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        

    def convert_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_dir.test_train_spilt)
            file_path=os.path.dirname(self.data_ingestion_dir.training_csv)
            os.makedirs(file_path,exist_ok=True)

            train_set.to_csv(self.data_ingestion_dir.training_csv,index=False,header=True)
            test_set.to_csv(self.data_ingestion_dir.testing_csv,index=False,header=True)
            

        
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        

    def final_convert(self):
        try:
            dataframe=self.read_dataset_db()
            dataframe=self.covert_raw(dataframe)
            self.convert_train_test(dataframe)
            
            data_artifects=DATA_INGESTION_AR(train_data_csv=self.data_ingestion_dir.training_csv,
                                            test_data_csv=self.data_ingestion_dir.testing_csv)
            return data_artifects
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)



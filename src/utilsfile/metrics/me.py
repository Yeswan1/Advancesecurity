
import os 
import pandas as pd
import sys
import numpy as np
from src.logging.logger import logging
from src.exception.customexception import NetworkSecurityException
from src.entity.artifects import Modelmetricsevalutor
from sklearn.metrics import f1_score,precision_score,recall_score
from src.constant.trainpipeline import MODEL_FILE,MODEL_FILE_PATH
import sys

def get_classification_score(y_true,y_pred)->Modelmetricsevalutor:
    try:
            
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classification_metric =  Modelmetricsevalutor(f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    



class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            if isinstance(x, pd.DataFrame):
                expected_features = list(getattr(self.preprocessor, "feature_names_in_", []))
                if expected_features:
                    missing_features = [col for col in expected_features if col not in x.columns]
                    if missing_features:
                        raise NetworkSecurityException(
                            f"Missing required feature columns: {missing_features}",
                            sys,
                        )
                    # Keep only columns used during fit and in the same order.
                    x = x[expected_features]

            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

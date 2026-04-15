from dataclasses import dataclass
@dataclass
class DATA_INGESTION_AR:
    train_data_csv:str
    test_data_csv:str
@dataclass
class DATA_VALIDATION_AR:
    data_validation_staus:bool
    data_valid_train:str
    data_invalid_train:str
    data_valid_test:str
    data_invalid_test:str
    data_shema_file:str
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str
    
@dataclass
class Modelmetricsevalutor:
    f1_score:float
    recall_score:float
    precision_score:float

@dataclass
class ModeltrainArtifects:
    model_train_file:str
    model_train_metrics:Modelmetricsevalutor
    model_test_metrics:Modelmetricsevalutor




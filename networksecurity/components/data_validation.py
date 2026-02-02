import pandas as pd
import numpy as np
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from scipy.stats import ks_2samp
import os
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    @staticmethod
    def read_file(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Number of columns in Schema Config is {number_of_columns}")
            logging.info(f"Input Dataframe has {len(dataframe.columns)} columns")
            if (len(dataframe.columns) == number_of_columns):
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self,base_df, current_df, threshold=0.05) -> bool :
        try:
            status=True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                sample_distribution_value = ks_2samp(d1,d2)
                if (threshold <= sample_distribution_value.pvalue):
                    is_Found = False
                else:
                    is_Found=True
                    status=False
                report.update({column:{
                    "p-value" : float(sample_distribution_value.pvalue),
                    "Drift_status" : is_Found  
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create Directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read data from train and test
            trained_dataframe = DataValidation.read_file(train_file_path)
            test_dataframe = DataValidation.read_file(test_file_path)

            #Validate number of columns in Train
            status = self.validate_number_of_columns(trained_dataframe)
            if not status:
                error_message = f"Train Dataframe does not contain all columns.\n"

            #Validating number of columns in Test
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Test Dataframe does not contain all columns.\n"

            # Validate numerical columns exist in Train
            if (trained_dataframe.select_dtypes(include=['int','float']).empty):
                status = False
                error_message = f"No numerical columns founf in train dataframe."

            # Validate numerical columns exist in Test
            if (test_dataframe.select_dtypes(include=['int','float']).empty):
                status = False
                error_message = f"No numerical columns founf in test dataframe."

            # Detect Data Drift
            status = self.detect_dataset_drift(base_df=trained_dataframe, current_df=test_dataframe)
            if status:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path, exist_ok = True)
                dir_path = os.path.dirname(self.data_validation_config.valid_test_file_path)
                os.makedirs(dir_path, exist_ok = True)

                trained_dataframe.to_csv(self.data_validation_config.valid_train_file_path, header=True, index=False)
                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,header=True,index=False)

            # else:
            #     dir_path = os.path.dirname(self.data_validation_config.invalid_train_file_path)
            #     os.mkdirs(dir_path, exist_ok = True)
            #     dir_path = os.path.dirname(self.data_validation_config.invalid_test_file_path)
            #     os.mkdirs(dir_path, exist_ok = True)

            #     trained_dataframe.to_csv(self.data_validation_config.invalid_train_file_path, header=True, index=False)
            #     test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path,header=True,index=False)

            datavalidationartifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
                invalid_train_file_path=None, #self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=None #self.data_validation_config.invalid_test_file_path
            )

            return datavalidationartifact

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)




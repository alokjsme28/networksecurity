from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
import sys
import os
import pandas as pd

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def export_collection_as_dataframe(self):
        '''
        Read data from Mongo DB
        '''
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            
            collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            # Mongo DB by default adds an extra column named _id
            if '_id' in df.columns.to_list():
                df.drop(columns=["_id"],axis=1,inplace=True)

            df.replace({"na":np.nan},inplace=True)

            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        finally:
            self.mongo_client.close()

    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Create Folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed Train Test Split on Dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting Train Test File Path")

            train_set.to_csv(self.data_ingestion_config.training_file_path, header=True, index=False)

            test_set.to_csv(self.data_ingestion_config.testing_file_path, header=True, index=False)

            logging.info(f'Exported Train & Test file path')

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            dataingestionartifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path= self.data_ingestion_config.testing_file_path)
            return dataingestionartifact

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)


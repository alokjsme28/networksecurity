from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

if __name__ == "__main__":
    try:
        train_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(train_pipeline_config)
        obj = DataIngestion(data_ingestion_config)
        logging.info("Initiate Data Ingestion")
        dataingestionartifact=obj.initiate_data_ingestion()
        print(dataingestionartifact)
    except Exception as ex:
        raise NetworkSecurityException(ex,sys)
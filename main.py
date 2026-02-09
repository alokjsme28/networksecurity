from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

if __name__ == "__main__":
    try:
        train_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(train_pipeline_config)
        obj = DataIngestion(data_ingestion_config)
        logging.info("Initiate Data Ingestion")
        data_ingestion_artifact=obj.initiate_data_ingestion()
        print(data_ingestion_artifact)
        print()
        logging.info("Data Ingestion complete")

        logging.info("Data Validation start")
        data_validation_config = DataValidationConfig(train_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        print()
        logging.info("Data Validation complete")

        logging.info("Data Transformation start")
        data_transformation_config = DataTransformationConfig(train_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                 data_transformation_config=data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_ingestion_artifact)
        print()
        logging.info("Data Transformation complete")

        logging.info("Model Training started")
        model_trainer_config = ModelTrainerConfig(train_pipeline_config)
        model_trainer = ModelTrainer(data_transformation_artifact,model_trainer_config)
        model_trainer_artifact = model_trainer.initiate_model_training()
        #print(model_trainer_artifact)
        #print()
        logging.info("Model Training Complete")



    except Exception as ex:
        raise NetworkSecurityException(ex,sys)
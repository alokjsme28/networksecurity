import os, sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            return self.model.predict(x_transform)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
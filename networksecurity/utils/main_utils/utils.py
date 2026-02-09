import yaml
import sys
import pickle
import os
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,'r') as file_obj:
            return yaml.safe_load(file_obj)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str, content:object, replace:bool = False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,'w') as file_obj:
            yaml.dump(content, file_obj)
    except Exception as ex:
        raise NetworkSecurityException(ex,sys)
    
def save_numpy_array_data(file_path:str, array:np.array):
    # Save numpy array data to file
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as ex:
        raise NetworkSecurityException(ex,sys)

def save_object(file_path:str, obj: object ) -> None:
    try:
        logging.info("Entered the save object method of main_utils class")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of main_utils class")
    except Exception as ex:
        raise NetworkSecurityException(ex,sys)
    
def load_object(file_path:str) -> object:
    try:
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"The file path {file_path} does not exists")
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as ex:
        raise NetworkSecurityException(ex,sys)

def load_numpy_array_data(file_path:str):
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as ex:
        raise NetworkSecurityException(ex,sys)
    
def evaluate_models(X_train, X_test, y_train, y_test, models, model_params):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = model_params[list(models.keys())[i]]

            rcv = RandomizedSearchCV(estimator=model, param_distributions=param,cv=3)
            rcv.fit(X_train,y_train)

            model.set_params(**rcv.best_params_)
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_Score = r2_score(y_train,y_train_pred)

            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    except Exception as ex:
        raise NetworkSecurityException(ex,sys)


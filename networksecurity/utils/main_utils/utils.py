import yaml
import sys
import pickle
import os
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

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

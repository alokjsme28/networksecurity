import yaml
import sys
import os
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

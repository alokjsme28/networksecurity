import os
from dotenv import load_dotenv
import sys
import json
import pandas as pd
import numpy as np
import pymongo
import certifi
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException


# Load all Environment variables
load_dotenv()

# Fetch our URL from .env
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# This is basically for a trusted certificate authority SSL/TLS like that.
ca = certifi.where()


class NetworkSecurityExtract():
    def __init__(self):
        try:
            pass
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        

    def csv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.to_json(orient='records'))
            #records = list(json.loads(data.T.to_json()).values())   # Both output same
            return records
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        

    def insert_data_mongodb(self,records,database,collection):
        try:
            # self.database = database
            # self.collection = collection
            # self.records = records

            client = pymongo.MongoClient(MONGO_DB_URL)

            db = client[database]
            col = db[collection]

            result = col.insert_many(records)

            return len(result.inserted_ids)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        finally:
            client.close()
        

if __name__ == "__main__":
    File_Path = "Network_Data/phisingData.csv"
    Database = "ALOK_IND"
    Collection = "NetworkData"

    obj = NetworkSecurityExtract()
    Records = obj.csv_to_json_convertor(File_Path)
    print(obj.insert_data_mongodb(Records,Database,Collection))



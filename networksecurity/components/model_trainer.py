import os
import sys

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.entity.artifacts_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import save_object, load_object, load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import mlflow

import dagshub
dagshub.init(repo_owner='alokjsme28', repo_name='networksecurity', mlflow=True)

class ModelTrainer:
    def __init__(self, 
                                data_transformation_artifact:DataTransformationArtifact,
                                model_trainer_config : ModelTrainerConfig ) -> ModelTrainerArtifact:
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def track_mlflow(self, best_model, classificationmetrics):
        try:
            with mlflow.start_run():
                f1_score = classificationmetrics.f1_score
                recall_score = classificationmetrics.recall_score
                precision_score = classificationmetrics.precision_score

                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("precision_score",precision_score)
                mlflow.log_metric("recall_score",recall_score)
                mlflow.sklearn.log_model(best_model, "model")
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def train_model(self,X_train,X_test, y_train, y_test):
        try:
            model = {
                "Random Forest" : RandomForestClassifier(verbose=1),
                "Decision Tree" : DecisionTreeClassifier(),
                "KNN Classifier" : KNeighborsClassifier(),
                "Adaboost" : AdaBoostClassifier(),
                "Gradient Boost" : GradientBoostingClassifier(verbose=1),
                "Logistic Regression" : LogisticRegression(verbose=1),
            }

            params = {
                "Decision Tree" : {
                    'criterion' : ['gini','entropy','log-loss'],
                    'max_depth' : [3,5,8]
                },
                "Random Forest" : {
                    'n_estimators' : [50,100,150,200],
                },
                "KNN Classifier" : {
                    'n_neighbors' : [3,5,8],
                },
                "Adaboost" : {
                    'learning_rate' : [0.01,0.1,1],
                    'n_estimators' : [10,25,50],
                },
                "Logistic Regression" : {
                    'penalty' : ['l1', 'l2', 'elasticnet'],
                },
                "Gradient Boost" : {
                    'learning_rate' : [0.01,0.1,1],
                    'n_estimators' : [10,25,50],
                    'subsample' : [0.7,0.8,0.9],
                }

            }

            model_report : dict = evaluate_models(X_train, X_test,y_train,y_test, model, params)

            best_model_score = max(sorted(model_report.values()))

            # To get the best model name
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = model[best_model_name]

            y_train_pred = best_model.predict(X_train)

            classification_train_metric=get_classification_score(y_train,y_train_pred)

            # Track the experiments with ML FLOW
            self.track_mlflow(best_model,classification_train_metric)

            y_test_pred = best_model.predict(X_test)

            classification_test_metric = get_classification_score(y_test, y_test_pred)

            #Trak teh experiments with MLFLOW
            self.track_mlflow(best_model,classification_test_metric)

            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)

            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor, best_model)

            save_object(self.model_trainer_config.trained_model_file_path, network_model)

            save_object("final_model/model.pkl",best_model)

            ## Model Trainer Artifact

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path= self.model_trainer_config.trained_model_file_path,
                train_metric_artifact= classification_train_metric,
                test_metric_artifact= classification_test_metric
            )

            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")

            return model_trainer_artifact


        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
    
    def initiate_model_training(self) -> ModelTrainerArtifact:
        logging.info("Initiated Model Training")
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #Loading train and test numpy array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, X_test, y_train, y_test = (
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
            )

            model_trainer_artifact = self.train_model(X_train,X_test,y_train,y_test)
            
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)

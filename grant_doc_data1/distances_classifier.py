import os
import json
import datetime
import numpy as np
import pandas as pd
import xgboost as xgb
import sklearn.model_selection
from jarowinkler import jaro_winkler
from grant_doc_data1.string_distance_features import NameDistance 

class distancesClassifier():
    def __init__(self, model_dir: str, model_type: str = 'xgb'):
        self.model = (self._initialize_xgb_model() if model_type == 'xgb' 
                      else self._initialize_random_forest())
        self.metadata = {}
        self.model_dir = model_dir
        # ADDED THE NAME DISTANCE 
        self.name_distance = NameDistance()

    def train(self, df: pd.DataFrame, labels: pd.Series):
        """Train our classifier with features to predict models.

        Args:
            df (pd.DataFrame): DataFrame containing the necessary columns
            labels (pd.Series): set of associated labels per row
        """
        features = self.name_distance.training_data(df)
        features, features_test, labels, labels_test = (
            sklearn.model_selection.train_test_split(features, labels, test_size=0.2))
        self.model.fit(features, labels)
        self.metadata['training_date'] = datetime.datetime.now().strftime('%Y%m%d')
        self.metadata['training_rows'] = len(labels)
        
        self.metadata['accuracy'] = self.assess(features_test, labels_test)

    def predict(self, df: pd.DataFrame, proba: bool = False) -> np.ndarray:
        """Use a trained model to predict the output 

        Args:
            df (pd.DataFrame): the input DataFrame
            proba (bool, optional): whether to return probabilities. Defaults to False.

        Returns:
            np.ndarray: True or False labels for every row in features or 
                probabilities of true for every row of features
        """
        features = self.name_distance.training_data(df)
        if len(self.metadata) == 0:
            raise ValueError('Model must be trained first')
        
        if proba:
            return self.model.predict_proba(features)[:, 0]
        
        return self.model.predict(features)

    def assess(self, features: pd.DataFrame, labels: pd.Series) -> float:
        """compute the accuracy of our model 

        Args:
            features (pd.DataFrame): input features 
            labels (pd.Series): known labels

        Returns:
            float: the accuracy of our model 
        """
        pred_labels = self.predict(features)
        return (pred_labels == labels.sum())/len(labels)
    
    def save(self, filename: str, overwrite: bool = False):
        """save file name location model_path on hard drive"""
        if len(self.metadata) == 0:
            raise ValueError('Model must be trained before saving')
        
        today = datetime.datetime.now().strftime('%y%m%d')
        if filename[-5:].lower() != '.json':
            filename += '.json'

        path = os.path.join(self.model_dir, filename)
        metadata_path = os.path.splitext(path)[0] + 'metadata.json'

        if not overwrite and (os.path.exists(path) or os.path.exists(metadata_path)):
            raise FileExistsError('Cannot overwrite existing file')
        
        self.model.save_model(path)
        with open(metadata_path) as fo:
            json.dump(self.metadata, fo)

    def load(self, filename: str):
        """Load in a model filename with associated metadata from model_dir"""
        path = os.path.join(self.model_dir, filename)
        metadata_path = os.path.splitext(path)[0] + 'metadata.json'
        self.model.load_model(path)
        
        with open(metadata_path) as fr:
            self.metadata = json.load(fr)

    def _initialize_xgboost(self):
        """Create a new xgbclassifier"""
        return xgb.XGBClassifier()

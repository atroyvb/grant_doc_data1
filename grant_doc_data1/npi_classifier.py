import os
import json
import datetime
import numpy as np
import pandas as pd
import xgboost as xgb
import sklearn.model_selection

class NPIClassifier():  #CAMEL CASE BECAUSE IT'S A CLASS
    def __init__(self, model_dir: str, model_type: str = 'xgb'):
        self.model = (self._initialize_xgb_model() if model_type == 'xgb' 
                      else self._initialize_random_forest())
        self.metadata = {}
        self.model_dir = model_dir
        

    # TRAIN FUNCTION
    def train(self, features: pd.DataFrame, labels: pd.Series):
        """Train our classifier with features to predict models.

        Args:
            features (pd.DataFrame): data frame of features --
                the components used for calculations which may be created
                from the data 
            labels (pd.Series): set of associated labels per row
        """
        #self.model.train()
        features, features_test, labels, labels_test = (
            sklearn.model_selection.train_test_split(features, labels, test_size = 0.2))
        self.model.fit(features, labels)
        self.metadata['training_date'] = datetime.datetime.now().strftime('%Y%m%d')
        self.metadata['training_rows'] = len(labels)
        
        self.metadata['accuracy'] = self.assess(features_test, labels_test)



    # PREDICT FUNCTION
    def predict(self,
                features: pd.DataFrame, 
                proba: bool = False) -> np.ndarray:
        """Use a trained model to predict the output 

        Args:
            features (pd.DataFrame): the input features
            proba (bool, optional): whether to return probabilities. Defaults to False.

        Returns:
            np.ndarray: True or False labels for every row in features or 
                probabilities of true for every row of features
        """
        if len(self.metadata) == 0:
            raise ValueError('Model must be trained first')
        
        if proba:
            return self.model.predict_proba(features)[:, 0]
        
        return self.model.predict(features)

    #ASSESS FUNCTION 
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
    
    #SAVE FUNCTION
    def save(self, filename: str, path:str, overwrite: bool = False):
        """save file name location model_path on hard drive"""
        if len(self.metadata) == 0:
            raise ValueError('Model must be trained before saving')
        
        # want to check the date the file was saved so its the same one
        today = datetime.datetime.now().strftime('%y%m%d')
        if path[:6] != today:
            filename = f'{today}_{filename}'

        # ugly way DON'T USE 
        # if filename[-5:].lower() != 'json':
        #     filename = filename + '.json'

        # # ugly way 2  DON'T USE 
        # dot_pos = filename.find('.')
        # if filename[dot_pos:] != 'json':
        #     filename = filename + '.json'

        # # pretty way 
        # if os.path.splitext(filename)[1] != '.json':
        #     filename = filename + '.json'

        # We are saving our file here 
        path = os.path.join(self.model_dir, filename)
        metadata_path = os.path.splitext(path)[0] + 'metadata.json'


        # os.path.join?
        # pickle
            # pickle is dangerous on rare cases because it depends on having 
            # access to the class VERSION that was used for saving 
        # Ensure .json

        if not overwrite and (os.path.exists(path) or os.path.exists(metadata_path)):
            raise FileExistsError('Cannot overwrite existing file')
        

        self.model.save_model(path)
        with open(metadata_path) as fo:
            json.dump(self.metadata, fo)

    #LOAD FUNCTION
    def load(self, filename: str):
        """Load in a model filename with associated metadata from model_dir"""
        path = os.path.join(self.model_dir, filename)
        metadata_path = os.path.splitext(path)[0] + 'metadata.json'
        self.model.load_model(path)
        
        with open(metadata_path) as fr:
            self.metadata = json.load(fr)



    def _initialize_xgboost():
        """Create a new xgbclassifier"""
        return xgb.XGBCLassifier()

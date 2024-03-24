import fasttext
import jarowinkler 
import numpy as np
import pandas as pd
from regex import D 

from grant_doc_data1 import read_grants_year 

class string_distance_reader():
    def __init__(self, ft_model_path: str = 'data/cc.en.50.bin'):
        self.ft_model = fasttext.load_model(ft_model_path)

    def combine_prediction_data(self, grants: pd.DataFrame, npi: pd.DataFrame) -> pd.DataFrame:
        """_Combine grants and npi dataframe into pairs  """
        grants = grants.add_prefix('grant_')
        npi = npi.add_prefix('npi_')
        grants['merge_val'] = 1
        npi['merge_val'] = 1

        return grants.merge[npi, on='merge_val']



    def features_from_pairs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Computes distance features from a dataframe of pairs of grant_ and npi_ data"""
        # grants data has:
            # last_name, forename, organization, city, state, country
        # NPI Data has: 
            # last_name, first_name, city, state, country, address
        # prefix of grant_ or npi_
        data_cols = df.columns

        df['jw_dist_last'] = df.apply(lambda row: 
                                 jarowinkler.jarosimularity(row['grant_last_name'],
                                                            row['npi_last_name']), axis = 1)
        df['jw_dist_first'] = df.apply(lambda row: 
                                 jarowinkler.jarosimularity(row['grant_first_name'],
                                                            row['npi_first_name']), axis = 1)
        df['match_city'] = df.apply(lambda row: 
                                    (row['grant_city'] == row['npi_city']), axis = 1)
        df['match_state'] = df.apply(lambda row: 
                                    (row['grant_state'] == row['npi_state']), axis = 1)
        
        for dataset in ['grant', 'npi']:
            for col in ['last_name', 'forename']:
                df[f'vec_{dataset}_{col}'] = df[f'{dataset}_{col}'].apply(lambda x: self.ft_model.get_sentence_vector(x))

        df['ft_dist_last_name'] = df.apply(lambda row: np.linalg.norm((row['vec_grant_last_name']) - row['vec_npi_last_name']),
                                            axis = 1)
        
        return df.drop(columns=data_cols).drop(columns=[
            v for v in df.columns if 'vec' in v])




# ft_model = fasttext.load_model('data/cc.en/50.bin')
# ft_model.get_sentence_vector(s1.lower())

if __name__ == '__main__':
    df = read_grants_year(2022)
    df = read('data/')
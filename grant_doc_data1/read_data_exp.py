import pandas as pd
from sklearn.model_selection import train_test_split
import pickle

class GrantsData:
    def __init__(self, path: str):
        self.df = pd.read_csv(path)

    def read(self) -> pd.DataFrame:
        """Returns a cleaned dataframe"""
        df = self._select_columns(self.df)
        self.df = self._clean(df)

        return self.df

        # Data can have NaNs
        # Different types (reasonable)
        # Different types (unreasonable)
        #print(self.df)
        #print(self.df.isna().sum())


    @staticmethod
    def _select_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Rename and select columns
        NOTE: Underscored methods are "private methods", otherwise 
        meaning that we should only call them from WITHIN the class.

        Args:
            df (pd.DataFrame): dataframe

        Returns:
            pd.DataFrame: the subset, clean name dataframe
        """
        mapper = {
            'APPLICATION_ID': 'application_id',
            'BUDGET_START': 'budget_start',
            'ACTIVITY': 'grant_type',
            'TOTAL_COST': 'total_cost',
            'PI_NAMEs': 'pi_names',
            'PI_IDS': 'pi_ids',
            'ORG_NAME': 'organization',
            'ORG_CITY': 'city',
            'ORG_STATE': 'state',
            'ORG_COUNTRY': 'country'
        }
        return df.rename(columns=mapper)[mapper.values()]
    
    @staticmethod
    def _clean(df: pd.DataFrame) -> pd.DataFrame:
        """Remove NaNs and other cleaning functions

        Args:
            df (pd.DataFrame): dataframe with subset column names

        Returns:
            pd.DataFrame: dataframe free of NaNs
        """
        df['pi_names'] = df['pi_names'].str.split(';')
        df = df.explode('pi_names')
        df['is_contact'] = df['pi_names'].str.lower().str.contains('(contact)')
        df['pi_names'] = df['pi_names'].str.replace('(contact)', '')
        df['both_names'] = df['pi_names'].apply(lambda x: x.split(',')[:2])
        df[['last_name', 'forename']] = pd.DataFrame(df['both_names'].to_list(), index=df.index)

        #Getting modes
        start_mode = df['budget_start'].mode()[0]  

        # Impute missing values in 'PROJECT_START' and 'PROJECT_END' with the mode. I did this because for all dates missing in this column
        # There are also dates missing in the budget_end column, so imputing with the most frequent date will most likely capture the 
        # Pattern. Budgets may typically start on a certain date as well, and choosing the mode would capture this.
        df['budget_start'].fillna(start_mode, inplace=True)

        return df




def read_grants_year(year) -> pd.DataFrame:
    """Read in Grants Data for a year and return as clean dataframe

    Args:
        year (int | str): year to read

    Returns:
        pd.DataFrame: clean dataframe of grants data
    """
    # We know the filename is: RePORTER_PRJ_C_FY2022.zip
    path = r'/Users/alexistroy/grant_doc_data1/grant_doc_data1/data/pl_pfile_20050523-20240211.csv'
    gd = GrantsData(path.format(year=year))
    return gd.read()


if __name__ == '__main__':
    import numpy as np
    # '/mnt/search/data/grants/RePORTER_PRJ_C_FY2022.zip'

    vec1 = [i for i in range(1_000_000)]
    vec2 = np.arange(1_000_000)

    print(read_grants_year(2022).isna().sum())

    

    
    # gd = GrantsData()
import pandas as pd


class GrantsData:
    def __init__(self, path: str):
        self.df = pd.read_csv(path, compression='zip')

    def read(self) -> pd.DataFrame:
        """Returns a cleaned dataframe"""
        df = self._select_columns(self.df)
        df = self._clean(df)
        # Data can have NaNs
        # Different types (reasonable)
        # Different types (unreasonable)
        print(self.df)

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
        print(df)

        



def read_grants_year(year: int | str) -> pd.DataFrame:
    """Read in Grants Data for a year and return as clean dataframe

    Args:
        year (int | str): year to read

    Returns:
        pd.DataFrame: clean dataframe of grants data
    """
    # We know the filename is: RePORTER_PRJ_C_FY2022.zip
    path = "/Users/alexistroy/Downloads/RePORTER_PRJ_C_FY2022.zip"
    gd = GrantsData(path.format(year=year))
    return gd.read()



if __name__ == '__main__':
    import numpy as np
    # '/mnt/search/data/grants/RePORTER_PRJ_C_FY2022.zip'

    vec1 = [i for i in range(1_000_000)]
    vec2 = np.arange(1_000_000)

    read_grants_year(2022)
    # gd = GrantsData()

def fill_in_budget(year: int | str) -> pd.DataFrame:
    """ To fill in the missing dates for the 'budget_start' column

    Args:
        year (int | str): year to read 

    Returns:
        pd.DataFrame: All of the dates filled in 
    """
    #path = "/Users/alexistroy/Downloads/RePORTER_PRJ_C_FY2022.zip"
    #gd2 = GrantsData(path.format(year=year))
    
    
    

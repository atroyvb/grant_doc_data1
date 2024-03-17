import pandas as pd


def read(path):
    """read in NPI 

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """

    df = pd.read_csv(path)

    mapper = {
            'NPI': 'npi',
            'Healthcare Provider Taxonomy Code_1': 'taxonomy_code',
            'Provider Last Name (Legal Name)': 'last_name',
            'Provider First Name': 'first_name',
            'Provider First Line Business Practice Location Address': 'address',
            'Certification Date': 'cert_date',
            'Provider Business Practice Location Address State Name': 'city',
            'Provider Business Practice Location Address State Name': 'state',
            'Provider Business Practice Location Address Country Code (If outside U.S.)': 'country'
        }
    
    df = df.rename(columns=mapper)[mapper.values()]

    return df

    #There are 850 missing values for taxonomy_code, address, state, and country
    #There are 6,259 missing last names and 6,262 missing first names
    #There are 1,505 missing values for cert_date


if __name__ == '__main__':
    df = read("data/pl_pfile_20050523-20240211.csv")
    print(df.head())
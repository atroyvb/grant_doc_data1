import sqlalchemy
from grant_doc_data1 import npi_reader
from grant_doc_data1 import read_data_exp


def db():
    """
    This function creates a sqlalchemy engine connection to the database
    """
    engine = sqlalchemy.create_engine(
        'sqlite:///data/grant_npi.db'
    )

    conn = engine.connect()

    return conn

def npi_csv_to_db(csv_path: str):
    """
    This function creates a database out of the npi csv dataset
    """

    #Make npi data
    df = npi_reader.read(csv_path)

    #Subsetting to desired columns
    df = df[['last_name', 'forename', 'city', 'state', 'country']]

    #Translating pandas dataframe to database
    df.to_sql('npi',
              db(),
              if_exists='append',
              index=False
              #Big Data
              #method = 'multi'
              #chunksize=1000
              )
    
def grants_csv_to_db(year: int):
    """
    This function creates a relational database out of the grants csv dataset
    """

    #reading in data
    df = read_data_exp.read_grants_year(year)

    #subsetting to desired columns
    df = df[['last_name', 'forename', 'city', 'state', 'country']]


    #Translating pandas dataframe to database
    df.to_sql('grants',
              db(),
              if_exists='append',
              index=False
              )
    

if __name__ == '__main__':
    npi_csv_to_db(r"/Users/alexistroy/grant_doc_data1/grant_doc_data1/data/pl_pfile_20050523-20240211.csv")
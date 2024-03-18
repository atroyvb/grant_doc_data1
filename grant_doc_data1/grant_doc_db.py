import sqlalchemy
from grant_doc_data1 import npi_reader


def db():
    engine = sqlalchemy.create_engine(
        'sqlite:///data/grant_npi.db'
    )

    conn = engine.connect()

    return conn

def npi_csv_to_db(csv_path: str):
    df = npi_reader.read(csv_path)
    df.to_sql('npi',
              db(),
              if_exists='append',
              index=False
              #Big Data
              #method = 'multi'
              #chunksize=1000
              )
    
def grants_csv_to_db(year: int):
    df = read.read_grants_year(year)
    df.to_sql('grants',
              db(),
              if_exists='append',
              index=False
              )
    

if __name__ == '__main__':
    npi_csv_to_db(r"/Users/alexistroy/grant_doc_data1/grant_doc_data1/data/pl_pfile_20050523-20240211.csv")
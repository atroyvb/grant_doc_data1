import pandas as pd 
import sqlalchemy
from grant_doc_data1 import grants_reader 

def db():
    engine = sqlalchemy.create_engine('sqlite://data/grant_npi.db')
    return engine


def npi_csv_to_db9(csv_path : str):
    df = grants_reader.read_grants_year(22)
    df.to_sql('npi',
              db(),
              if_exists = 'append',
              index = False)
            # method = 'multi'
            # chunksize = 1000


# import sqlite3

# query = '''
# CREATE TABLE IF NOT EXISTS npi(
#     id INTEGER PRIMARY KEY,
#     lastname VARCHAR(100) NOT NULL,
#     forename VARCHAR(100),

#     med_school BOOL NOT NULL 
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
# );
# '''

# conn = sqlite3.connect('data/grant_npi.db')
# cursor = conn.cursor()

# version_query = 'select sqlite_version();'
# cursor.execute(version_query)
# record = cursor.fetchall()
# print('version is: ', record)

# cursor.close()

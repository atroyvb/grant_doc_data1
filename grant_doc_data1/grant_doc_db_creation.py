import pandas as pd
import sqlalchemy

from grant_doc_data1 import grants_reader


def db():
    engine = sqlalchemy.create_engine('sqlite:///data/grant_npi.db')
    conn = engine.connect()
    return conn


def npi_csv_to_db(csv_path: str):
    df = grants_reader.read_grants_year(22)
    df.to_sql('npi',
              db(),
              if_exists='append',
              index=False)
              # method='multi',
              # chunksize=1000


# # Another slash
# engine = sqlalchemy.create_engine(
#     'sqlite:////Users/arthur/teaching/duq_ds3_2023/data/live_test_sqlite.db')
# df = pd.read_csv('data/affiliations.csv')

# # Have to account for SQLAlchemy v2
# with engine.connect() as conn:
#     df.to_sql('aff', conn, index=False, if_exists='append')
#     df2 = pd.read_sql(sqlalchemy.text('SELECT * FROM aff'), conn)
# print(df2)


if __name__ == '__main__':
    npi_csv_to_db('')
import sqlite3

query = '''
CREATE TABLE IF NOT EXISTS npi (
    id INTEGER PRIMARY KEY,
    lastname VARCHAR(100) NOT NULL,
    forename VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

'''

query2 = '''
CREATE TABLE IF NOT EXISTS grants (
    id INTEGER PRIMARY KEY,
    lastname VARCHAR(100) NOT NULL,
    forename VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

'''

query3 = '''
CREATE TABLE IF NOT EXISTS npi_grants_bridge (
    id INTEGER PRIMARY KEY,
    npi_id INTEGER NOT NULL,
    grants_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (npi_id) REFERENCES npi(id),
    FOREIGN KEY (grants_id) REFERENCES grants(id)
);

'''

#Connecting to database
conn = sqlite3.connect('data/grant_npi.db')
cursor = conn.cursor()

#Executing Queries
cursor.execute(query)
cursor.execute(query2)
cursor.execute(query3)


#Selecting Version
version_query = 'select sqlite_version()'
cursor.execute(version_query)
record = cursor.fetchall()
print('version is', record)

cursor.close()
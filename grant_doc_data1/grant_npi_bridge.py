import sqlite3

#Connecting to database
conn = sqlite3.connect('data/grant_npi.db')
cursor = conn.cursor()

#Defining Queries for bridge table
query = '''
INSERT INTO npi_grants_bridge(npi_id)
SELECT id FROM npi;

'''

query2 = '''
INSERT INTO npi_grants_bridge(grants_id)
SELECT id FROM grants;

'''

#Executing Queries
cursor.execute(query)
cursor.execute(query2)

#Selecting Version
version_query = 'select sqlite_version()'
cursor.execute(version_query)
record = cursor.fetchall()
print('version is', record)

cursor.close()
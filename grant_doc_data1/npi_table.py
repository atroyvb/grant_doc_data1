import sqlite3

query = '''
CREATE TABLE IF NOT EXISTS npi(
    id INTEGER PRIMARY KEY,
    lastname VARCHAR(100) NOT NULL,
    forename VARCHAR(100),
    address VARCHAR(100), 
    certdate DATE,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    med_school BOOL NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

conn = sqlite3.connect('data/grant_npi.db')
cursor = conn.cursor()

# Execute the CREATE TABLE query
cursor.execute(query)

# Check SQLite version
version_query = 'SELECT sqlite_version();'
cursor.execute(version_query)
record = cursor.fetchall()
print('SQLite version is:', record)

# Close the cursor and connection
cursor.close()
conn.close()

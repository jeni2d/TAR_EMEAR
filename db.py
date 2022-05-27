import sqlite3



sqlite_connection = sqlite3.connect('c:/job/python/TAR_EMEAR/country_docs_tar.db')
cursor = sqlite_connection.cursor()	

				
cursor.execute("""CREATE TABLE IF NOT EXISTS docs(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                country TEXT,
                date TEXT,
                url TEXT,
                doc_name TEXT);
                """)

sqlite_connection.commit()
cursor.close()

if (sqlite_connection):
	sqlite_connection.close()

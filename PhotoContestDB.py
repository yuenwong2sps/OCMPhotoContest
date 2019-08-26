import sqlite3

DBPATH = "./db/pythonsqlite.db"

con = sqlite3.connect(DBPATH)
print("Database opened successfully")

sql_create_photoentry_table = """ CREATE TABLE IF NOT EXISTS PhotoEntries (
                                                  id integer PRIMARY KEY AUTOINCREMENT,
                                                  uploadtime text NOT NULL,
                                                  tel text NOT NULL,
                                                  photoPath text NOT NULL,
                                                  fellowship text NOT NULL,
                                                  tagName text NOT NULL
                                                  )
                                                  """

con.execute(sql_create_photoentry_table)

print("Table created successfully")

con.close()

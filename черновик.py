import sqlite3

con=sqlite3.connect('silki.db')
cursor=con.cursor()
cursor.execute('SELECT * FROM link')
for i in cursor.fetchall():
    print(i)
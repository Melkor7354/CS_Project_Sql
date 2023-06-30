import sqlite3 as sql


def test():
    con = sql.connect('test.db')
    con.execute('''CREATE TABLE IF NOT EXISTS Test(ID int primary key not null, Name varchar(20) not null)''')
    con.execute('''INSERT INTO Test VALUES(1, 'Eklavya') ''')
    con.commit()
    cur = con.cursor()
    a = cur.fetchall()
    return a

def que():
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Test;''')
    a = cur.fetchall()
    return a

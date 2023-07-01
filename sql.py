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


def sign_up(username, password):
    con = sql.connect('test.db')
    con.execute('''CREATE TABLE IF NOT EXISTS Auth(Username varchar(20) not null, password varchar(20) not null)''')
    con.execute('''INSERT INTO Auth VALUES("{}", "{}")'''.format(username, password))
    con.commit()


def login(username, password):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Auth WHERE username="{}" AND password="{}"'''.format(username, password))
    a = cur.fetchall()
    con.commit()
    if len(a) != 0:
        return True
    else:
        return False

import sqlite3 as sql


def initialize():
    con = sql.connect('x.db')
    con.execute("CREATE TABLE IF NOT EXISTS Auth(username varchar(20) primary key not null, password varchar(20) not null)")
    con.execute("CREATE TABLE IF NOT EXISTS SignedIn(Boolean int not null)")
    con.commit()


def signed_in():
    con = sql.connect('x.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM SignedIn")
    signed_up = cur.fetchall()
    if len(signed_up) == 0:
        return False
    else:
        return True


def sign_up(username, password):
    con = sql.connect('x.db')
    con.execute('''CREATE TABLE IF NOT EXISTS Auth(Username varchar(20) not null, password varchar(20) not null)''')
    con.execute('''INSERT INTO Auth VALUES("{}", "{}")'''.format(username, password))
    con.execute('''INSERT INTO SignedIn VALUES(1)''')
    con.commit()


def login(username, password):
    con = sql.connect('x.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Auth WHERE username="{}" AND password="{}"'''.format(username, password))
    a = cur.fetchall()
    con.commit()
    if len(a) != 0:
        return True
    else:
        return False

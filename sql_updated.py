import sqlite3 as sql
import os

parent_dir = os.path.expanduser('~')
_dir = 'billing_db'
path = os.path.join(parent_dir, _dir)
        
        
def initialize():
    try:
        mode = 0o666
        os.mkdir(mode=mode, path=path)
    except FileExistsError:
        pass
    con = sql.connect(r'{}\x.db'.format(path))
    con.execute('''CREATE TABLE IF NOT EXISTS Auth(username varchar(20) primary key not null, 
    password varchar(20) not null)''')
    con.execute("CREATE TABLE IF NOT EXISTS SignedIn(Boolean int not null)")
    con.execute('''CREATE TABLE IF NOT EXISTS Products(Product_ID int primary key auto_increment, Product_Name varchar(30) not null, 
    Product_Type varchar(20)''')
    con.execute('''CREATE TABLE IF NOT EXISTS Inventory(Product_ID int not null, product_name varchar(30) not null, 
    quantity int not null, FOREIGN KEY(Product_ID) REFERENCES Products(Product_ID) ON DELETE CASCADE)''')
    con.commit()


def signed_in():
    con = sql.connect(r'{}\x.db'.format(path))
    cur = con.cursor()
    cur.execute("SELECT * FROM SignedIn")
    signed_up = cur.fetchall()
    if len(signed_up) == 0:
        return False
    else:
        return True


def sign_up(username, password):
    con = sql.connect(r'{}\x.db'.format(path))
    con.execute('''CREATE TABLE IF NOT EXISTS Auth(Username varchar(20) not null, password varchar(20) not null)''')
    con.execute('''INSERT INTO Auth VALUES("{}", "{}")'''.format(username, password))
    con.execute('''INSERT INTO SignedIn VALUES(1)''')
    con.commit()


def login(username, password):
    con = sql.connect(r'{}\x.db'.format(path))
    cur = con.cursor()
    cur.execute('''SELECT * FROM Auth WHERE username="{}" AND password="{}"'''.format(username, password))
    a = cur.fetchall()
    con.commit()
    if len(a) != 0:
        return True
    else:
        return False


def update_inventory(values):
    con = sql.connect(r'{}\x.db'.format(path))
    for i in values:
        try:
            pass
        except:
            pass

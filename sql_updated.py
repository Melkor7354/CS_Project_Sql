import sqlite3 as sql
import os

parent_dir = os.path.expanduser('~')
_dir = 'billing_db'
path = os.path.join(parent_dir, _dir)
con = sql.connect(r'{}\z.db'.format(path))
cur = con.cursor()
        

def initialize():
    try:
        mode = 0o666
        os.mkdir(mode=mode, path=path)
    except FileExistsError:
        pass
    con.execute('''CREATE TABLE IF NOT EXISTS Auth(username varchar(20) primary key not null, 
    password varchar(20) not null)''')
    con.execute("CREATE TABLE IF NOT EXISTS SignedIn(Boolean int not null)")
    con.execute('''CREATE TABLE IF NOT EXISTS Products(Product_ID integer primary key AUTOINCREMENT, 
    Product_Name varchar(30) not null, 
    Product_Type varchar(20), Cost int not null, Selling_Price int not null)''')
    con.execute('''CREATE TABLE IF NOT EXISTS Inventory(Product_ID int not null, product_name varchar(30) not null, 
    quantity int not null, FOREIGN KEY(Product_ID) REFERENCES Products(Product_ID) ON DELETE CASCADE)''')
    con.commit()


def signed_in():
    cur.execute("SELECT * FROM SignedIn")
    signed_up = cur.fetchall()
    if len(signed_up) == 0:
        return False
    else:
        return True


def sign_up(username, password):
    con.execute('''CREATE TABLE IF NOT EXISTS Auth(Username varchar(20) not null, password varchar(20) not null)''')
    con.execute('''INSERT INTO Auth VALUES("{}", "{}")'''.format(username, password))
    con.execute('''INSERT INTO SignedIn VALUES(1)''')
    con.commit()


def login(username, password):
    cur.execute('''SELECT * FROM Auth WHERE username="{}" AND password="{}"'''.format(username, password))
    a = cur.fetchall()
    con.commit()
    if len(a) != 0:
        return True
    else:
        return False


def enter_products(values):
    for i in values:
        con.execute("INSERT INTO Products VALUES(NULL, '{}', '{}', {}, {})".format(i[0].title(),
                                                                                   i[1].title(), i[2], i[3]))
    con.commit()
    
    cur.execute("SELECT * FROM Products")
    a = len(cur.fetchall())
    b = len(values)
    cur.execute("SELECT Product_ID, Product_Name FROM Products where Product_ID>{}".format(a-b))
    c = cur.fetchall()
    for i in c:
        cur.execute("SELECT Product_ID FROM Inventory where Product_ID={}".format(i[0]))
        if len(cur.fetchall()) > 0:
            pass
        else:
            con.execute("INSERT INTO Inventory Values({}, '{}', 0)".format(i[0], i[1]))
    con.commit()


def check_products(values):
    for i in values:
        cur.execute("SELECT * FROM Products where Product_Name='{}'".format(i[0]))
        a = cur.fetchall()
        if len(a) > 0:
            return False
        else:
            continue
    return True


def update_inventory(values):
    for i in values:
        con.execute("update Inventory set quantity = quantity + {} where Product_ID={}".format(i[0], i[1]))
    con.commit()


def check_data_integrity(values):
    for i in values:
        cur.execute('SELECT * FROM Products where Product_ID={}'.format(i[0]))
        a = cur.fetchall()
        if len(a) == 0:
            return False
        else:
            continue
    return True


def display_inventory():
    cur.execute('SELECT * FROM Inventory')
    return cur.fetchall()


cur.execute("SELECT * FROM Products")
print(cur.fetchall())

import sqlite3

def generateDatabase():
    conn = sqlite3.connect('Databases/trading_Ledger.db') 
    conn.close()
    

def generateTableTrade():
    conn = sqlite3.connect('Databases/trading_Ledger.db') 
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS trade (
                       id INTEGER PRIMARY KEY,
                       clientOrderId TEXT,
                       timestamp INTEGER,
                       paire TEXT ,
                       side TEXT,
                       received FLOAT,
                       price FLOAT,
                       commentaire TEXT
                       )
                   """) #received = how much token you received
    conn.commit()
    conn.close()
    
    
def deleteTableTrade():
    conn = sqlite3.connect('Databases/trading_Ledger.db') 
    cursor = conn.cursor()
    cursor.execute("""
                   DROP TABLE IF EXISTS trade
                   """)
    conn.commit()
    conn.close()
  
    
def addTrade(id,clientOrderId,timestamp,paire,side,received,price,commentaire):
    conn = sqlite3.connect('Databases/trading_Ledger.db') 
        
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO trade(id, clientOrderId, timestamp, paire, side, received, price, commentaire) VALUES( ?, ?, ?, ? , ?, ?, ?, ?)""", 
                   (int(id),clientOrderId,int(timestamp),paire,side,float(received),float(price),commentaire))
    conn.commit()
    conn.close()
    
    
def readTrade(caract):
    if(caract == ''):
        conn = sqlite3.connect('Databases/trading_Ledger.db') 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trade ORDER BY id" )
        out = cursor.fetchall()
        conn.close()
    else:
        caract = str(caract)
        conn = sqlite3.connect('Databases/trading_Ledger.db') 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contact WHERE paire = '" + caract + "' OR side = '" + caract + "'")
        out = cursor.fetchall()
        conn.close()            
    return out


def generateTableWallet():
    conn = sqlite3.connect('Databases/trading_Ledger.db') 
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS wallet (
                       id INTEGER PRIMARY KEY,
                       coin TEXT,
                       timestamp INTEGER,
                       price FLOAT ,
                       quantityOwned FLOAT)
                   """) 
    conn.commit()
    conn.close()

def deleteTableWallet():
    conn = sqlite3.connect('Databases/trading_Ledger.db') 
    cursor = conn.cursor()
    cursor.execute("""
                   DROP TABLE IF EXISTS wallet
                   """)
    conn.commit()
    conn.close()
    
    
def addWallet(coin,timestamp,price,quantity):
    """
    price par rapport à l'usdt'
    """
    conn = sqlite3.connect('Databases/trading_Ledger.db') 
    
    cursor = conn.cursor()
    
    cursor.execute("""SELECT max(id) FROM wallet""")
    id = 0 
    a = cursor.fetchall()
    if (a != [(None,)]):
        id = int(a[0][0]) + 1
    
    
    cursor.execute("""
                   INSERT INTO wallet (id, coin, timestamp, price, quantityOwned) VALUES( ?, ?, ?, ?, ?)""", 
                   (id,coin,timestamp,price,quantity))
    conn.commit()
    conn.close()
    
def readWallet(caract):
    if(caract == ''):
        conn = sqlite3.connect('Databases/trading_Ledger.db') 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wallet ORDER BY id" )
        out = cursor.fetchall()
        conn.close()
    else:
        caract = str(caract)
        conn = sqlite3.connect('Databases/trading_Ledger.db') 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contact WHERE coin = '" + caract + "' OR timestamp = '" + caract + "'")
        out = cursor.fetchall()
        conn.close()            
    return out    
    
    
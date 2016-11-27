
import sqlite3


class DB:
    path = 'my.sqlite'

    def __init__(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS users
(id INTEGER PRIMARY KEY NOT NULL,
raiting REAL,
poruchitel_id INT,
age INT,
city VARCHAR,
sex BOOLEAN)''')

        c.execute(
            '''CREATE TABLE IF NOT EXISTS creditUser
(id INTEGER PRIMARY KEY NOT NULL,
summ REAL,
percent REAL)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS transactions (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
credit_id INT,
cust_id INT,
summa REAL,
created VARCHAR,
days_stop VARCHAR,
cust_reiting REAL)''')
        conn.commit()
        c.close()
        conn.close()

    def addUser(self, id, raiting, poruchitel_id, age, city, sex):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (id, raiting, poruchitel_id, age, city, sex) "
            "VALUES (?,?,?,?,?,?)", (id, raiting,
                                     poruchitel_id,
                                     age, city, sex))
        conn.commit()
        c.close()
        conn.close()

    def getUser(self, id):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        data = c.execute("SELECT * FROM users WHERE id = {}".format(id)).fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data[0] if data else data


    def getAllUser(self):
        conn= sqlite3.connect(self.path)
        c = conn.cursor()
        data = c.execute("SELECT * FROM users ").fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    def addCreditMan(self, id, summ, percent):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO creditUser (id, summ, percent) "
            "VALUES (?,?,?)", (id, summ, percent))
        conn.commit()
        c.close()
        conn.close()

    def getCreditMan(self, id):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        data = c.execute("SELECT * FROM creditUser WHERE id = {}".format(id)).fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data[0] if data else data

    def addTransaction(self, credit_id, cust_id, summa, cust_reiting):
        result = False
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        data = c.execute(
            "SELECT * FROM transactions WHERE cust_id = {} AND days_stop IS NULL".format(cust_id)).fetchall()
        if not data:
            result = True
            c.execute(
                "INSERT INTO transactions (credit_id , cust_id , summa , created , cust_reiting) VALUES (?,?,?,?,?)",
                (credit_id, cust_id, summa, sqlite3.datetime.datetime.now(), cust_reiting))
        conn.commit()
        c.close()
        conn.close()
        return result

    def getNotClosedTransactions(self, cust_id):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        data = c.execute(
            "SELECT * FROM transactions WHERE cust_id = {} AND days_stop IS NULL".format(cust_id)).fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    def getSuccessTransactions(self, cust_id):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        data = c.execute(
            "SELECT * FROM transactions WHERE cust_id = {} AND days_stop IS NOT NULL".format(cust_id)).fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    def closeTransaction(self, cust_id):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute(
            "UPDATE transactions SET days_stop=?  WHERE cust_id=?",
            (sqlite3.datetime.datetime.now(), cust_id,))
        conn.commit()
        c.close()
        conn.close()

    def updtaeUserRating(self, id, raiting):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute(
            "UPDATE users SET raiting=?  WHERE id=?", (raiting, id,))
        conn.commit()
        c.close()
        conn.close()

    def updateCreditManInfo(self, summ, percent):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute(
            "UPDATE creditUser SET summ=?, percent=?  WHERE id=?", (summ, percent, id,))
        conn.commit()
        c.close()
        conn.close()

import sqlite3


class DBHelper:

    def __init__(self, dbname="outc.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS outcome (amount number, owner text)"
        outidx = "CREATE INDEX IF NOT EXISTS outIndex ON outcome (amount ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON outcome (owner ASC)"
        self.conn.execute(stmt)
        self.conn.execute(outidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_outcome(self, out_amount, owner):
        stmt = "INSERT INTO outcome (amount, owner) VALUES (?, ?)"
        args = (out_amount, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_outcome(self, out_amount, owner):
        stmt = "DELETE FROM outcome WHERE amount = (?) AND owner = (?)"
        args = (out_amount, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_outcome(self, owner):
        stmt = "SELECT amount FROM outcome WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_total_outcome(self, owner):
        stmt = "SELECT SUM(amount) FROM outcome WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

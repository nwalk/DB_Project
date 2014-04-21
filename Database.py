"""
Database Module
Nathan Walker
nwalk19@gmail.com
"""

import psycopg2

class DBConnect():
    """Creates a database connection and a cursor"""
    def __init__(self):
        self.conn = psycopg2.connect("""dbname=DbProject user=postgres
                                        host=localhost password=postgres""")
        self.cur = self.conn.cursor()
        self.conn.commit()
        print("Connected")

class DBOperations(DBConnect):
    """This class performs all the operations
       needed to work with the database"""

    def addAppliance(self, a, b, m, p):
        self.cur.execute("""INSERT INTO appliance (app_type, brand, model, price)
                            VALUES (%s, %s, %s, %s);""", (a, b, m, p,))
        self.conn.commit()
        self.cur.execute("""SELECT MAX(id) FROM appliance;""")
        x = self.cur.fetchone()
        print x[0]
        
    def addCustomer(self, n, p, a):
        self.cur.execute("""INSERT INTO customer (name, phone, address)
                            VALUES (%s, %s, %s);""", (n, p, a,))
        self.conn.commit()

    def searchName(self, n):
        self.cur.execute("""SELECT * FROM customer
                            WHERE name = %s;""", (n,))
        x = self.cur.fetchall()
        for a,b,c,d in x:
            print a,b,c,d
        
    def searchPhone(self, p):
        self.cur.execute("""SELECT * FROM customer
                            WHERE phone = (%s);""", (p,))
        x = self.cur.fetchall()
        for a,b,c,d in x:
            print a,b,c,d

    def saleTicket1(self, n, p, a, app):
        self.cur.execute("""SELECT * FROM customer
                            WHERE name = (%s)
                            AND phone = (%s);""", (n, p,))
        x = self.cur.fetchone()
        print x
        if x == None:
            self.cur.execute("""INSERT INTO customer (name, phone, address)
                            VALUES (%s, %s, %s);""", (n, p, a,))
            self.conn.commit()
            DBOperations().saleTicket2(n, p, a, app)
        else:
            DBOperations().saleTicket2(n, p, a, app)
        
    def saleTicket2(self, n, p, a, app=''):
        self.cur.execute("""SELECT id FROM customer
                            WHERE name = (%s)
                            AND phone = (%s);""", (n, p,))
        x = self.cur.fetchone()
        self.cur.execute("""INSERT INTO sales (cust_id, date)
                            VALUES (%s, Now());""", (x,))
        self.conn.commit()
        self.cur.execute("""SELECT MAX(id) FROM sales;""")
        ID = self.cur.fetchone()
        for app_id in app:
                self.cur.execute("""INSERT INTO sold_appl(sale_id,
                                                          cust_id,
                                                          appl_id,
                                                          date)
                                    VALUES (%s, %s, %s, Now());""",
                                (ID, x, app_id,))
                self.conn.commit()
        
    def createTable(self):
        """Creates tables appliance, customer, sales, and sold_appl"""
        self.cur.execute("""CREATE TABLE appliance(id serial,
                                                   app_type varchar,
                                                   brand varchar,
                                                   model varchar,
                                                   price numeric
                                                   );"""
                         )
        self.conn.commit()
        
        self.cur.execute("""CREATE TABLE customer(id serial,
                                                  name varchar(20),
                                                  phone varchar,
                                                  address varchar
                                                  );"""
                         )
        self.conn.commit()

        self.cur.execute("""CREATE TABLE sales(id serial,
                                               cust_id integer,
                                               date timestamp,
                                               delivery_date timestamp,
                                               war_exp timestamp                                          
                                               );"""
                         )
        self.conn.commit()
        self.cur.execute("""CREATE TABLE sold_appl(id serial,
                                                   sale_id integer,
                                                   cust_id integer,
                                                   appl_id integer,
                                                   date timestamp
                                                   );"""
                         )
        self.conn.commit()
        print("Tables Created")

    def dropTables(self):
        """Drops tables; appliance, customer, sales, and sold_appl"""
        self.cur.execute("""DROP TABLE appliance;""")
        self.cur.execute("""DROP TABLE customer;""")
        self.cur.execute("""DROP TABLE sales;""")
        self.cur.execute("""DROP TABLE sold_appl;""")
        self.conn.commit()
        print("Tables Dropped")


                        



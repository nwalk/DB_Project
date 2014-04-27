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
        cust_id = raw_input("Please enter customer ID:")
        self.cur.execute("""SELECT * FROM sold_appl NATURAL JOIN appliance
                            WHERE cust_id = (%s);""", (cust_id,))
        purchase = self.cur.fetchall()
        print purchase
        
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
                            VALUES (%s, current_date);""", (x,))
        self.conn.commit()
        self.cur.execute("""SELECT MAX(id) FROM sales;""")
        ID = self.cur.fetchone()


        self.cur.execute("""SELECT * FROM money
                            WHERE date = current_date;""")
        date = self.cur.fetchone()
        if date == None:
            self.cur.execute("""INSERT INTO money(washer,
                                                  dryer,
                                                  refrigerator,
                                                  freezer,
                                                  dishwasher,
                                                  range,
                                                  oven,
                                                  repair,
                                                  misc,
                                                  tax,
                                                  total,
                                                  date)
                                VALUES(0,0,0,0,0,0,0,0,0,0,0,current_date
                                       );""")
            self.conn.commit()
        for app_id in app:
            self.cur.execute("""SELECT app_type, price
                                FROM appliance
                                WHERE id = (%s);""",(app_id))
            y = self.cur.fetchone()
            app_type = y[0]
            price = y[1]
            ID2 = ID[0]
            self.cur.execute("""SELECT {} FROM money
                                WHERE date = current_date;""".format(app_type))
            instance = self.cur.fetchone()
            number = instance[0]
            if number == 0.0:
                self.cur.execute("""UPDATE money
                                    SET {} = {}::float
                                    WHERE date = current_date;""".format(app_type,
                                                                         price))
                self.conn.commit()
            else:
                self.cur.execute("""UPDATE money
                                    SET {} = {}::float + {}::float
                                    WHERE date = current_date;""".format(
                                                                  app_type,
                                                                  price,
                                                                  number))
                self.conn.commit()
        for app_id in app:
                self.cur.execute("""INSERT INTO sold_appl(sale_id,
                                                          cust_id,
                                                          appl_id,
                                                          date)
                                    VALUES (%s, %s, %s, current_date);""",
                                (ID, x, app_id,))
                self.conn.commit()
        self.cur.execute("""SELECT washer,
                                   dryer,
                                   refrigerator,
                                   freezer,
                                   dishwasher,
                                   range,
                                   oven,
                                   repair,
                                   misc
                                   FROM money WHERE date = current_date;""")
        tpl = self.cur.fetchall()
        tpl = tpl[0]
        total = sum(tpl)
        tax = total * 0.07
        grand_total = total + tax
        self.cur.execute("""UPDATE money SET tax = %s
                            WHERE date = current_date;""", (tax,))
        self.conn.commit()
        self.cur.execute("""UPDATE money SET total = %s
                            WHERE date = current_date;""", (grand_total,))
        self.conn.commit()

        
    def createTable(self):
        """Creates tables appliance, customer, sales, money, and sold_appl"""
##        self.cur.execute("""CREATE EXTENSION pgrouting;""")
##        self.cur.execute("""ALTER TABLE stephens_rd DROP COLUMN source;""")
##        self.cur.execute("""ALTER TABLE public.stephens_rd add column source integer;""")
##        self.cur.execute("""ALTER TABLE public.stephens_rd add column target integer;""")
##        self.cur.execute("""SELECT pgr_createTopology('public.stephens_rd', 0.0001, 'geom', 'id');""")


        self.cur.execute("""CREATE TABLE appliance(id serial,
                                                   app_type varchar,
                                                   brand varchar,
                                                   model varchar,
                                                   price float
                                                   );"""
                         )
        self.conn.commit()
        
        self.cur.execute("""CREATE TABLE customer(id serial,
                                                  name varchar(20),
                                                  phone integer,
                                                  address varchar
                                                  );"""
                         )
        self.conn.commit()

        self.cur.execute("""CREATE TABLE sales(id serial,
                                               cust_id integer,
                                               date date,
                                               delivery_date date,
                                               war_exp date                                          
                                               );"""
                         )
        self.conn.commit()
        self.cur.execute("""CREATE TABLE sold_appl(id serial,
                                                   sale_id integer,
                                                   cust_id integer,
                                                   appl_id integer,
                                                   date date
                                                   );"""
                         )
        self.conn.commit()
        self.cur.execute("""CREATE TABLE money(washer float,
                                               dryer float,
                                               refrigerator float,
                                               freezer float,
                                               dishwasher float,
                                               range float,
                                               oven float,
                                               repair float,
                                               misc float,
                                               tax float,
                                               total float,
                                               date date
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
        self.cur.execute("""DROP TABLE money;""")
        self.conn.commit()
        print("Tables Dropped")


                        



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

    def viewAvailable(self):
        """Selects all available appliances from appliance table"""
        self.cur.execute("""SELECT * FROM appliance
                            WHERE status = 'available';""")
        x = self.cur.fetchall()
        print("ID |Type |Brand |Style |Price")
        for a,b,c,d,e,f,g in x:
            print a,c,d,e,f


    def addAppliance(self, a, b, s, p, r):
        self.cur.execute("""INSERT INTO appliance (status, app_type, brand,
                                                   style, price, repairs)
                            VALUES ('available', %s, %s, %s, %s, %s);""",
                            (a, b, s, p, r,))
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
        self.cur.execute("""SELECT date, app_type, brand, style, price
                            FROM sold_appl NATURAL JOIN appliance
                            WHERE cust_id = (%s);""", (cust_id,))
        List = self.cur.fetchall()
        for tuple in List:
            print ("\n")
            for i in tuple:
                print i             
        
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
            DBOperations().saleTicket2(n, p, app)
        else:
            DBOperations().saleTicket2(n, p, app)
        
    def saleTicket2(self, n, p, app='', tax=0):
        self.cur.execute("""SELECT id FROM customer
                            WHERE name = (%s)
                            AND phone = (%s);""", (n, p,))
        x = self.cur.fetchone()
        self.cur.execute("""INSERT INTO sales (cust_id, date)
                            VALUES (%s, current_date);""", (x,))
        self.conn.commit()
        self.cur.execute("""SELECT MAX(id) FROM sales;""")
        ID = self.cur.fetchone()
        ID = ID[0]
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
            self.cur.execute("""SELECT app_type
                                FROM appliance
                                WHERE id = (%s);""",(app_id,))
            y = self.cur.fetchone()
            app_type = y[0]
            price = float(raw_input("Enter amount recieved for {} ID = {}:".format(app_type, app_id)))
            self.cur.execute("""SELECT {} FROM money
                                WHERE date = current_date;""".format(app_type))
            selection = self.cur.fetchone()
            number = selection[0]
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
                self.cur.execute("""UPDATE appliance SET status = 'sold'
                                    WHERE id = %s;""", (app_id,))
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
##        tax = total * 0.07
##        grand_total = total + tax
        # pull this from sales:
        self.cur.execute("""UPDATE money SET tax = %s
                            WHERE date = current_date;""", (tax,))
        self.conn.commit()
        self.cur.execute("""UPDATE money SET total = %s
                            WHERE date = current_date;""", (total,))
        self.conn.commit()
        self.cur.execute("""UPDATE sales SET delivery_date = current_date
                            WHERE id = %s""", (ID,))
        self.conn.commit()

        self.cur.execute("""UPDATE sales SET war_exp = current_date + 365
                            WHERE id = %s""", (ID,))
        self.conn.commit()
        

    def serviceCalls(self, app_id):
        self.cur.execute("""SELECT sale_id FROM sold_appl NATURAL JOIN appliance
                            WHERE appl_id = (%s);""", (app_id,))
        sale_id = self.cur.fetchone()
        service = raw_input("Repaires made:")
        self.cur.execute("""INSERT INTO service_calls(sale_id, appl_id, repair, date)
                            VALUES(%s, %s, %s, current_date);""", (sale_id, app_id, service,))
        self.conn.commit()

    def viewService(self):
        self.cur.execute("""SELECT * FROM service_calls NATURAL JOIN sales NATURAL JOIN customer;""")
        results = self.cur.fetchall()
        print("SaleID|APPLID|Action|WARexp|Name|Phone|Address")
        for a,b,c,d,e,f,g,h,i,j,k in results:
            print c,d,e,h,i,j,k

    def viewRoute(self):
        """http://anitagraser.com/2013/07/06/pgrouting-2-0-for-windows-quick-guide/"""
        self.cur.execute("""SELECT seq, id1 AS node, id2 AS edge, cost, geom INTO newtable
                             FROM pgr_dijkstra(
                             'SELECT id, source, target, st_length(geom) as cost FROM public.scrouting',
                             1, 500, false, false
                             ) as di
                             JOIN public.scrouting pt
                             ON di.id2 = pt.id""")


        
    def createTable(self):
        """Creates tables appliance, customer, sales, money, and sold_appl"""
##        self.cur.execute("""CREATE EXTENSION pgrouting;""")
##        self.cur.execute("""ALTER TABLE scrouting DROP COLUMN source;""")
##        self.cur.execute("""ALTER TABLE scrouting add column source integer;""")
##        self.cur.execute("""ALTER TABLE scrouting add column target integer;""")
##        self.cur.execute("""select pgr_createTopology('network.publictransport', 0.0005, 'geom', 'id');""")

        # self.cur.execute("""SELECT seq, id1 AS node, id2 AS edge, cost, geom INTO newtable
        #                      FROM pgr_dijkstra(
        #                      'SELECT id, source, target, st_length(geom) as cost FROM public.scrouting',
        #                      1, 500, false, false
        #                      ) as di
        #                      JOIN public.scrouting pt
        #                      ON di.id2 = pt.id""")


        self.cur.execute("""CREATE TABLE appliance(id serial,
                                                   status varchar,
                                                   app_type varchar,
                                                   brand varchar,
                                                   style varchar,
                                                   price float,
                                                   repairs varchar
                                                   );"""
                         )
        self.conn.commit()
        
        self.cur.execute("""CREATE TABLE customer(id serial,
                                                  name varchar(20),
                                                  phone bigint,
                                                  address varchar
                                                  );"""
                         )
        self.conn.commit()
        # need total/tax and total+tax column of recieved per sale
        self.cur.execute("""CREATE TABLE sales(id serial,
                                               cust_id integer,
                                               total float,
                                               tax float,
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

        self.cur.execute("""CREATE TABLE service_calls(id serial,
                                                       sale_id integer,
                                                       appl_id integer,
                                                       repair varchar,
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


                        



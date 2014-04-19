"""
Database Module
Nathan Walker
nwalk19@gmail.com
"""

import psycopg2

class DBConnect():
    """Creates a database connection and a cursor"""
    def __init__(self):
        self.conn = psycopg2.connect("dbname=DbProject user=postgres host=localhost password=postgres")
        self.cur = self.conn.cursor()
        self.conn.commit()
        print("Connected")

class DBOperations(DBConnect):
    """This class performs all the operations
       needed to work with the database"""

    def createTable(self):
        """Creates tables appliance, customer, sales, and sold_appl"""
        self.cur.execute("""CREATE TABLE appliance(id serial,
                                                   type varchar,
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
                         
                        



from Database import DBOperations
import re

class Menu():
    """Displays a menu and respond to choices when run."""
    def __init__(self):
        self.DB = DBOperations()
        self.choices = {
                1: self.create,
                2: self.drop,
                3: self.add_a,
                4: self.sale,
                5: self.search,
                6: self.available,
                7: self.service,
                8: self.view_serv
                }

    def display_menu(self):
        print("""
Used Appliance:
                   MAIN MENU

1 - Add Table      6 - View Available
2 - Drop Tables    7 - Service Calls
3 - Add Appliance  8 - View Service Calls
4 - Sale
5 - Search
""")

    def run(self):
        """Display the menu and respond to choices."""
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{} is not a valid choice".format(choice))

    def available(self):
        self.DB.viewAvailable()

    def create(self):
        self.DB.createTable()

    def drop(self):
        self.DB.dropTables()

    def view_serv(self):
        self.DB.viewService()

    def add_a(self):
        a = raw_input("Appliance Type:")
        b = raw_input("Brand:")
        s = raw_input("Style:")
        p = float(raw_input("Price:"))
        r = raw_input("Repairs made:")
        self.DB.addAppliance(a, b, s, p, r)

    def sale(self):
        n = raw_input("Name:")
        p = raw_input("Phone:")
        a = raw_input("Address:")
        app = raw_input("Appliance ID(s):")
        app = re.findall(r"[-+]?\d*\.\d+|\d+", app)
        print app
        self.DB.saleTicket1(n, p, a, app)

    def service(self):
        app_id = raw_input("Appliance ID:")
        self.DB.serviceCalls(app_id)
        
        
        
        
    def search(self):
        print("""
SEARCH MENU
1 - Search By Name
2 - Search By Phone
b - Back
          """)
        x = raw_input("Make a selection:")
        if x == '1':
            n = raw_input("Name:")
            self.DB.searchName(n)
        elif x == '2':
            p = raw_input("Phone Number:")
            self.DB.searchPhone(p)
        elif x == 'b':
            Menu().run()
            
        
        
        



if __name__ == "__main__":
    Menu().run()

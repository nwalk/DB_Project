from database import DBOperations
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
                5: self.search
##                6: self.,
##                7: self.,
##                8: self.quit,
                }

    def display_menu(self):
        print("""
Used Appliance:
                   MAIN MENU

1 - Add Table
2 - Drop Tables
3 - Add Appliance
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

    def create(self):
        self.DB.createTable()

    def drop(self):
        self.DB.dropTables()

    def add_a(self):
        a = raw_input("Appliance Type:")
        b = raw_input("Brand:")
        m = raw_input("Model:")
        p = float(raw_input("Price:"))
        self.DB.addAppliance(a, b, m, p)

    def sale(self):
        n = raw_input("Name:")
        p = raw_input("Phone:")
        a = raw_input("Address:")
        app = raw_input("Appliance ID(s):")
        app = re.findall(r"[-+]?\d*\.\d+|\d+", app)
        print app
        self.DB.saleTicket1(n, p, a, app)
        
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

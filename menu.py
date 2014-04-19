from database import DBOperations


class Menu():
    """Displays a menu and respond to choices when run."""
    def __init__(self):
        self.DB = DBOperations()
        self.choices = {
                1: self.create,
                2: self.drop,
                3: self.add_a,
                4: self.add_c,
                5: self.sold
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
4 - Add Customer
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

    def add_c(self):
        n = raw_input("Name:")
        p = raw_input("Phone:")
        a = raw_input("Address:")
        self.DB.findCustomer(n, p)
        self.DB.addCustomer(n, p, a)
        self.DB.saleTicket(n, p)

    def sold(self):
        
        self.DB.saleTicket()
        
        
        



if __name__ == "__main__":
    Menu().run()

from database import DBOperations


class Menu():
    """Displays a menu and respond to choices when run."""
    def __init__(self):
        self.SQL = DBOperations()
        self.choices = {
                1: self.create,
                2: self.drop,
##                3: self.,
##                4: self.,
##                5: self.,
##                6: self.,
##                7: self.,
##                8: self.quit,

    def display_menu(self):
        print("""
Used Appliance:
                   MAIN MENU

1 - Add Table
2 - Drop Tables
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
        self.SQL.createTable()

    def drop(self):
        self.SQL.dropTables()
        
        
        



if __name__ == "__main__":
    Menu().run()

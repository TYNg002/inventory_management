# import tabulate module to allow presentation of information in tables
from tabulate import tabulate

#========The beginning of the class==========

# define Shoe class
class Shoe:

    # initiates class
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
    # returns item cost
    def get_cost(self):
        return int(self.cost)

    # returns stock quantity
    def get_quantity(self):
        return int(self.quantity)

    # returns string representation of class
    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"

#==========Functions outside the class==============

# get all information from inventory.txt and add to shoe list
# show error message if file not found
def read_shoes_data():
    try:
        with open("inventory.txt", "r", encoding="UTF-8") as inventory:
            # each line in inventory.txt states country, code, product, cost, and quantity in this order
            inventory_lines = inventory.readlines()
            for line in inventory_lines:
                # skip first line of inventory.txt
                if line == inventory_lines[0]:
                    continue
                line = line.strip("\n").split(",")
                shoe = Shoe(line[0], line[1], line[2], line[3], line[4])
                shoe_list.append(shoe)
    except FileNotFoundError:
        print("Inventory file was not found; terminating program.")
        exit()

# asks for information for new Shoe object and appends object to shoe_list
def capture_shoes():
    while True:
        # try/except to ensure numbers are entered for quantity and cost
        try:
            shoe_country = input("Country: ")
            shoe_code = input("Code: ")
            shoe_product = input("Product: ")
            shoe_quantity = int(input("Quantity: "))
            shoe_cost = int(input("Cost: "))
            # print error message if any fields are left blank
            if shoe_country == "" or shoe_code  == "" or shoe_product == "" or shoe_quantity == "" or shoe_cost == "":
                print("No input detected in one or more fields. Please try again.")
            else:
                break
        except ValueError:
            print("Please enter a number for both quantity and cost.")
    # create Shoe object and append to shoe list
    new_shoe = Shoe(shoe_country, shoe_code, shoe_product, shoe_quantity, shoe_cost)
    shoe_list.append(new_shoe)

# shows all shoe data in table form
def view_all():
    # create list for storing shoe information obtained from objects in shoe_list
    shoe_table = []
    for shoe in shoe_list:
        shoe_info = str(shoe).split(",")
        shoe_table.append(shoe_info)
    print(tabulate(shoe_table, headers = header.strip("\n").split(",")))

# shows the shoe with lowest stock level and increases stock level if prompted
def re_stock():
    # variable to keep track of list index
    shoe_index = -1
    for shoe in shoe_list:
        shoe_index += 1
        # get quantity value of shoe
        quantity_current = shoe.get_quantity()
        # for first item, set lowest quantity to quantity of first item
        if shoe_index == 0:
            quantity_lowest =  shoe.get_quantity()
        # set lowest quantity to be the same as the current quantity if current quantity is lower than lowest quantity variable
        if quantity_current < quantity_lowest:
            quantity_lowest = quantity_current
            # set variable to identify index number of lowest quantity item
            quantity_lowest_index = shoe_index
    
    # get the name of the product with the lowest quantity and present name 
    # and quantity to user
    quantity_lowest_name = shoe_list[quantity_lowest_index].product
    print(f"The item with the lowest stock level is {quantity_lowest_name} with "
          f"a stock level of {quantity_lowest}.\n")
    
    # ask if user would like to increase stock level of item
    while True:
        restock = input("Would you like to increase the stock level of this "
                        "item? (Y/N) ")
        
        # return to menu if user does not wish to increase stock
        if restock.lower() == "n":
            return
        
        # ask for restock amount if user wishes to increase stock, and add to 
        # existing stock number
        if restock.lower() == "y":
            while True:
                try:
                    restock_amount = int(
                        input("\nHow much would you like to increase the stock "
                              "by? Please enter an integer: "))
                    break
                except ValueError:
                    print("\nNumerical input required. Please try again.")
            shoe_list[quantity_lowest_index].quantity = int(
                shoe_list[quantity_lowest_index].quantity) + restock_amount
            print(f"\n{quantity_lowest_name} now has a stock level of "
                  f"{shoe_list[quantity_lowest_index].quantity}.")
            
            # write new stock info to file
            with open("inventory.txt", "w", encoding="UTF-8") as inventory:
                # include header in inventory file
                inventory.write(header)
                # populate new info into file
                for item in shoe_list:
                    inventory.write(f"{str(item)}\n")
            return
        
        else:
            print("Input not recognised. Please try again.")

# search for a shoe using the code and print the related shoe information
def search_shoe():
    while True:
        shoe_code = input("Enter the product code: ")
        print("")
        for shoe in shoe_list:
            # for each shoe in the list, if the input matches a code, print out 
            # relevant information
            # use strip and split functions to enable display of information 
            # using tabulate
            if shoe.code == shoe_code:
                shoe_search = [str(shoe).split(",")]
                print(tabulate(shoe_search, headers = header.strip("\n").split(",")))
                return
        else:
            print("Product code not found. Please try again.\n")

# calculate total value of each item and prints in table format
def value_per_item():
    value_table = []
    for shoe in shoe_list:
        # get existing shoe information in list form
        shoe_info = str(shoe).split(",")
        # get value of shoe and append to info list
        value = shoe.get_cost() * shoe.get_quantity()
        shoe_info.append(value)
        # add shoe info with value included into value table
        value_table.append(shoe_info)
    # modify header to include 'value' column and be used with tabulate
    value_header = header.strip("\n").split(",")
    value_header.append("Value")
    print(tabulate(value_table, headers = value_header))

# finds shoe with the highest stock level and show as being on sale
def highest_qty():
    # variable to keep track of list index
    shoe_index = -1
    for shoe in shoe_list:
        shoe_index += 1
        # get quantity value of shoe
        quantity_current = shoe.get_quantity()
        # for first item, set highest quantity to quantity of first item
        if shoe_index == 0:
            quantity_highest = shoe.get_quantity()
        # set lowest quantity to be the same as the current quantity if current 
        # quantity is lower than lowest quantity variable
        if quantity_current > quantity_highest:
            quantity_highest = quantity_current
            # set variable to identify index number of lowest quantity item
            quantity_highest_index = shoe_index
    
    # get the name of the product with the lowest quantity and present name and 
    # quantity to user
    quantity_highest_name = shoe_list[quantity_highest_index].product
    print(f"{quantity_highest_name} is currently on sale with {quantity_highest} "
          "in stock.")

#==========Main Menu=============

# the list will be used to store a list of shoes as objects
shoe_list = []

# populate shoe list
read_shoes_data()

# define header variable for use in various functions
with open("inventory.txt", "r", encoding="UTF-8") as inventory:
    for line in inventory:
        header = line
        break

menu = ""
print("Welcome to the shoe inventory.")

# present menu with options for user and call relevant functions based on input
# stop presenting when user chooses to exit program
while menu != "exit":
    menu = input("""\nChoose from one of the following options:
All     -   See all shoes information
New     -   Add information on new shoe
Restock -   Increase stock level of shoe with lowest quantity
Search  -   Search for shoe by code
Value   -   See total value of each shoe type
Sale    -   See which shoe is currently on sale
Exit    -   Exit the program
: """).lower()
    print("")
    
    if menu == "all":
        view_all()

    elif menu == "new":
        capture_shoes()

    elif menu == "restock":
        re_stock()

    elif menu == "search":
        search_shoe()

    elif menu == "value":
        value_per_item()
        
    elif menu == "sale":
        highest_qty()

    elif menu == "exit":
        print("Program terminated.")
        exit()

    else:
        print("Input not recognised. Please try again.\n")
# Capstone Project Object-Oriented Programming(OOP)
'''Code a Python program that will read from the text file inventory.txt and
perform the following tasks on the data, to prepare for presentation to managers:
Tasks involved:
Shoe class creation
With functions to return cost, quatity of sheos, and return strong represenation of class.
With function to read the data, capture data about a shoe, locate the lowest quantity, highest quantity, search shoes, show the values.

'''
from tabulate import tabulate

# Class Shoes with attributes included in inventory file
class Shoes:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

# This function is used in def value_per_item() to calcuate the value per item
    def get_cost(self):
        return self.cost

# This function is used in def value_per_item() to calcuate the value per item
    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.code} - {self.product} ({self.quantity} in stock)"

# Outside this class create a variable with an empty list. This variable will be used to store a list of shoes objects
shoes_list = []

# Function to read the data from inventory file, it is run at the beginning of main()
def read_shoes_data():
    try:
        with open("inventory.txt", "r") as file:
            # Skip the header line
            next(file)

            for line in file:
                data = line.strip().split(",")
                country, code, product, cost_str, quantity_str = data
                cost = float(cost_str)
                quantity = int(quantity_str)
                shoe = Shoes(country, code, product, cost, quantity)
                shoes_list.append(shoe)
        print("Inventory loaded successfully!")
    except FileNotFoundError:
        print("Could not open file 'inventory.txt'")

# Function to add new shoe to either just saving on the list or saving on both list and file
# I assume that the inventory file already exist, so I didn't make the program to write a new headline when there is no inventory file
def capture_shoes():
    print("Enter details of the new shoe:")
    country = input("Country: ")
    code = input("Code: ")
    product = input("Product: ")
    while True:
        cost = input("Cost: ")
        try:
            cost = float(cost)
            if cost < 0:
                print("Invalid input. Cost should be a non-negative number.")
            else:
                break
        except ValueError:
            print("Invalid input. Cost should be a number.")
    quantity = input("Quantity: ")
    while not quantity.isdigit() or int(quantity) <= 0:
        print("Invalid input. Quantity should be a positive integer.")
        quantity = input("Quantity: ")
    quantity = int(quantity)
    shoe = Shoes(country, code, product, cost, quantity)
    shoes_list.append(shoe)
    print("Shoe added successfully! List updated !(Be aware that the ventory file hasn't been updated yet!)")
    
    # To save it to the inventory file
    save_choice = input("Do you want to save the shoe added to the inventory file? (y/n): ")
    if save_choice.lower() == "y":
        try:
            with open("inventory.txt", "a") as file:
                # write a new line before writing shoe information
                file.write("\n")
                # write shoe information on a new line
                file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")
            print("Shoe added information has been saved to file.")
        except IOError:
            print("Error: Could not write to inventory file.")
    elif save_choice.lower() == "n":
        print("Shoe added information has not been saved to file.")
    else:
        print("Invalid input. Shoe added information has not been saved to file.")

# Function to view all the data in a table with tabulate as requested
def view_all():
    if len(shoes_list) == 0:
        print("No shoes in inventory.")
    else:
        table = []
        for shoe in shoes_list:
            table.append([shoe.code, shoe.product, shoe.cost, shoe.quantity])
        print(tabulate(table, headers=["Code", "Product", "Cost", "Quantity"]))

# Function to seek the item with lowest quantity and modify the quantity
def re_stock():
    if len(shoes_list) == 0:
        print("No shoes in inventory.")
    else:
        lowest_qty = min(shoe.quantity for shoe in shoes_list)
        lowest_qty_shoes = [shoe for shoe in shoes_list if shoe.quantity == lowest_qty]
        print("The shoe with the lowest quantity is:")
        for i, shoe in enumerate(lowest_qty_shoes):
            print(f"\n{i+1}. {shoe}")
        add_qty = input("\nDo you want to add more quantity? (y/n): ")
        while add_qty.lower() not in ["y", "n"]:
            add_qty = input("Invalid input. Do you want to add more quantity? (y/n): ")
        if add_qty.lower() == "y":
            shoe_choice = int(input(f"Select the index of the shoe you want to restock (1-{len(lowest_qty_shoes)}): "))
            if 1 <= shoe_choice <= len(lowest_qty_shoes):
                qty_to_add = int(input("Enter quantity to add: "))
                lowest_qty_shoes[shoe_choice-1].quantity += qty_to_add
                with open("inventory.txt", "w") as file:
                    file.write("Country,Code,Product,Cost,Quantity\n")  # Write header line
                    for shoe in shoes_list:
                        file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
            else:
                print("Invalid shoe choice.")

# Function to search information about the shoe by entering product code
def search_shoe():
    code = input("Enter shoe code to search: ")
    for shoe in shoes_list:
        if shoe.code == code:
            print(shoe)
            return
    print("Shoe not found.")

# Function to show value per item (value = cost * quantity)
def value_per_item():
    if len(shoes_list) == 0:
        print("No shoes in inventory.")
    else:
        table = []
        for shoe in shoes_list:
            cost = shoe.get_cost()
            quantity = shoe.get_quantity()
            value = cost * quantity
            table.append([shoe.code, shoe.product, shoe.cost, shoe.quantity, value])
        print(tabulate(table, headers=["Code", "Product", "Cost", "Quantity", "Value"]))

# Function to find the item on sales/with highest quantity
def highest_qty():
    if len(shoes_list) == 0:
        print("No shoes in inventory.")
    else:
        highest_qty = max(shoe.quantity for shoe in shoes_list)
        highest_qty_shoes = [shoe for shoe in shoes_list if shoe.quantity == highest_qty]
        for shoe in highest_qty_shoes:
            print(f"{shoe.product} is for sale!")

# Main program
def main():
    read_shoes_data()
    while True:
        print("\nMENU") 
        print("1. Add new shoe")
        print("2. View all shoes")
        print("3. Restock shoes")
        print("4. Search for a shoe")
        print("5. Value per item")
        print("6. Highest quantity shoe")
        print("7. Quit")

        choice = input("Enter your choice: ")
        if choice == "1":
            capture_shoes()
        elif choice == "2":
            view_all()
        elif choice == "3":
            re_stock()
        elif choice == "4":
            search_shoe()
        elif choice == "5":
            value_per_item()
        elif choice == "6":
            highest_qty()
        elif choice == "7":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
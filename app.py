import os
import csv
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Constants for file names
FILE_USERS = "users.csv"
FILE_BRANCHES = "branches.csv"
FILE_PRODUCTS = "products.csv"
FILE_SALES = "sales.csv"

########## Factory Pattern ##########

# Interface for data loaders
class DataLoader:
    def load_data(self):
        raise NotImplementedError

# CSV loader implementation
class CSVLoader(DataLoader):
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_data(self):
        data = []
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    data.append(row)
        return data

# Factory to create loaders
class DataLoaderFactory:
    @staticmethod
    def create_loader(file_path):
        if file_path.endswith('users.csv'):
            return CSVLoader(file_path)
        elif file_path.endswith('branches.csv'):
            return CSVLoader(file_path)
        elif file_path.endswith('products.csv'):
            return CSVLoader(file_path)
        elif file_path.endswith('sales.csv'):
            return CSVLoader(file_path)
        else:
            raise ValueError("Unsupported file type")

########## Command Pattern ##########

# Base command interface
class Action:
    def execute(self):
        raise NotImplementedError

# Concrete action to add a new branch
class AddBranchAction(Action):
    def execute(self):
        print("\n!!!!! Add New Branch !!!!!")
        branch_data = load_data(FILE_BRANCHES)
        
        branch_id = input("Enter Branch ID: ")
        branch_name = input("Enter Branch Name: ")
        branch_location = input("Enter Location: ")

        new_branch = [branch_id, branch_name, branch_location]
        branch_data.append(new_branch)

        os.remove(FILE_BRANCHES)

        headers = ['Branch ID', 'Branch Name', 'Location']
        save_data(FILE_BRANCHES, branch_data, headers=headers)
        print(f"Branch {branch_name} added successfully.")

# Concrete action to add a new sale
class AddSaleAction(Action):
    def execute(self):
        print("\n!!!!! Add New Sale !!!!!")
        sale_data = load_data(FILE_SALES)
        
        branch_id = input("Enter Branch ID: ")
        product_id = input("Enter Product ID: ")
        amount_sold = input("Enter Amount Sold: ")

        new_sale = [branch_id, product_id, amount_sold, datetime.now().strftime('%Y-%m-%d')]
        sale_data.append(new_sale)

        os.remove(FILE_SALES)

        headers = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
        save_data(FILE_SALES, sale_data, headers=headers)
        print("Sale added successfully.")

# Concrete action for monthly sales analysis of a specific branch
class BranchMonthlySalesAnalysisAction(Action):
    def __init__(self, branch_id):
        self.branch_id = branch_id
    
    def execute(self):
        monthly_sales_analysis(self.branch_id)

# Concrete action for price analysis of a specific product
class ProductPriceAnalysisAction(Action):
    def __init__(self, product_id):
        self.product_id = product_id
    
    def execute(self):
        price_analysis(self.product_id)

# Concrete action for weekly sales analysis of the supermarket network
class SupermarketWeeklySalesAnalysisAction(Action):
    def execute(self):
        weekly_sales_analysis()

# Concrete action for total sales amount analysis
class TotalSalesAmountAnalysisAction(Action):
    def execute(self):
        total_sales_amount_analysis()

# Concrete action for monthly sales analysis of all branches
class AllBranchesMonthlySalesAnalysisAction(Action):
    def execute(self):
        all_branches_monthly_sales_analysis()

########## Utility Functions ##########

# Function to load data from CSV file
def load_data(file_path):
    loader = DataLoaderFactory.create_loader(file_path)
    return loader.load_data()

# Function to save data to CSV file
def save_data(file_path, data, headers=None):
    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists and headers:
            writer.writerow(headers)
        writer.writerows(data)

# Function for user login
def login():
    print("!!!!! Login !!!!!")
    username = input("Enter username: ")
    password = input("Enter password: ")
    with open(FILE_USERS, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

# Function for monthly sales analysis of a specific branch
def monthly_sales_analysis(branch_id):
    print(f"\n!!!!! Monthly Sales Analysis - Branch {branch_id} !!!!!")
    sales_data = load_data(FILE_SALES)
    branch_sales_amounts = [int(sale[2]) for sale in sales_data if sale[0] == branch_id]

    if not branch_sales_amounts:
        print(f"No sales details found for Branch ID {branch_id}.")
        return

    plt.figure(figsize=(8, 5))
    plt.hist(branch_sales_amounts, bins=10, edgecolor='black')
    plt.title(f'Monthly Sales Analysis - Branch {branch_id}')
    plt.xlabel('Sales Amount (LKR)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Function for price analysis of a specific product
def price_analysis(product_id):
    print(f"\n!!!!! Price Analysis - Product {product_id} !!!!!")
    sales_data = load_data(FILE_SALES)
    product_sales_amounts = [int(sale[2]) for sale in sales_data if sale[1] == product_id]

    if not product_sales_amounts:
        print(f"No sales details found for Product ID {product_id}.")
        return

    avg_price = np.mean(product_sales_amounts)
    maximum_price = np.max(product_sales_amounts)
    minimum_price = np.min(product_sales_amounts)
    median_price = np.median(product_sales_amounts)

    print(f"Average Price: {avg_price} LKR")
    print(f"Maximum Price: {maximum_price} LKR")
    print(f"Minimum Price: {minimum_price} LKR")
    print(f"Median Price: {median_price} LKR")

    # Plotting boxplot for price distribution
    plt.figure(figsize=(8, 5))
    plt.boxplot(product_sales_amounts, vert=False)
    plt.title(f'Price Distribution - Product {product_id}')
    plt.xlabel('Sales Amount (LKR)')
    plt.grid(True)
    plt.show()

# Function for weekly sales analysis of the supermarket network
def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d'):  # Added '%Y/%m/%d' format
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"time data '{date_str}' does not match any known format")



def weekly_sales_analysis():
    print("\n!!!!! Weekly Sales Analysis - Supermarket Network !!!!!")
    sales_data = load_data(FILE_SALES)

    # Example: Analyze sales for the current week
    current_day = datetime.today()
    start_week = current_day - timedelta(days=current_day.weekday())
    end_week = start_week + timedelta(days=6)

    weekly_sales_amounts = [int(sale[2]) for sale in sales_data
                            if start_week <= parse_date(sale[3]) <= end_week]

    total_sales = sum(weekly_sales_amounts)
    average_sales = np.mean(weekly_sales_amounts) if weekly_sales_amounts else 0

    print(f"Total Sales for the Week: {total_sales} LKR")
    print(f"Average Daily Sales: {average_sales} LKR")

# Function for total sales amount analysis
def total_sales_amount_analysis():
    print("\n!!!!! Total Of Sales Amount Analysis !!!!!")
    sales_data = load_data(FILE_SALES)
    total_sales = sum([int(sale[2]) for sale in sales_data])

    print(f"Total Sales Amount: {total_sales} LKR")

# Function for monthly sales analysis of all branches
def all_branches_monthly_sales_analysis():
    print("\n!!!!! Monthly Sales Analysis of All Branches !!!!!")
    sales_data = load_data(FILE_SALES)
    branches_data = load_data(FILE_BRANCHES)
    
    monthly_sales = {branch[0]: 0 for branch in branches_data}
    
    for sale in sales_data:
        branch_id = sale[0]
        monthly_sales[branch_id] += int(sale[2])
    
    
    branch_ids, sales_amounts = zip(*monthly_sales.items())
    
    plt.figure(figsize=(10, 6))
    plt.bar(branch_ids, sales_amounts)
    plt.title('Monthly Sales Analysis of All Branches')
    plt.xlabel('Branch ID')
    plt.ylabel('Total Sales Amount(LKR)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

########## Main Program ##########

# Main program loop with action execution
def main():
    # Ensure CSV files exist with headers
    headers_users = ['Username', 'Password']
    if not os.path.exists(FILE_USERS):
        save_data(FILE_USERS, [], headers=headers_users)

    headers_branches = ['Branch ID', 'Branch Name', 'Location']
    if not os.path.exists(FILE_BRANCHES):
        save_data(FILE_BRANCHES, [], headers=headers_branches)

    headers_products = ['Product ID', 'Product Name']
    if not os.path.exists(FILE_PRODUCTS):
        save_data(FILE_PRODUCTS, [], headers=headers_products)

    headers_sales = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
    if not os.path.exists(FILE_SALES):
        save_data(FILE_SALES, [], headers=headers_sales)

    # Login loop
    while True:
        if login():
            print("Login successful!")
            break
        else:
            print(".")

    # Action map
    actions = {
        '1': AddBranchAction,
        '2': AddSaleAction,
        '3': BranchMonthlySalesAnalysisAction,
        '4': ProductPriceAnalysisAction,
        '5': SupermarketWeeklySalesAnalysisAction,
        '6': TotalSalesAmountAnalysisAction,
        '7': AllBranchesMonthlySalesAnalysisAction,
        '8': lambda: print("Logged out!")
    }

    # Main menu
    while True:
        print("\n!!!!! Welcome to Main Menu !!!!!")
        print("1. Add a New Branch")
        print("2. Add a New Sale")
        print("3. Specific Branch's Monthly Sales Analysis")
        print("4. Price Analysis of a Specific Product")
        print("5. Supermarket Network's Weekly Sales Analysis")
        print("6. Analysis of Total Sales Amounts")
        print("7. All Branches' Monthly Sales Analysis")
        print("8. Log out")

        selection = input("Enter your Selection (1-8): ")

        if selection in actions:
            if selection == '8':
                actions[selection]()  # Log out directly
                break
            else:
                if selection in ['3', '4']:
                    param = input(f"Enter {'Branch ID' if selection == '3' else 'Product ID'}: ")
                    action = actions[selection](param)
                else:
                    action = actions[selection]()
                action.execute()
        else:
            print("Invalid Selection. Please enter a number between 1 and 8.")

# Execute the main program
main()

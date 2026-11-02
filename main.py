import json
import os
from datetime import datetime

# ==========================================
# 1. LOAD OR CREATE INVENTORY
# ==========================================

DATA_FILE = "inventory_data.json"
SALES_FILE = "sales_history.json"

def load_inventory():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                products = json.load(file)

            for product in products:
                if product["name"].lower() == "chicken":
                    product["cost_price"] = 3000

                elif product["name"].lower() == "rice":
                    product["cost_price"] = 1500

                elif product["name"].lower() == "fish":
                    product["cost_price"] = 500

            return products

        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read inventory file.")

    return [
        {"name": "Chicken", "quantity": 25, "price": 5000, "cost_price": 3000},
        {"name": "Rice", "quantity": 20, "price": 3000, "cost_price": 1500},
        {"name": "Fish", "quantity": 8, "price": 2500, "cost_price": 500}
    ]


def load_sales():
    if os.path.exists(SALES_FILE):
        try:
            with open(SALES_FILE, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read sales history.")
            return []

    return []

def save_sales():
    with open(SALES_FILE, "w") as file:
        json.dump(sales, file, indent=4)
        
products = load_inventory()
sales = load_sales()



def total_revenue():
    revenue = 0

    for sale in sales:
        revenue += sale["amount"]

    print("\n======= SALES SUMMARY =======")
    print(f"Total sales transactions: {len(sales)}")
    print(f"Total revenue: ₦{revenue:,.2f}")



def total_profit():
    profit = 0

    for sale in sales:
        profit += sale.get("profit", 0)

    print("\n======= PROFIT SUMMARY =======")
    print(f"Total gross profit: ₦{profit:,.2f}")



def view_sales_history():
    print("\n======= SALES HISTORY =======")

    if not sales:
        print("No sales have been recorded yet.")
        return

    for index, sale in enumerate(sales, start=1):
        print(f"\nSale {index}")
        print(f"Product: {sale['product']}")
        print(f"Quantity: {sale['quantity']}")
        print(f"Amount: ₦{sale['amount']:,.2f}")
        print(f"Date: {sale['date']}")
        print("-" * 30)

    print("\n======= END OF SALES HISTORY =======")

def total_quantity_sold():
    total_quantity = 0

    for sale in sales:
        total_quantity += sale["quantity"]

    print("\n======= QUANTITY SOLD =======")
    print(f"Total quantity sold: {total_quantity}")


def best_selling_product():
    if not sales:
        print("No sales recorded yet.")
        return

    product_sales = {}

    for sale in sales:
        product = sale["product"]
        quantity = sale["quantity"]

        if product in product_sales:
            product_sales[product] += quantity
        else:
            product_sales[product] = quantity

    best_product = max(product_sales, key=product_sales.get)

    print("\n======= BEST-SELLING PRODUCT =======")
    print(f"Product: {best_product}")
    print(f"Quantity sold: {product_sales[best_product]}")


def product_profit_report():
    product_data = {}

    for sale in sales:
        product = sale["product"]

        if product not in product_data:
            product_data[product] = {
                "revenue": 0,
                "profit": 0,
                "quantity": 0
            }

        product_data[product]["revenue"] += sale["amount"]
        product_data[product]["profit"] += sale.get("profit", 0)
        product_data[product]["quantity"] += sale["quantity"]

    print("\n======= PRODUCT PROFIT BREAKDOWN =======")

    for product, data in product_data.items():
        print(f"\nProduct: {product}")
        print(f"Quantity sold: {data['quantity']}")
        print(f"Revenue: ₦{data['revenue']:,.2f}")
        print(f"Recorded gross profit: ₦{data['profit']:,.2f}")
        print("-" * 35)


def sales_report():
    print("\n========== SALES REPORT ==========")

    total_revenue()
    total_profit()
    total_quantity_sold()
    best_selling_product()
    

    print("\n======= END OF SALES REPORT =======")


# ==========================================
# 2. SAVE INVENTORY
# ==========================================

def save_inventory():
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(products, file, indent=4)

        print("Inventory saved successfully!")

    except OSError:
        print("Error: Could not save inventory.")


# Create the data file if it does not exist
if not os.path.exists(DATA_FILE):
    save_inventory()


# ==========================================
# 3. VIEW INVENTORY
# ==========================================

def view_inventory():
    print("\n========== INVENTORY ==========")

    if not products:
        print("Your inventory is empty.")
        return

    for product in products:
        print(f"\nProduct: {product['name']}")
        print(f"Quantity: {product['quantity']}")
        print(f"Price per item: ₦{product['price']:,.2f}")
        print("-" * 30)


# ==========================================
# 4. ADD PRODUCT
# ==========================================

def add_product():
    name = input("Enter product name: ").strip()

    if not name:
        print("Product name cannot be empty!")
        return

    for product in products:
        if product["name"].lower() == name.lower():
            print("Product already exists!")
            return

    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter selling price: "))
        cost_price = float(input("Enter cost price: "))

        if quantity < 0 or price < 0 or cost_price < 0:
            print("Quantity and price cannot be negative!")
            return

    except ValueError:
        print("Please enter valid numbers for quantity and price.")
        return

    products.append({
        "name": name,
        "quantity": quantity,
        "price": price,
        "cost_price": cost_price
})

    save_inventory()
    print(f"{name} added successfully!")


# ==========================================
# 5. UPDATE PRODUCT
# ==========================================

def update_product():
    name = input("Enter product to update: ").strip()

    for product in products:
        if product["name"].lower() == name.lower():

            try:
                quantity = int(input("Enter new quantity: "))
                price = float(input("Enter new price: "))

                if quantity < 0 or price < 0:
                    print("Quantity and price cannot be negative!")
                    return

            except ValueError:
                print("Please enter valid numbers.")
                return

            product["quantity"] = quantity
            product["price"] = price

            save_inventory()
            print("Product updated successfully!")
            return

    print("Product not found!")


# ==========================================
# 6. REMOVE PRODUCT
# ==========================================

def remove_product():
    name = input("Enter product to remove: ").strip()

    for product in products:
        if product["name"].lower() == name.lower():
            products.remove(product)

            save_inventory()
            print(f"{name} removed successfully!")
            return

    print("Product not found!")


# ==========================================
# 7. INVENTORY SUMMARY
# ==========================================

def inventory_summary():
    total_quantity = 0
    total_value = 0

    for product in products:
        total_quantity += product["quantity"]
        total_value += product["quantity"] * product["price"]

    print("\n======= INVENTORY SUMMARY =======")
    print(f"Different products: {len(products)}")
    print(f"Total quantity: {total_quantity}")
    print(f"Total inventory value: ₦{total_value:,.2f}")

def low_stock_alert():
    threshold = 10
    found = False

    print("\n======= LOW-STOCK ALERTS =======")

    for product in products:
        if product["quantity"] <= threshold:
            print(
                f"WARNING: {product['name']} has only "
                f"{product['quantity']} units left!"
            )
            found = True

    if not found:
        print("All products have sufficient stock.")


def record_sale():
    product_name = input("Enter product sold: ").strip()

    for product in products:
        if product["name"].lower() == product_name.lower():

            try:
                quantity_sold = int(
                    input("Enter quantity sold: ")
                )
            except ValueError:
                print("Please enter a valid whole number.")
                return

            if quantity_sold <= 0:
                print("Quantity sold must be greater than zero.")
                return

            if quantity_sold > product["quantity"]:
                print("Error: Not enough stock available!")
                return

            total_sale = quantity_sold * product["price"]
            total_cost = quantity_sold * product["cost_price"]
            profit = total_sale - total_cost
           
            sale_record = {
                "product": product["name"],
                "quantity": quantity_sold,
                "amount": total_sale,
                "cost": total_cost,
                "profit": profit,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

            sales.append(sale_record)

            save_sales()

            product["quantity"] -= quantity_sold

            save_inventory()

            print("\nSale recorded successfully!")
            print(f"Total sale amount: ₦{total_sale:,.2f}")
            print(f"Total cost: ₦{total_cost:,.2f}")
            print(f"Profit made: ₦{profit:,.2f}")
            print(
            f"{product['name']} remaining: "
            f"{product['quantity']}"
            )

            if product["quantity"] <= 10:
                print("WARNING: This product is running low!")

            return

    print("Product not found!")
# ==========================================
# 8. GENERATE INVENTORY REPORT
# ==========================================

def generate_report():
    total_quantity = 0
    total_value = 0

    try:
        with open("inventory_report.txt", "w") as file:

            file.write("===== RESTAURANT INVENTORY REPORT =====\n\n")

            for product in products:
                quantity = product["quantity"]
                price = product["price"]
                value = quantity * price

                total_quantity += quantity
                total_value += value

                file.write(f"Product: {product['name']}\n")
                file.write(f"Quantity: {quantity}\n")
                file.write(f"Price per item: ₦{price:,.2f}\n")
                file.write(f"Stock value: ₦{value:,.2f}\n")
                file.write("-" * 30 + "\n")

            file.write("\n======= SUMMARY =======\n")
            file.write(f"Different products: {len(products)}\n")
            file.write(f"Total quantity: {total_quantity}\n")
            file.write(f"Total inventory value: ₦{total_value:,.2f}\n")

        print("Inventory report generated successfully!")
        print("Saved as inventory_report.txt")

    except OSError:
        print("Error: Could not create the inventory report.")


# ==========================================
# 9. MAIN MENU
# ==========================================

def main():
    while True:
        print("\n================================")
        print(" RESTAURANT INVENTORY SYSTEM")
        print("================================")
        print("1. View inventory")
        print("2. Add product")
        print("3. Update product")
        print("4. Remove product")
        print("5. View inventory summary")
        print("6. Generate inventory report")
        print("7. Check low-stock alerts")
        print("8. Record a sale")
        print("9. View total revenue")
        print("10. View total gross profit")
        print("11. View product profit breakdown")
        print("12. View sales history")
        print("13. View complete sales report")
        print("14. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_inventory()

        elif choice == "2":
            add_product()

        elif choice == "3":
            update_product()

        elif choice == "4":
            remove_product()

        elif choice == "5":
            inventory_summary()

        elif choice == "6":
            generate_report()
        
        elif choice == "7":
            low_stock_alert()

        elif choice == "8":
            record_sale()

        elif choice == "9":
            total_revenue()
         
        elif choice == "10":
             total_profit()
         
        elif choice == "11":
            product_profit_report()

        elif choice == "12":
            view_sales_history()

        elif choice == "13":
            sales_report()

        elif choice == "14":
            print("Thank you for using the inventory system!")
            break

# ==========================================
# 10. RUN THE PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
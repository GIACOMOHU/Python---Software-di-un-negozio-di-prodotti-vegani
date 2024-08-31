# importiamo i moduli e le funzioni necessarie

import os
from tabulate import tabulate





PRODUCTS_FILE = "products.txt"
SALES_FILE = "sales.txt"

# definiamo le funzioni necessarie

def load_products():
    """
    Load product information from a file and return it as a dictionary.
    The function reads product data from a file, if it exists, and stores
    it in a dictionary with the product name as the key.
    """

    products = {}  

    if os.path.exists(PRODUCTS_FILE): 
        with open(PRODUCTS_FILE, "r") as file:  
            for line in file:  
                # Split the line by commas into product attributes
                name, quantity, purchase_price, sale_price = line.strip().split(',')

                # Convert the attributes to the appropriate data types and store in the dictionary
                products[name] = {
                    "quantity": int(quantity),  
                    "purchase_price": float(purchase_price),  
                    "sale_price": float(sale_price)  
                } 
    return products  


            
def save_products(products):
    """
    Save product information to a file.
    The function writes the data from the products dictionary to a file, 
    storing each product's details on a new line.
    """

    with open(PRODUCTS_FILE, "w") as file:  
        for name, data in products.items(): 
            # Write the product details to the file in the format: name,quantity,purchase_price,sale_price
            file.write(f"{name},{data['quantity']},{data['purchase_price']},{data['sale_price']}\n")



def load_sales():
    """
    Load sales data from a file and return it as a list of lists.
    The function reads sales records from a file, if it exists, and stores
    each record as a list of strings in a list.
    """

    sales = [] 

    if os.path.exists(SALES_FILE):  
        with open(SALES_FILE, "r") as file:  
            for line in file:  
                # Strip leading/trailing whitespace and split the line by commas
                # Each record is appended as a list of strings to the sales list
                sales.append(line.strip().split(','))
    return sales  

            

def save_sales(sales):
    """
    Save sales data to a file.
    The function writes each sales record from the sales list to a file,
    with each record on a new line and fields separated by commas.
    """

    with open(SALES_FILE, "w") as file: 
        for sale in sales: 
            # Convert all elements of the sale list to strings
            sale_str = [str(item) for item in sale]

            # Join the string elements with commas and write the record to the file
            file.write(",".join(sale_str) + "\n")

               
    
def validate_quantity(quantity_input):
    """
    Validate the input quantity to ensure it is a positive integer.
    The function attempts to convert the input to an integer and checks if it
    is greater than zero. If the input is valid, it returns the quantity; 
    otherwise, it prints an error message and returns None.
    """

    try:
        quantity = int(quantity_input)
        if quantity <= 0:
            raise ValueError("La quantità non può essere negativa o uguale a 0.")
        return quantity 
    except ValueError:
        print("Errore: La quantità deve essere un numero intero positivo. Inserisci una quantità valida oppure premi invio per tornare al menù iniziale.")
        return None  


    
def validate_price(price_input):
    """
    Validate the input price to ensure it is a non-negative number.
    The function attempts to convert the input to a float and checks if it is 
    not negative. If the input is valid, it returns the price; otherwise, it 
    prints an error message and returns None.
    """

    try:
        price = float(price_input)
        if price < 0:
            raise ValueError("Il prezzo non può essere negativo.")
        return price  
    except ValueError:
        print("Errore: Il prezzo deve essere un numero non negativo. Inserisci un prezzo valido oppure premi invio per tornare al menù iniziale.")
        return None 

    
    
def add_product(products):
    """
    Add a product to the inventory. 
    The function prompts the user for the product's name, quantity, purchase price,
    and sale price, validates these inputs, and then updates or adds the product 
    to the inventory.
    """

    name = input("Nome del prodotto: ").strip()  

    while True:
        quantity_input = input("Quantità: ").strip() 
        if not quantity_input:
            return  
        quantity = validate_quantity(quantity_input) 
        if quantity is not None:
            break  

    if name in products:
        # If the product already exists, update its quantity
        products[name]["quantity"] += quantity
        print(f"AGGIUNTO: {quantity} X {name}")
    else:
        # If the product is new, prompt the user to enter its purchase and sale prices
        while True:
            purchase_price_input = input("Prezzo di acquisto: ").strip()
            if not purchase_price_input:
                return  
            purchase_price = validate_price(purchase_price_input)  
            if purchase_price is not None:
                break  

        while True:
            sale_price_input = input("Prezzo di vendita: ").strip()
            if not sale_price_input:
                return  
            sale_price = validate_price(sale_price_input)  
            if sale_price is not None:
                break  

        # Add the new product to the inventory with the provided details
        products[name] = {
            "quantity": quantity,
            "purchase_price": purchase_price,
            "sale_price": sale_price
        }
        print(f"AGGIUNTO: {quantity} X {name}")

    save_products(products)  


      
def list_products(products):
    """
    List all products in the inventory, excluding those with zero quantity.
    The function creates a table of products that have a positive quantity and
    displays it with headers for product name, quantity, and sale price.
    """

    table = []  

    for name, data in products.items():
        if data['quantity'] > 0:  
            # Add the product details to the table
            table.append([name, data['quantity'], f"€{data['sale_price']:.2f}"])

    headers = ["PRODOTTO", "QUANTITA'", "PREZZO"]  
    # Print the table with headers using the tabulate library
    print(tabulate(table, headers, tablefmt="fancy_grid", stralign="left"))
    
    
    
def register_sale(products, sales):
    """
    Register a sale by prompting the user for product details, updating the inventory,
    and recording the sale. The function handles multiple products in a single sale 
    and validates user inputs.
    """

    sale_items = []  
    total_sale = 0  

    while True:
        name = input("Nome del prodotto: ").strip()  
        if not name:
            return  

        if name not in products:
            # If the product is not in the inventory, display an error
            print(f"Errore: Il prodotto '{name}' non è presente in magazzino.")
            input("Premi Invio per tornare al menù principale.")
            return

        while True:
            quantity_input = input("Quantità: ").strip() 
            if not quantity_input:
                return  
            quantity = validate_quantity(quantity_input) 
            if quantity is not None:
                break  

        if quantity > products[name]["quantity"]:
            # Check if the requested quantity exceeds available stock
            print(f"Errore: Quantità richiesta per '{name}' non disponibile.")
            input("Premi Invio per tornare al menù principale.")
            return

        # Add the item to the sale and update the inventory
        sale_items.append((name, quantity, products[name]["sale_price"]))
        total_sale += quantity * products[name]["sale_price"]
        products[name]["quantity"] -= quantity  # Reduce the stock quantity

        while True:
            another = input("Aggiungere un altro prodotto ? (si/no): ").strip().lower()
            if another in ["si", "no"]:
                break  
            elif not another:
                return 
            else:
                print("Errore: Risposta non valida. Inserisci 'si' o 'no'.")  

        if another == "no":
            break 

   
    print("VENDITA REGISTRATA")
    for name, quantity, price in sale_items:
        print(f"- {quantity} X {name}: €{price:.2f}")
    print(f"Totale: €{total_sale:.2f}")

    save_products(products)  
    sales.append([item for sublist in sale_items for item in sublist])  
    save_sales(sales)  


    
def calculate_profits(sales, products):
    """
    Calculate and display gross and net profits from recorded sales.
    The function iterates through the sales records to compute the gross profit 
    (total revenue) and net profit (revenue minus purchase costs) based on 
    product quantities and prices.
    """

    gross_profit = 0  
    net_profit = 0  

    for sale in sales: 
        # Assuming each sale entry is in the format: product_name, quantity, sale_price
        for i in range(0, len(sale), 3):
            name, quantity, price = sale[i], int(sale[i+1]), float(sale[i+2])
            
            if name in products:
                # Calculate gross profit (total revenue from the sale)
                gross_profit += quantity * price
                
                # Calculate net profit (revenue minus the cost of goods sold)
                net_profit += quantity * (price - products[name]["purchase_price"])
            else:
                print(f"Warning: Product '{name}' not found in inventory.")

    # Print the calculated gross and net profits
    print(f"Profitto: lordo=€{gross_profit:.2f} netto=€{net_profit:.2f}")
    

    
def show_help():
    """
    Show available commands to the user.
    The function prints a list of commands that the user can enter to interact 
    with the inventory management system, providing a brief description of each.
    """
    
    print("I comandi disponibili sono i seguenti:")
    print("● aggiungi: aggiungi un prodotto al magazzino")
    print("● elenca: elenca i prodotti in magazzino")
    print("● vendita: registra una vendita effettuata")
    print("● profitti: mostra i profitti totali")
    print("● aiuto: mostra i possibili comandi")
    print("● chiudi: esci dal programma")

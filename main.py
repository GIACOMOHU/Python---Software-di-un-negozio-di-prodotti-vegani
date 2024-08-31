from utils import load_products,  load_sales,  add_product, list_products, register_sale, calculate_profits, show_help 

def main():
    """
    Main function to run the inventory management system.
    The function loads product and sales data, then enters a loop to prompt the user
    for commands. It executes corresponding functions based on the user's input
    and continues until the user decides to exit the program.
    """
    
    products = load_products()
    sales = load_sales()

    while True:
        command = input("Inserisci un comando: ").strip().lower()

        if command == "aggiungi":
            add_product(products)
        elif command == "elenca":
            list_products(products)
        elif command == "vendita":
            register_sale(products, sales)
        elif command == "profitti":
            calculate_profits(sales, products)
        elif command == "aiuto":
            show_help()
        elif command == "chiudi":
            print("Bye bye")
            break
        else:
            print("Comando non valido")
            show_help()


if __name__ == "__main__":
    main()
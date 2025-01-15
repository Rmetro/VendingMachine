# Define the MetrosVendingMachine class
class MetrosVendingMachine:
    def __init__(self):
        # Initialize products with categories, prices, and stock
        self.products = {
            "Drinks": {
                1: {"name": "Soda", "price": 1.50, "stock": 5},
                2: {"name": "Water", "price": 1.00, "stock": 5},
                3: {"name": "Juice", "price": 2.00, "stock": 5},
                4: {"name": "Tea", "price": 1.80, "stock": 5},
                5: {"name": "Coffee", "price": 2.50, "stock": 5}
            },
            "Snacks": {
                6: {"name": "Chips", "price": 1.00, "stock": 5},
                7: {"name": "Biscuits", "price": 1.50, "stock": 5},
                8: {"name": "Granola Bar", "price": 1.00, "stock": 5}
            },
            "Desserts": {
                9: {"name": "Chocolate Bar", "price": 1.20, "stock": 5},
                10: {"name": "Donuts", "price": 1.50, "stock": 5},
                11: {"name": "Cake", "price": 2.50, "stock": 5},
                12: {"name": "Fruit Cup", "price": 2.00, "stock": 5}
            }
        }
        # Flag to track if the first purchase has been made
        self.first_purchase = True

    # Display the menu to the user
    def show_menu(self):
        print("\nMetro's Menu:")
        for category, items in self.products.items():
            print(f"\n{category}:")
            for code, item in items.items():
                print(f"{code}. {item['name']} - ${item['price']:.2f} (Stock: {item['stock']})")

    # Handle item purchase logic
    def purchase_item(self, item_code, amount_inserted):
        # Search for the selected item in the product list
        for category, items in self.products.items():
            if item_code in items:
                product = items[item_code]  # Retrieve the product details
                print(f"You have selected {product['name']} from the {category} category.")
                break
        else:
            # Invalid item code entered
            print("Invalid item code.")
            return amount_inserted, None

        # Check if the product is out of stock
        if product['stock'] <= 0:
            print(f"Sorry, {product['name']} is out of stock.")
            return amount_inserted, None

        # Apply a 10% discount for the first purchase
        price = product['price']
        if self.first_purchase:
            price *= 0.9
            print("Congratulations! You got a 10% discount.")
            self.first_purchase = False

        # Check if the user has inserted enough money
        if amount_inserted < price:
            print(f"Insufficient funds. You need to insert ${price - amount_inserted:.2f} more.")
            return amount_inserted, price

        # Update stock and calculate change
        product['stock'] -= 1
        change = amount_inserted - price
        print(f"Dispensing {product['name']}.")
        print(f"Your change is ${change:.2f}. Thank you for buying!")
        return change, None

    # Suggest complementary items based on the selected product
    def suggest_purchase(self, item_code):
        # Predefined suggestions for each product code
        suggestions = {
            1: "Suggested purchase: Biscuits! A great choice with Soda.",
            2: "Suggested purchase: Juice! Perfect with Chips.",
            3: "Suggested purchase: Coffee! A nice pairing with Chocolate Bar.",
            4: "Suggested purchase: Tea! A refreshing choice with Water.",
            5: "Suggested purchase: Biscuits! Great with Coffee.",
            6: "Suggested purchase: Juice! A good match with Biscuits.",
            7: "Suggested purchase: Chocolate Bar! A sweet treat with Juice.",
            8: "Suggested purchase: Coffee! A warm drink to enjoy with Tea.",
            9: "Suggested purchase: Coffee! Perfect with Donuts.",
            10: "Suggested purchase: Fruit Cup! A healthy choice with Cake.",
            11: "Suggested purchase: Granola Bar! A great snack with Fruit Cup.",
            12: "Suggested purchase: Chips! A crunchy snack to enjoy with Granola Bar."
        }
        if item_code in suggestions:
            print(suggestions[item_code])

    # Handle payment processing
    def choose_payment_method(self, total_amount):
        while True:
            # Prompt the user to choose a payment method
            print("Choose your payment method:")
            print("1. Cash")
            print("2. Card")
            payment_method = input("Enter 1 or 2: ").strip()

            if payment_method == '1':
                # Handle cash payment
                while True:
                    try:
                        amount = float(input(f"Insert cash (Total amount: ${total_amount:.2f}): $"))
                        return amount
                    except ValueError:
                        print("Invalid amount. Please enter a valid number.")
            elif payment_method == '2':
                # Handle card payment
                print("Processing your card payment...")
                print("Payment is being processed...")
                print("Payment was successful. The amount has been charged to your card.")
                return total_amount
            else:
                # Invalid payment method
                print("Invalid option. Please try again.")

    # Main function to run the vending machine
    def run(self):
        print("Welcome to Metro's Vending Machine!")
        while True:
            # Display the product menu
            self.show_menu()

            # Prompt the user to select an item or exit
            user_input = input("Enter the code of the item you want to buy or type 'exit' to quit: ").strip()

            if user_input.lower() == 'exit':
                # Exit the vending machine
                print("Thank you for visiting Metro's Vending Machine")
                break

            try:
                # Validate and convert the item code
                item_code = int(user_input)
                if not any(item_code in items for items in self.products.values()):
                    print("Invalid code. Please try again.")
                    continue
            except ValueError:
                # Handle non-numeric input
                print("Invalid code. Kindly make sure to fill a correct item code.")
                continue

            # Determine the price of the selected item
            total_amount = next(item['price'] for items in self.products.values() for item in items.values() if item_code in items)

            # Process payment
            amount_inserted = self.choose_payment_method(total_amount)

            # Attempt to purchase the item
            remaining_amount, required_amount = self.purchase_item(item_code, amount_inserted)

            while required_amount is not None:
                # If additional payment is required
                print(f"You still need to insert ${required_amount - remaining_amount:.2f} more.")
                additional_amount = self.choose_payment_method(required_amount - remaining_amount)

                remaining_amount += additional_amount
                if remaining_amount >= required_amount:
                    # Complete the purchase if sufficient funds are provided
                    remaining_amount, required_amount = self.purchase_item(item_code, remaining_amount)
                else:
                    # Inform the user of the remaining amount needed
                    print(f"You still need to insert ${required_amount - remaining_amount:.2f} more.")

            if remaining_amount > 0:
                # Refund any extra amount inserted
                print(f"Refunding ${remaining_amount:.2f}.")

            # Suggest complementary purchases
            self.suggest_purchase(item_code)

            # Prompt the user to continue or exit
            continue_shopping = input("Enter 1 to continue shopping or 0 to exit: ").strip()
            if continue_shopping == '0':
                print("Thank you for visiting Metro's Vending Machine!, We hope to see you again soon")
                break

# Create and run the vending machine
machine = MetrosVendingMachine()
machine.run()

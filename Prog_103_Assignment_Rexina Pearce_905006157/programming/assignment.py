import csv
import os
from datetime import datetime


# Functions using Structured Programming

def calculate_subtotal(qty, price):
    """Sequence: Direct calculation"""
    return qty * price


def apply_discount(subtotal, discount_percent):
    """Selection: Only apply if discount > 0"""
    if discount_percent > 0:
        return subtotal * (discount_percent / 100)
    return 0


def calculate_tax(subtotal_after_discount, tax_percent):
    """Selection: Only apply if tax > 0"""
    if tax_percent > 0:
        return subtotal_after_discount * (tax_percent / 100)
    return 0


def save_transaction(data, filename="sales_log.csv"):
    """Modularization: Handles all file operations"""
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def display_daily_summary(filename="sales_log.csv"):
    """Iteration: Loops through file to calculate today's totals"""
    if not os.path.exists(filename):
        print("\nNo sales recorded yet.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    total_sales = 0
    total_tax = 0
    transaction_count = 0

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:  # Iteration
            if row['Date'].startswith(today):
                total_sales += float(row['Total'])
                total_tax += float(row['Tax'])
                transaction_count += 1

    print("\n--- DAILY SUMMARY ---")
    print(f"Date: {today}")
    print(f"Total Sales: Le {total_sales:,.2f}")
    print(f"Transactions: {transaction_count}")
    print(f"Tax Collected: Le {total_tax:,.2f}")
    print("---------------------\n")


#  Main Program
def main():
    print("=" * 40)
    print("   SMALL BUSINESS SALES CALCULATOR")
    print("=" * 40)

    while True:  # Iteration: Main program loop
        items = []  # Data Structure: List to hold items

        # Add Items Loop
        while True:  # Iteration: Add multiple items
            print("\n--- New Sale ---")
            item_name = input("Enter item name or 'done' to finish: ").strip()

            if item_name.lower() == 'done':
                break

            try:  # Selection: Input validation
                qty = int(input("Enter quantity: "))
                price = float(input("Enter unit price Le: "))

                if qty <= 0 or price < 0:
                    print("Error: Quantity and price must be positive.")
                    continue

            except ValueError:
                print("Error: Please enter valid numbers.")
                continue

            subtotal = calculate_subtotal(qty, price)
            items.append({
                "Item": item_name,
                "Qty": qty,
                "Price": price,
                "Subtotal": subtotal
            })
            print(f"Added: {item_name} x{qty} = Le {subtotal:,.2f}")

        if not items:
            print("No items added. Returning to menu.")
        else:
            # Display Items & Calculate Totals
            print("\n--- Current Sale ---")
            total_subtotal = 0
            for item in items:  # Iteration
                print(f"{item['Item']}: {item['Qty']} x Le {item['Price']:,.2f} = Le {item['Subtotal']:,.2f}")
                total_subtotal += item['Subtotal']

            print(f"\nSubtotal: Le {total_subtotal:,.2f}")

            #  Discount & Tax
            try:
                discount = float(input("Enter discount % or 0: "))
                tax = float(input("Enter tax/VAT % or 0: "))
            except ValueError:
                print("Invalid input. Setting discount and tax to 0.")
                discount, tax = 0, 0

            discount_amt = apply_discount(total_subtotal, discount)
            taxable_amt = total_subtotal - discount_amt
            tax_amt = calculate_tax(taxable_amt, tax)
            final_total = taxable_amt + tax_amt

            # Final Summary
            print("\n--- RECEIPT ---")
            print(f"Subtotal:       Le {total_subtotal:,.2f}")
            print(f"Discount {discount}%:  -Le {discount_amt:,.2f}")
            print(f"Tax {tax}%:        +Le {tax_amt:,.2f}")
            print(f"TOTAL PAYABLE:  Le {final_total:,.2f}")
            print("---------------")

            #  Save
            confirm = input("Complete sale and save? y/n: ").lower()
            if confirm == 'y':  # Selection
                transaction = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Items": len(items),
                    "Subtotal": round(total_subtotal, 2),
                    "Discount": round(discount_amt, 2),
                    "Tax": round(tax_amt, 2),
                    "Total": round(final_total, 2)
                }
                save_transaction(transaction)
                print("Sale recorded to sales_log.csv!")
            else:
                print("Sale cancelled.")

        #  Menu
        print("\nOptions: 1. New Sale  2. Daily Summary  3. Exit")
        choice = input("Choose option: ").strip()

        if choice == '2':
            display_daily_summary()
        elif choice == '3':
            print("Goodbye!")
            break
        # If 1 or invalid, loop continues for new sale


if __name__ == "__main__":
    main()

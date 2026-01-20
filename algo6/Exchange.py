# price_generator.py
import random
import time
import json

def generate_price(base_price=1000):
    """Simulate small, slower random changes in stock price (INR, whole rupees)."""
    change = random.randint(-3, 3)  # +/- ₹3 maximum fluctuation
    new_price = max(1, base_price + change)  # avoid negative price
    return new_price

def main():
    price = 1000  # starting price in INR
    print("📈 Starting price generator... (Press Ctrl+C to stop)\n")
    while True:
        price = generate_price(price)
        with open("price_data.json", "w") as f:
            json.dump({"price": price}, f)
        print(f"Updated price: ₹{price}")
        time.sleep(2)  # slower updates (every 2 seconds)

if __name__ == "__main__":
    main()

# adaptive_trader.py
import json
import time
import os

CAPITAL = 100000
STEP_TIME = 10         # seconds per step
STEP_LIMIT = 15        # total steps in first cycle
PRICE_FILE = "price_data.json"

# ---------- Utility Functions ----------

def get_latest_price():
    """Read latest price from price_data.json safely."""
    try:
        with open(PRICE_FILE, "r") as f:
            data = json.load(f)
            return data["price"]
    except Exception as e:
        print(f"[⚠️] Error reading price file: {e}")
        return None

def calc_portfolio_value(shares, avg_cost, last_price):
    return shares * last_price

def print_status(cycle, step, shares, avg_cost, price, capital):
    print(f"[Cycle {cycle} | Step {step}] Price ₹{price} | Shares {shares} | "
          f"Avg Cost ₹{avg_cost:.2f} | Capital ₹{capital:.2f}")

# ---------- Trading Logic ----------

def trade_cycle(cycle_length, starting_capital, starting_shares, starting_avg_cost, cycle_num=1):
    """Run one trading cycle of N steps."""
    shares = starting_shares
    avg_cost = starting_avg_cost
    capital = starting_capital
    profit_steps = 0
    loss_steps = 0
    last_price = get_latest_price()

    print(f"\n🚀 Starting Cycle {cycle_num} for {cycle_length} steps...\n")

    for step in range(1, cycle_length + 1):
        time.sleep(STEP_TIME)
        price = get_latest_price()
        if price is None:
            continue  # skip iteration if no price

        # Buy 1 share per step (if enough capital)
        if capital >= price:
            shares += 1
            capital -= price
            avg_cost = ((avg_cost * (shares - 1)) + price) / shares
        else:
            print("💰 Not enough capital to buy more shares.")
            break

        # Check if price is up or down compared to previous
        if price > last_price:
            profit_steps += 1
        elif price < last_price:
            loss_steps += 1

        last_price = price
        print_status(cycle_num, step, shares, avg_cost, price, capital)

    # After cycle complete → evaluate portfolio
    portfolio_value = calc_portfolio_value(shares, avg_cost, last_price)
    total_value = portfolio_value + capital
    invested = shares * avg_cost
    profit_pct = ((last_price - avg_cost) / avg_cost) * 100 if avg_cost else 0

    print(f"\n📊 Cycle {cycle_num} Summary:")
    print(f"   Profit steps: {profit_steps}/{cycle_length}")
    print(f"   Shares held: {shares}, Avg Cost ₹{avg_cost:.2f}")
    print(f"   Portfolio Value ₹{portfolio_value:.2f}, Capital ₹{capital:.2f}")
    print(f"   Net {'Profit' if profit_pct > 0 else 'Loss'}: {profit_pct:.2f}%\n")

    # Stop or continue logic
    if profit_pct <= 0 or profit_steps == 0:
        print("🛑 Stopping due to loss or no profit steps.")
        return capital + shares * last_price  # Final account value

    # Next cycle → half of profit steps
    next_steps = profit_steps // 2
    if next_steps < 1:
        print("✅ Strategy complete. Stopping (next cycle < 1 step).")
        return capital + shares * last_price

    # Recursive continuation
    return trade_cycle(next_steps, capital, shares, avg_cost, cycle_num + 1)


# ---------- Main Runner ----------

def main():
    print("\n📘 Starting Adaptive Trading Bot...\n")

    if not os.path.exists(PRICE_FILE):
        print(f"[❌] Missing {PRICE_FILE}. Please start price_generator.py first.")
        return

    final_value = trade_cycle(STEP_LIMIT, CAPITAL, 0, 0.0)
    print(f"\n🏁 Trading finished. Final portfolio value: ₹{final_value:.2f}")

if __name__ == "__main__":
    main()

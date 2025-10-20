import os
import sys
import pandas as pd

def generate_summary(portfolio_file):
    if not os.path.exists(portfolio_file):
        print(f"Error: file {portfolio_file} not found", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("Portfolio is empty.")
        return

    total_value = df["card_market_value"].sum()
    top_idx = df["card_market_value"].idxmax()
    top_card = df.loc[top_idx]

    print("=== Portfolio Summary ===")
    print(f"Total Portfolio Value: ${total_value:,.2f}")
    print(
        f"Most Valuable Card: {top_card['card_name']} "
        f"(ID: {top_card['card_id']}) - "
        f"${top_card['card_market_value']:,.2f}"
    )

def main():
    generate_summary("card_portfolio.csv")

def test():
    generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
    print("Starting in Test Mode")
    test()

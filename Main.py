import sys
import pandas as pd

portfolios = {}


def check_trade(trade):

    # Step 1: Validate trade data

    try:
        quantity = float(trade["quantity"])
        price = float(trade["price"])
        action = str(trade["action"]).strip().capitalize()

    except (ValueError, TypeError):
        return "Rejected", "Invalid trade data."

    if quantity <= 0 or price <= 0 or action not in ["Buy", "Sell"]:
        return "Rejected", "Invalid trade data."

    portfolio_id = trade["portfolio_id"]
    security_id = trade["security_id"]

    if portfolio_id not in portfolios:
        return "Needs Manual Sign-off", "Portfolio reference data unavailable."

    portfolio = portfolios[portfolio_id]

    cash = portfolio["cash_balance"]
    restricted = portfolio["restricted_securities"]
    max_position = portfolio["max_position_pct"]
    holdings = portfolio["current_holdings"]

    # Step 2: Restricted security check

    if security_id in restricted:
        return "Rejected", "Security is restricted for this portfolio."

    existing_quantity = 0

    for holding in holdings:
        if holding[0] == security_id:
            existing_quantity += holding[1]

    # Step 3: Sell check

    if action == "Sell":
        if existing_quantity < quantity:
            return "Rejected", "Insufficient holdings to sell."

    # Step 4: Buy affordability check

    if action == "Buy":

        trade_value = quantity * price

        if trade_value > cash:
            return "Rejected", "Insufficient cash for this buy order."

        # Step 5: Position concentration check

        post_trade_cash = cash - trade_value

        post_trade_quantity = existing_quantity + quantity

        post_trade_security_value = post_trade_quantity * price

        other_holdings_value = 0

        for holding in holdings:
            if holding[0] != security_id:
                other_holdings_value += holding[1] * holding[2]

        total_portfolio_value = (
            post_trade_cash
            + post_trade_security_value
            + other_holdings_value
        )

        if total_portfolio_value <= 0:
            return "Needs Manual Sign-off", "Invalid portfolio valuation."

        position_percentage = (
            post_trade_security_value / total_portfolio_value
        )

        if position_percentage > max_position:
            return (
                "Needs Manual Sign-off",
                "Exceeds maximum position concentration — requires approval."
            )

    # Step 6: Approve trade

    return "Approved", "Trade passed all compliance checks."


def main():

    input_file = "proposed_trades.csv"
    output_file = "trade_compliance_results.csv"

    try:
        trades = pd.read_csv(input_file)

        required_columns = [
            "portfolio_id",
            "security_id",
            "action",
            "quantity",
            "price",
            "security_type"
        ]

        for column in required_columns:
            if column not in trades.columns:
                print("Missing column:", column)
                sys.exit(1)

        decisions = []
        reasons = []

        for index, trade in trades.iterrows():
            decision, reason = check_trade(trade)
            decisions.append(decision)
            reasons.append(reason)

        trades["decision"] = decisions
        trades["reason"] = reasons

        trades.to_csv(output_file, index=False)

        print("\nTRADE COMPLIANCE RESULTS")
        print("-" * 40)

        for index, trade in trades.iterrows():
            print("\nTrade", index + 1)
            print("Portfolio:", trade["portfolio_id"])
            print("Security:", trade["security_id"])
            print("Action:", trade["action"])
            print("Decision:", trade["decision"])
            print("Reason:", trade["reason"])

        print("\nSUMMARY")
        print("Total trades:", len(trades))
        print("Approved:", (trades["decision"] == "Approved").sum())
        print("Rejected:", (trades["decision"] == "Rejected").sum())
        print(
            "Needs Manual Sign-off:",
            (trades["decision"] == "Needs Manual Sign-off").sum()
        )

        print("\nResults saved to", output_file)

    except FileNotFoundError:
        print("Input CSV file not found:", input_file)
        sys.exit(1)


if __name__ == "__main__":
    main()
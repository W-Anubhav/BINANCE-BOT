import argparse
import os
import sys
from dotenv import load_dotenv
from client import BinanceFuturesClient

def main():
    parser = argparse.ArgumentParser(description="Simplified Binance Futures Trading Bot CLI")
    
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], required=True, help="Order side (BUY/SELL)")
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT"], required=True, help="Order type (MARKET/LIMIT)")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price for LIMIT orders")

    args = parser.parse_args()

    if args.type == "LIMIT" and args.price is None:
        parser.error("--price is required when --type is LIMIT")

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("Error: BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env file.")
        sys.exit(1)

    print("\n--- Order Request Summary ---")
    print(f"Symbol: {args.symbol}")
    print(f"Side: {args.side}")
    print(f"Type: {args.type}")
    print(f"Quantity: {args.quantity}")
    if args.type == "LIMIT":
        print(f"Price: {args.price}")
    print("-----------------------------\n")

    # Initialize client and place order
    try:
        client = BinanceFuturesClient(api_key, api_secret)
        result = client.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

        print("\n--- Order Result ---")
        if result["success"]:
            print(f"Status: SUCCESS")
            print(f"Message: {result['message']}")
            details = result["details"]
            print(f"Order ID: {details['orderId']}")
            print(f"Order Status: {details['status']}")
            print(f"Executed Qty: {details['executedQty']}")
            print(f"Average Price: {details['avgPrice']}")
        else:
            print(f"Status: FAILED")
            print(f"Error: {result['error']}")
        print("--------------------\n")

    except Exception as e:
        print(f"Critical execution error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

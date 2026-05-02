import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from client import BinanceFuturesClient

load_dotenv()

# We need the API keys to initialize the Binance client for the agent
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")

# Initialize the client only if keys are present
binance_client = None
if binance_api_key and binance_api_secret and binance_api_secret != "your_testnet_secret_key_here":
    try:
        binance_client = BinanceFuturesClient(binance_api_key, binance_api_secret)
    except Exception as e:
        print(f"Agent warning: Binance client failed to initialize: {e}")

def place_order_tool(query: str) -> str:
    """
    Parses a combined query string to place an order.
    Expected format: "symbol,side,type,quantity,price"
    Price is optional for MARKET orders.
    """
    if not binance_client:
        return "Error: Binance client is not initialized. Please check your API keys in the .env file."

    parts = [p.strip() for p in query.split(",")]
    if len(parts) < 4:
        return "Error: Invalid input format. Please provide symbol, side, type, quantity (and price if LIMIT)."
    
    symbol = parts[0]
    side = parts[1]
    order_type = parts[2]
    
    try:
        quantity = float(parts[3])
        price = float(parts[4]) if len(parts) > 4 and parts[4].lower() != "none" else None
        
        result = binance_client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        if result["success"]:
            details = result["details"]
            return f"Success! Order ID: {details['orderId']}, Status: {details['status']}, Executed Qty: {details['executedQty']}, Avg Price: {details['avgPrice']}"
        else:
            return f"Failed: {result['error']}"
    except ValueError:
        return "Error: Quantity and price must be valid numbers."

# Define the tools
tools = [
    Tool(
        name="Place_Binance_Futures_Order",
        func=place_order_tool,
        description=(
            "Use this tool to place a MARKET or LIMIT order on Binance Futures Testnet. "
            "Input should be a comma-separated string in this exact order: "
            "symbol,side,type,quantity,price. "
            "Example 1 (Market): BTCUSDT,BUY,MARKET,0.1 "
            "Example 2 (Limit): ETHUSDT,SELL,LIMIT,0.5,3000.0 "
            "If price is not needed, do not include it or pass 'None'."
        )
    )
]

def get_agent():
    # Initialize the LLM
    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    
    # Initialize the agent
    agent = create_react_agent(
        tools=tools,
        model=llm,
        prompt="You are a helpful AI trading assistant. A user wants to place an order on Binance Futures Testnet. Help them format their request and use the Place_Binance_Futures_Order tool."
    )
    return agent

def run_agent(user_input: str) -> str:
    agent = get_agent()
    try:
        # LangGraph invoke structure requires a dict with "messages"
        response = agent.invoke({"messages": [("user", user_input)]})
        # The final message content is the agent's response
        return response["messages"][-1].content
    except Exception as e:
        return f"Agent encountered an error: {e}"

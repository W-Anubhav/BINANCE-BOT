# BINANCE-BOT

 Binance Futures Trading Bot (Testnet)

This project is a simplified trading bot for the Binance Futures Testnet (USDT-M), fulfilling the core requirements of placing Market and Limit orders via a CLI, logging, and structured code.

Additionally, this project includes an **AI Agent wrapper** using Langchain and a **Streamlit UI**, allowing users to place trades using natural language.

# Project Structure

- `client.py`: The core API wrapper utilizing the `python-binance` library.
- `logger.py`: Centralized logging configuration (writes to `trading_bot.log`).
- `cli.py`: The command-line interface using `argparse`.
- `agent.py`: A Langchain agent that uses `client.py` as tools to execute natural language trades.
- `app.py`: A lightweight Streamlit chat interface for the AI Agent.

 Setup Instructions

1. **Clone the repository** (or extract the zip folder).
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your Binance Testnet API Key and Secret Key. If you want to use the AI Streamlit interface, also provide an OpenAI API Key.

   ```
   BINANCE_API_KEY=your_key
   BINANCE_API_SECRET=your_secret
   OPENAI_API_KEY=your_openai_key
   ```

## Running Examples (CLI)

The CLI fulfills the core requirements of the task. It supports both BUY and SELL sides, and MARKET and LIMIT order types.

**1. Place a MARKET order (BUY)**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.1
```

**2. Place a LIMIT order (SELL)**
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3500.0
```

## Running the Streamlit UI (AI Agent)

If you prefer a natural language interface, run the Streamlit app:
```bash
streamlit run app.py
```
You can then type commands like: "Buy 0.1 BTC at market price" or "Sell 0.5 ETH at a limit price of 3500". The Langchain agent will parse this and execute the trade securely via the underlying API layer.

## Assumptions
- The testnet account has sufficient USDT to cover the trades.
- Python 3.10+ is installed.
- For the AI agent, a valid LLM API key (e.g., OpenAI) is provided.

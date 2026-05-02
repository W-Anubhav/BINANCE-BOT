import os
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from logger import logger

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        # Initialize client with testnet
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            logger.info("Initialized Binance client on testnet.")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """
        Place a MARKET or LIMIT order on Binance Futures Testnet.
        """
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()

        logger.info(f"Order Request: {side} {quantity} {symbol} @ {order_type} (Price: {price})")

        try:
            params = {
                'symbol': symbol,
                'side': getattr(Client, f"SIDE_{side}", side),
                'type': getattr(Client, f"ORDER_TYPE_{order_type}", order_type),
                'quantity': quantity
            }

            if order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price must be provided for LIMIT orders.")
                params['price'] = price
                params['timeInForce'] = Client.TIME_IN_FORCE_GTC

            # Place the order via Futures API
            logger.info(f"Sending API request with params: {params}")
            response = self.client.futures_create_order(**params)
            
            logger.info("Order placed successfully.")
            logger.info(f"Order Response: {response}")

            # Extract details for clear output
            order_id = response.get('orderId')
            status = response.get('status')
            executed_qty = response.get('executedQty')
            avg_price = response.get('avgPrice', 'N/A')

            return {
                "success": True,
                "message": "Order executed successfully",
                "details": {
                    "orderId": order_id,
                    "status": status,
                    "executedQty": executed_qty,
                    "avgPrice": avg_price
                },
                "raw_response": response
            }

        except BinanceAPIException as e:
            logger.error(f"Binance API Exception: {e}")
            return {"success": False, "error": f"API Error: {e}"}
        except BinanceOrderException as e:
            logger.error(f"Binance Order Exception: {e}")
            return {"success": False, "error": f"Order Error: {e}"}
        except ValueError as e:
            logger.error(f"Value Error: {e}")
            return {"success": False, "error": f"Input Error: {e}"}
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            return {"success": False, "error": f"Unexpected Error: {e}"}

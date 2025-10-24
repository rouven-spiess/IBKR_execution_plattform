import threading
import time

from wrapper import IBWrapper
from client import IBClient

from contract import stock, future, option, crypto
from order import limit, BUY


class IBApp(IBWrapper, IBClient):
    def __init__(self, ip, port, client_id):
        IBWrapper.__init__(self)
        IBClient.__init__(self, wrapper=self)
        
        # Store connection parameters
        self.ip = ip
        self.port = port
        self.client_id = client_id

        self.connect(ip, port, client_id)

        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        time.sleep(2)
        
        # Request open orders to receive callbacks
        self.request_open_orders()
        
        # Test if wrapper methods are being called
        print("🔧 Testing wrapper methods...")
        print(f"🔧 Next valid order ID: {self.nextValidOrderId}")


if __name__ == "__main__":
    app = IBApp("127.0.0.1", 7497, client_id=10)
    # eur = future("ES", "CME", "202512")
    # for tick in app.get_streaming_data(99, eur):
    #     print(tick)
    aapl=stock("AAPL", "SMART", "USD")
    
    # Try different Air Liquide contract configurations
    # Option 1: Using SMART routing (most common for European stocks)
    air_liquide=stock("AI", "SMART", "EUR")
    
    # Cryptocurrency contracts (trade 24/7 including weekends)
    btc = crypto("BTC", "USD")
    eth = crypto("ETH", "USD")
    
    # Option 2: If SMART doesn't work, try these alternatives:
    # air_liquide=stock("AI", "EPA", "EUR")  # Euronext Paris
    # air_liquide=stock("AI", "EURONEXT", "EUR")  # Euronext
    # air_liquide=stock("AI", "IBIS", "EUR")  # German exchange routing
    # gbl=future("GBL", "EUREX", "202403")
    # pltr=option("PLTR", "BOX", "20240315", 20, "C")
    # data = app.get_historical_data(
    #     request_id=99, contract=aapl, duration="2 D", bar_size="30 secs"
    # )
    # print(data)
    # market_data = app.get_market_data(request_id=99, contract=aapl)
    # print(market_data)
    # Try to get market data first to test the contract
    try:
        # Test with AAPL (since crypto has API version issues)
        market_data = app.get_market_data(request_id=1, contract=aapl)
        print(f"Current AAPL price: ${market_data}")
        
        # If market data works, place the order
        # Use a limit order with a price that's unlikely to fill immediately
        current_price = market_data
        limit_price = current_price - 5.0  # $5 below current price (unlikely to fill)
        limit_order = limit(BUY, 1, limit_price)  # 1 share
        order_id = app.send_order(aapl, limit_order)
        print(f"Order placed with ID: {order_id}")
        
        # Wait longer for order callbacks to come through
        print("Waiting for order callbacks...")
        time.sleep(10)
        
        # Check order status (commented out to avoid tickerId error)
        # print("Checking order status...")
        # app.check_order_status(order_id)
        
        # Request executions after order is placed (commented out to avoid tickerId error)
        # print("Requesting executions...")
        # app.request_executions()
        
        # Wait a bit to see order callbacks
        print("Waiting for order callbacks...")
        time.sleep(5)
        
    except Exception as e:
        print(f"Error with current contract parameters: {e}")
        print("Try uncommenting one of the alternative contract configurations above")

    # for tick in app.get_streaming_data(99, eur):
        # print(tick)
    time.sleep(10)
    app.disconnect()

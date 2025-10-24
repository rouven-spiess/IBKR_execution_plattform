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


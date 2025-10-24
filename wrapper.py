from ibapi.wrapper import EWrapper
from threading import Event


class IBWrapper(EWrapper):
    def __init__(self):
        EWrapper.__init__(self)
        self.nextValidOrderId = None
        self.historical_data = {}
        self.market_data = {}
        self.stream_event = Event()
        self.streaming_data = {}


    def historicalData(self, request_id, bar):
        bar_data = (
            bar.date,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )
        if request_id not in self.historical_data.keys():
            self.historical_data[request_id] = []
        self.historical_data[request_id].append(bar_data)

    def tickPrice(self, request_id, tick_type, price, attrib):
        if request_id not in self.market_data.keys():
            self.market_data[request_id] = {}
        self.market_data[request_id][tick_type] = float(price)
        print(f"📈 TICK PRICE - Request ID: {request_id}, Type: {tick_type}, Price: {price}")

    def tickByTickBidAsk(self, request_id, time, bid_price, ask_price, bid_size, ask_size, tick_attrib_last):
        tick_data = (
            time,
            bid_price,
            ask_price,
            bid_size,
            ask_size,
        )
        self.streaming_data[request_id] = tick_data
        self.stream_event.set()

    def nextValidId(self, order_id):
        super().nextValidId(order_id)
        self.nextValidOrderId = order_id
        print(f"🆔 NEXT VALID ORDER ID: {order_id}")

    def orderStatus(self,
                    order_id,
                    status,
                    filled,
                    remaining,
                    avg_fill_price,
                    perm_id,
                    parent_id,
                    last_fill_price,
                    client_id,
                    why_held,
                    mkt_cap_price):
        print(
            f"📊 ORDER STATUS - ID: {order_id}, Status: {status}, "
            f"Filled: {filled}, Remaining: {remaining}, "
            f"Avg Fill Price: {avg_fill_price}, Last Fill Price: {last_fill_price}"
        )

    def openOrder(self, order_id, contract, order, order_state):
        print(
            f"📋 OPEN ORDER - ID: {order_id}, Symbol: {contract.symbol}, "
            f"Exchange: {contract.exchange}, Action: {order.action}, "
            f"Type: {order.orderType}, Quantity: {order.totalQuantity}, "
            f"Status: {order_state.status}"
        )

    def execDetails(self, request_id, contract, execution):
        print(
            f"✅ ORDER EXECUTED - Request ID: {request_id}, Symbol: {contract.symbol}, "
            f"Currency: {contract.currency}, Exec ID: {execution.execId}, "
            f"Order ID: {execution.orderId}, Shares: {execution.shares}, "
            f"Last Liquidity: {execution.lastLiquidity}"
        )

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"❌ ERROR - Request ID: {reqId}, Code: {errorCode}, Message: {errorString}")
        if advancedOrderRejectJson:
            print(f"Advanced Order Reject: {advancedOrderRejectJson}")

    def openOrderEnd(self):
        print("📋 OPEN ORDER END - All open orders received")

    def execDetailsEnd(self, reqId):
        print(f"✅ EXEC DETAILS END - Request ID: {reqId}")
from ibapi.client import EClient

import time
import pandas as pd

from dataclasses import dataclass, field

TRADE_BAR_PROPERTIES = ["time", "open", "high", "low", "close", "volume"]

@dataclass
class Tick:
    time: int
    bid_price: float
    ask_price: float
    bid_size: float
    ask_size: float
    timestamp_: pd.Timestamp = field(init=False)    

    def __post_init__(self):
        self.timestamp_ = pd.to_datetime(self.time, unit="s")
        self.bid_price = float(self.bid_price)
        self.ask_price = float(self.ask_price)
        self.bid_size = float(self.bid_size)
        self.ask_size = float(self.ask_size)


class IBClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
    
    def request_open_orders(self):
        """Request all open orders to receive openOrder callbacks"""
        self.reqAllOpenOrders()
    
    def request_executions(self, req_id=1):
        """Request executions to receive execDetails callbacks"""
        from ibapi.execution import ExecutionFilter
        exec_filter = ExecutionFilter()
        self.reqExecutions(reqId=req_id, execFilter=exec_filter)
    
    def check_order_status(self, order_id):
        """Request order status updates"""
        self.reqIds(-1)  # This will trigger order status updates

    def get_historical_data(self, request_id, contract, duration, bar_size):
        self.reqHistoricalData(
            reqId=request_id,
            contract=contract,
            endDateTime="",
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow="MIDPOINT",
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[],
        )
        time.sleep(5)

        bar_sizes = ["day", "D", "week", "W", "month"]
        if any(x in bar_size for x in bar_sizes):
            fmt = "%Y%m%d"
        else:
            fmt = "%Y%m%d  %H:%M:%S"  # Note: removed %Z timezone

        data = self.historical_data[request_id]
        df = pd.DataFrame(data, columns=TRADE_BAR_PROPERTIES)
        df.set_index(pd.to_datetime(df.time, format=fmt), inplace=True)
        df.drop("time", axis=1, inplace=True)
        df["symbol"] = contract.symbol
        df.request_id = request_id

        return df

    def get_historical_data_for_many(
        self, request_id, contracts, duration, bar_size, col_to_use="close"
    ):
        dfs = []
        for contract in contracts:
            data = self.get_historical_data(request_id, contract, duration, bar_size)
            dfs.append(data)
            request_id += 1
        return (
            pd.concat(dfs)
            .reset_index()
            .pivot(index="time", columns="symbol", values=col_to_use)
        )

    def get_market_data(self, request_id, contract, tick_type=4):
        self.reqMktData(
            reqId=request_id,
            contract=contract,
            genericTickList="",
            snapshot=True,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )
        time.sleep(5)

        self.cancelMktData(reqId=request_id)

        return self.market_data[request_id][tick_type]

    def get_streaming_data(self, request_id, contract):
        self.reqTickByTickData(
            reqId=request_id,
            contract=contract,
            tickType="BidAsk",
            numberOfTicks=0,
            ignoreSize=True,
        )
        time.sleep(10)
        while True:
            if self.stream_event.is_set():
                yield Tick(*self.streaming_data[request_id])
                self.stream_event.clear()
    
    def stop_streaming_data(self, request_id):
        self.cancelTickByTickData(reqId=request_id)

    def send_order(self, contract, order):
        order_id = self.wrapper.nextValidOrderId
        print(f"Placing order: ID={order_id}, Action={order.action}, Type={order.orderType}, Quantity={order.totalQuantity}, Price={getattr(order, 'lmtPrice', 'N/A')}")
        
        # Debug output removed - order is working now!
        
        # Place the order
        self.placeOrder(orderId=order_id, contract=contract, order=order)
        
        # Request next valid order ID for future orders
        self.reqIds(-1)
        
        return order_id

    def cancel_all_orders(self):
        self.reqGlobalCancel()

    def cancel_order_by_id(self, order_id):
        self.cancelOrder(orderId=order_id)

    def update_order(self, contract, order, order_id):
        self.cancel_order_by_id(order_id)
        return self.send_order(contract, order)
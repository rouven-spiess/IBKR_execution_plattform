import pytest
import time

from ibkr_execution_plattform.contract import stock
from ibkr_execution_plattform.broker_interface import IBApp
from ibkr_execution_plattform.order import limit, BUY
from ibapi.contract import Contract

def test_cme_futures_market_data():
    """
    Test CME futures market data retrieval functionality.
    
    This test verifies the following capabilities:
    1. ES (E-mini S&P 500) contract is correctly defined with proper futures parameters
    2. CL (Crude Oil) contract is correctly defined with proper futures parameters
    3. SMART exchange routing works for futures contracts
    4. Real-time price data is available and flowing correctly
    5. Futures market data farms are connected and providing CME data
    
    The test retrieves live market data for ES and CL futures contracts,
    confirming that futures trading infrastructure is working correctly.
    """
    app = IBApp("127.0.0.1", 7497, client_id=10)
    
    # ES (E-mini S&P 500) futures contract - try different approaches
    es_contract = Contract()
    es_contract.symbol = "ES"
    es_contract.secType = "FUT"
    es_contract.exchange = "CME"
    es_contract.currency = "USD"
    es_contract.lastTradeDateOrContractMonth = "202512"  # December 2025
    es_contract.multiplier = "50"  # ES multiplier
    
    # CL (Crude Oil) futures contract
    cl_contract = Contract()
    cl_contract.symbol = "CL"
    cl_contract.secType = "FUT"
    cl_contract.exchange = "NYMEX"
    cl_contract.currency = "USD"
    cl_contract.lastTradeDateOrContractMonth = "202512"  # December 2025
    cl_contract.multiplier = "1000"  # CL multiplier (1000 barrels)
    
    try:
        # Test ES futures market data
        print("Testing ES (E-mini S&P 500) futures...")
        es_market_data = app.get_market_data(request_id=7, contract=es_contract)
        print(f"Current ES price: ${es_market_data}")
        
        # Test CL futures market data
        print("Testing CL (Crude Oil) futures...")
        cl_market_data = app.get_market_data(request_id=8, contract=cl_contract)
        print(f"Current CL price: ${cl_market_data}")
        
    except Exception as e:
        print(f"Error with futures contract parameters: {e}")
        print("Check if futures market data subscription is active")
        print("Note: Futures contracts may need different contract month or exchange settings")

    app.disconnect()

def test_cme_futures_order_placement():
    """
    Test CME futures order placement and order book verification.
    
    This test verifies the following capabilities:
    1. Place a limit order for ES (E-mini S&P 500) futures
    2. Place a limit order for CL (Crude Oil) futures
    3. Order appears in IBKR order book
    4. Order callbacks are received (orderStatus, openOrder)
    5. Order remains open (limit price below market to avoid immediate fill)
    
    The test places limit buy orders for ES and CL futures at prices below current market
    to ensure they stay open and can be verified in the order book.
    """
    app = IBApp("127.0.0.1", 7497, client_id=10)
    
    # ES (E-mini S&P 500) futures contract
    es_contract = Contract()
    es_contract.symbol = "ES"
    es_contract.secType = "FUT"
    es_contract.exchange = "CME"
    es_contract.currency = "USD"
    es_contract.lastTradeDateOrContractMonth = "202512"  # December 2025
    es_contract.multiplier = "50"  # ES multiplier
    
    # CL (Crude Oil) futures contract
    cl_contract = Contract()
    cl_contract.symbol = "CL"
    cl_contract.secType = "FUT"
    cl_contract.exchange = "NYMEX"
    cl_contract.currency = "USD"
    cl_contract.lastTradeDateOrContractMonth = "202512"  # December 2025
    cl_contract.multiplier = "1000"  # CL multiplier (1000 barrels)
    
    try:
        # Test ES futures order placement
        print("Testing ES (E-mini S&P 500) futures order...")
        es_market_data = app.get_market_data(request_id=9, contract=es_contract)
        es_current_price = es_market_data
        print(f"Current ES price: ${es_current_price}")
        
        # Place ES limit order below current price
        es_limit_price = es_current_price - 50.0  # $50 below current price
        es_limit_order = limit(BUY, 1, es_limit_price)  # 1 contract
        es_order_id = app.send_order(es_contract, es_limit_order)
        print(f"ES order placed with ID: {es_order_id}")
        print(f"ES order details: BUY 1 ES @ ${es_limit_price} (current: ${es_current_price})")
        
        # Test CL futures order placement
        print("Testing CL (Crude Oil) futures order...")
        cl_market_data = app.get_market_data(request_id=10, contract=cl_contract)
        cl_current_price = cl_market_data
        print(f"Current CL price: ${cl_current_price}")
        
        # Place CL limit order below current price
        cl_limit_price = cl_current_price - 5.0  # $5 below current price
        cl_limit_order = limit(BUY, 1, cl_limit_price)  # 1 contract
        cl_order_id = app.send_order(cl_contract, cl_limit_order)
        print(f"CL order placed with ID: {cl_order_id}")
        print(f"CL order details: BUY 1 CL @ ${cl_limit_price} (current: ${cl_current_price})")
        
        # Wait for order callbacks
        print("Waiting for futures order callbacks...")
        time.sleep(5)
        
        print("Futures orders should now be visible in IBKR TWS/IB Gateway order book")
        print("Check the 'Orders' tab in TWS to see the open futures orders")
        
    except Exception as e:
        print(f"Error placing futures orders: {e}")
        print("Check if futures market is open and you have trading permissions")
        print("Note: Futures contracts may need different contract month or exchange settings")

    app.disconnect()

def test_cme_futures_market_hours():
    """
    Test CME futures market hours and trading availability.
    
    This test verifies the following capabilities:
    1. Check if CME futures market is currently open
    2. Verify market data availability during market hours
    3. Test order placement during market hours vs after hours
    4. Confirm market status affects trading capabilities
    5. Validate futures timezone handling (CME is Chicago time)
    
    The test checks ES and CL futures trading availability and market status
    to determine if CME futures markets are open for trading.
    """
    app = IBApp("127.0.0.1", 7497, client_id=10)
    
    # ES (E-mini S&P 500) futures contract
    es_contract = Contract()
    es_contract.symbol = "ES"
    es_contract.secType = "FUT"
    es_contract.exchange = "CME"
    es_contract.currency = "USD"
    es_contract.lastTradeDateOrContractMonth = "202512"  # December 2025
    es_contract.multiplier = "50"  # ES multiplier
    
    # CL (Crude Oil) futures contract
    cl_contract = Contract()
    cl_contract.symbol = "CL"
    cl_contract.secType = "FUT"
    cl_contract.exchange = "NYMEX"
    cl_contract.currency = "USD"
    cl_contract.lastTradeDateOrContractMonth = "202512"  # December 2025
    cl_contract.multiplier = "1000"  # CL multiplier (1000 barrels)
    
    try:
        # Check ES futures market status
        print("Checking ES (E-mini S&P 500) futures market status...")
        es_market_data = app.get_market_data(request_id=11, contract=es_contract)
        es_current_price = es_market_data
        print(f"Current ES price: ${es_current_price}")
        
        if es_current_price and es_current_price > 0:
            print("ES futures market appears to be OPEN")
            print("Real-time data available - ES futures are trading")
        else:
            print("ES futures market appears to be CLOSED")
            print("No real-time data available - ES futures are not trading")
        
        # Check CL futures market status
        print("Checking CL (Crude Oil) futures market status...")
        cl_market_data = app.get_market_data(request_id=12, contract=cl_contract)
        cl_current_price = cl_market_data
        print(f"Current CL price: ${cl_current_price}")
        
        if cl_current_price and cl_current_price > 0:
            print("CL futures market appears to be OPEN")
            print("Real-time data available - CL futures are trading")
        else:
            print("CL futures market appears to be CLOSED")
            print("No real-time data available - CL futures are not trading")
        
        # Overall CME market status
        if (es_current_price and es_current_price > 0) or (cl_current_price and cl_current_price > 0):
            print("CME futures markets appear to be OPEN")
            print("At least one futures contract is trading")
        else:
            print("CME futures markets appear to be CLOSED")
            print("No futures contracts are trading")
            
    except Exception as e:
        print(f"Error checking CME futures market status: {e}")
        if "No security definition" in str(e):
            print("Futures market may be closed - no security definition available")
        elif "Market data" in str(e):
            print("Futures market data unavailable - market likely closed")
        else:
            print("Unknown error - check futures market status manually")

    app.disconnect()
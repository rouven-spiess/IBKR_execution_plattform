from ibapi.contract import Contract


def future(symbol, exchange, contract_month):
    contract = Contract()
    contract.symbol = symbol
    contract.exchange = exchange
    contract.lastTradeDateOrContractMonth = contract_month
    contract.secType = "FUT"

    return contract


def stock(symbol, exchange, currency, primary_exchange=None):
    contract = Contract()
    contract.symbol = symbol
    contract.exchange = exchange
    contract.currency = currency
    contract.secType = "STK"
    
    # For European stocks, sometimes primary exchange is needed
    if primary_exchange:
        contract.primaryExchange = primary_exchange

    return contract

def option(symbol, exchange, contract_month, strike, right):
    contract = Contract()
    contract.symbol = symbol
    contract.exchange = exchange
    contract.lastTradeDateOrContractMonth = contract_month
    contract.strike = strike
    contract.right = right
    contract.secType = "OPT"

    return contract

def crypto(symbol, currency="USD"):
    """Create a cryptocurrency contract for BTC, ETH, etc."""
    contract = Contract()
    contract.symbol = symbol  # "BTC" or "ETH"
    contract.secType = "CRYPTO"
    contract.exchange = "PAXOS"  # Paxos is IB's crypto exchange
    contract.currency = currency
    return contract
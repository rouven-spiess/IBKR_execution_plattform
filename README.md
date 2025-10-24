# IBKR execution plattform

## Introduction
Testing options for HFT on IBKR TWS Api with an objective of several hundreds of trades/second

## Inspiration
Python for Algorithmic Trading Cookbook
https://github.com/PacktPublishing/Python-for-Algorithmic-Trading-Cookbook

## Testing

Run the test suit with

``` python -m pytest test/test_futures.py -v```


## Result
HIGH-FREQUENCY PERFORMANCE ANALYSIS:
❌ POOR: High-frequency performance < 50 trades/second
✅ EXCELLENT: Low latency <= 50ms


## Todo
- [ ] test if test_stocks_basic functions DONT work when exchange is closed
- [ ] Monitoring Live Orders
- [ ] Querying Your Accounts
- [ ] Querying Currency BalancesCopy Location
- [ ] Querying Equity and Margin
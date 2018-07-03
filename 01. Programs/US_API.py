from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order

ibConnection = None


def operate(orderId,ticker, action, quantity, price=None):  # None price for Market(or limit) operation
    # 1. Construct contract
    contract = Contract()
    contract.m_symbol = ticker
    contract.m_secType = 'STK'  # for stock
    contract.m_exchange = 'ISLAND'
    # contract.m_primaryExch = 'ISLAND'  # for NASDAQ
    contract.m_currency = 'USD'

    # 2. Construct order
    order = Order()
    if price is None:
        order.m_orderType = 'MKT'
    else:
        order.m_orderType = 'LMT'
        order.m_lmPrice = price
    order.m_totalQuantity = quantity
    order.m_action = action

    # 3. Place order
    ibConnection.placeOrder(orderId, contract, order)  # smaller ID has Higher priority




# 1. Establish connection
ibConnection = Connection.create(port=7497, clientId=308)
ibConnection.connect()


# 2. Buy
operate(orderId=20, ticker='NVDA', action='SELL', quantity=100)
operate(orderId=21, ticker='TSLA', action='SELL', quantity=100)


# 3. Disconnect
ibConnection.disconnect()

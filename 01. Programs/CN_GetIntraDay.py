import tushare
import pandas
import datetime
import os
import time


def stock_price_intraday(ticker, folder):
    # get intraday online
    intraday = tushare.get_hist_data(ticker, ktype='5')

    # append if the history exists
    file = folder + '/' + ticker + '.csv'
    if os.path.exists(file):
        history = pandas.read_csv(file, index_col=0)
        intraday.append(history)

    # inverse
    intraday.sort_index(inplace=True)
    intraday.index.name = 'timestamp'

    # Save
    intraday.to_csv(file)
    print('Intraday for [' + ticker + '] got')

# step 1. Get tickers Online
tickersRawData = tushare.get_stock_basics()
tickers = tickersRawData.index.tolist()

# step 2. Save the ticker list to a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '../02. Data/00. TickerListCN/TickerList_' + dateToday + '.csv'
tickersRawData.to_csv(file)
print('Tickers_saved')

# get Intraday for stocks
for i, ticker in enumerate(tickers):
    try:
        print('Intraday', i, '/', len(tickers))
        stock_price_intraday(ticker, folder='../02. Data/01. IntradayCN')
        time.sleep(2)
    except:
        pass

print("Intraday for all stocks got")

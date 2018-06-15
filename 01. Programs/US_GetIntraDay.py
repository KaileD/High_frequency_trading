import requests
import pandas
import io
import datetime
import os
import time


def dateframeFromUrl(url):
    dataString = requests.get(url).content
    parsedResult = pandas.read_csv(io.StringIO(dataString.decode("utf-8")), index_col=0)
    return parsedResult


def stockPriceIntraday(ticker, folder):
    # get data online
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}' \
          '&interval=1min&outputsize=full&apikey=P2CRGWRDNB94PYKS&datatype=csv'.format(ticker=ticker)
    intraday = dateframeFromUrl(url)

    # append if history exists
    file = folder + '/' +ticker+'.csv'
    if os.path.exists(file):
        history = pandas.read_csv(file, index_col=0)
        intraday.append(history)

    # inverse
    intraday.sort_index(inplace=True)

    # save
    intraday.to_csv(file)
    print('intraday for [' + ticker + '] got')


# Get tickers online
url = 'https://www.nasdaq.com/screening/companies-by-industry.aspx?&render=download'
dataString = requests.get(url).content
tickersRawData = pandas.read_csv(io.StringIO(dataString.decode("utf-8")))
tickers = tickersRawData['Symbol'].tolist()

# Save it into a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '../02. Data/00. TickerListUS/TickerList_' + dateToday + '.csv'
tickersRawData.to_csv(file, index=False)
print('tickers saved')

# get intraday
for i, ticker in enumerate(tickers):
    try:
        print('Intraday', i, '/', len(tickers))
        stockPriceIntraday(ticker, folder='../02. Data/01. IntradayUS')
    except:
        pass
    time.sleep(1)
    # if i > 3:
    #    break
print('Intraday for all stocks got.')
import tushare
import pandas
import datetime

# step 1. Get tickers Online
tickersRawData = tushare.get_stock_basics()  # DataFrame
tickers = tickersRawData.index.tolist()

# step 2. Save the ticker list to a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '/Users/Kyle/Desktop/THE project/02. Data/00. TickerListCN/TickerList_' + dateToday + '.csv'
tickersRawData.to_csv(file)
print('Tickers_saved')

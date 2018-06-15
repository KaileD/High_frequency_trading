import requests
import pandas
import io
import datetime


# Get tickers online
url = 'https://www.nasdaq.com/screening/companies-by-industry.aspx?&render=download'
dataString = requests.get(url).content
tickersRawData = pandas.read_csv(io.StringIO(dataString.decode("utf-8")))
tickers = tickersRawData['Symbol'].tolist()
print(tickersRawData)

# Save it into a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '../02. Data/00. TickerListUS/TickerList_' + dateToday + '.csv'
tickersRawData.to_csv(file, index=False)
print('tickers saved')
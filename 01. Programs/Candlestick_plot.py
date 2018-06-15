import pandas
import matplotlib
import matplotlib.finance
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')
# matplotlib.style.use('dark_background')


def stock_price_plot(ticker):
    # get data
    history = pandas.read_csv('../02. Data/01. IntradayUS/' + ticker + '.csv', parse_dates=True, index_col=0)

    # data manipulation
    close = history['close']
    close = close.reset_index()
    close['timestamp'] = close['timestamp'].map(matplotlib.dates.date2num)

    ohlc = history[['open', 'high', 'low', 'close']].resample('1H').ohlc()
    ohlc = ohlc.reset_index()
    ohlc['timestamp'] = ohlc['timestamp'].map(matplotlib.dates.date2num)

    # scatter plot
    plot1 = plt.subplot2grid((2, 1), (0, 0), rowspan=1, colspan=1)
    plot1.xaxis_date()
    plot1.plot(close['timestamp'], close['close'], 'b.')
    plt.title(ticker)

    # candle stick plot
    plot2 = plt.subplot2grid((2, 1), (1, 0), rowspan=1, colspan=1, sharex=plot1)
    matplotlib.finance.candlestick_ohlc(ax=plot2, quotes=ohlc.values, width=0.01, colorup='g', colordown='r')

    plt.show()


ticker = input("Which stock?: ")
stock_price_plot(ticker)

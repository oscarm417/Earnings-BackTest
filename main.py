import data_getter as dg
import pandas as pd
from portfolio import Security, Calendar
import earnings_scraper as es
import calculators
import matplotlib.pyplot as plt

"""
def main():

    port = Portfolio(
        symbols = tickers,
        start_Dt = start_dt,
        calendar_type = cal_type,
        data_src = dataSource,
        )



if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT']
    start_dt = '2005-01-01'
    cal_type = earnings_scraper.Yahoo
    dataSource = DataSource.CSV_Data





"""
ticker = 'AAPL'
start_date = '2015-01-01'
cal_type = Calendar(scraper=es.CSV('testEarnings.csv'), start_dt=start_date)
dat_src = dg.CSV_Data('data.csv')
moneyn = 100
stock = Security(symbol=ticker, moneyness=moneyn,
                 calendar=cal_type, data_source=dat_src)

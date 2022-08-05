from __future__ import annotations
from typing import List, Dict, Tuple
import pandas as pd
#from data_getter import *
import data_getter
from calculators import OptionCalculator, PNLCalculator
import numpy as np
from earnings_scraper import EarningsScraper
from datetime import datetime
from blackscholes import black_scholes
import matplotlib.pyplot as plt
#from data_getter import DataSource


class Calendar:
    def __init__(
        self,
        scraper: EarningsScraper,
        start_dt: str,
    ) -> None:

        self.df = scraper.get_dates(start_dt)

    def get_security_calendar(self, symbol: str) -> pd.DataFrame:
        return self.df[symbol]


class Security:
    def __init__(
        self,
        symbol: str,
        moneyness: float,
        calendar: Calendar,
        data_source: DataSource,
    ) -> None:
        self.symbol = symbol.upper()
        self.moneyness = moneyness
        self.calendar = calendar.get_security_calendar(self.symbol)
        self.df = pd.DataFrame
        self.pnl = 0
        self.runPNL = pd.Series()
        self.notional_exp = 1000000
        self.merge_spot_price(data_source)
        self.merge_rates(data_source)
        self.merge_strikes(data_source)
        self.merge_ivol(data_source, right='c')
        self.merge_ivol(data_source, right='p')
        self.merge_earnings()
        self.merge_weekday(data_source)
        self.merge_maturity(data_source)
        self.mark_orders()
        self.merge_num_contracts()
        OptionCalculator(self)  # ! reassignment
        self.calc_total_price()
        PNLCalculator(self)  # ! reassignment
        print(self.df[self.df['transaction'].isin(['sell', 'buy'])])
        self.df['run_pnl'].plot()
        plt.show()

    def mark_orders(self) -> None:

        self.df['transaction'] = np.nan
        # buy
        # buy orders
        self.df['transaction'] = np.where(
            (self.df[self.symbol] == "BMO").shift(-1), "buy", (np.where(
                self.df[self.symbol] == 'AMC', 'buy', self.df['transaction'])))

        # sell
        self.df['transaction'].mask(
            (self.df[self.symbol] == 'BMO') |
            (self.df[self.symbol] == 'AMC').shift(1),
            'sell',
            inplace=True,
        )

    def merge_earnings(self) -> None:
        self.df = pd.concat([self.df, self.calendar], axis=1)

    def merge_spot_price(self, data_source: DataSource) -> None:
        new_col = data_source.get_spot_price().rename('spot')
        self.df = new_col

    def merge_num_contracts(self) -> None:

        self.df['num_contracts'] = round(self.notional_exp / self.df['spot'],
                                         2)
        #making buy and sell have the contract amounts
        self.df['num_contracts'].mask(self.df['transaction'] == 'buy',
                                      (self.df['num_contracts']).shift(-1),
                                      inplace=True)

    def merge_ivol(self, data_source: DataSource, right: str) -> None:
        new_col = data_source.get_ivol().rename(right + '_ivol')
        self.df = pd.concat([self.df, new_col], axis=1)

    def merge_strikes(self, data_source: DataSource) -> None:
        new_col = data_source.get_strikes(self.moneyness).rename('strike')
        self.df = pd.concat([self.df, new_col], axis=1)

    def merge_rates(self, data_source: DataSource) -> None:
        new_col = data_source.get_rates().rename('rates')
        self.df = pd.concat([self.df, new_col], axis=1)

    def merge_weekday(self, data_source: DataSource) -> None:
        new_col = data_source.get_weekday().rename('weekday')
        self.df = pd.concat([self.df, new_col], axis=1)

    def merge_maturity(self, data_source: DataSource) -> None:
        new_col = data_source.get_maturity().rename('maturity')
        self.df = pd.concat([self.df, new_col], axis=1)
        #Buys on Friday for BMO on Monday
        self.df['maturity'].mask((self.df[self.symbol] == 'BMO').shift(-1) &
                                 (self.df['maturity'] == 0),
                                 7,
                                 inplace=True)

    def calc_delta(
        self,
        calculator: OptionCalculator,
        df: pd.DataFrame,
        right: str,
    ) -> None:
        self.df = calculator.calculate_delta(df, right)

    def calc_vega(
        self,
        calculator: OptionCalculator,
        df: pd.DataFrame,
        right: str,
    ) -> None:
        self.df = calculator.calculate_vega(df, right)

    def calc_gamma(
        self,
        calculator: OptionCalculator,
        df: pd.DataFrame,
        right: str,
    ) -> None:
        self.df = calculator.calculate_gamma(df, right)

    def calc_theta(
        self,
        calculator: OptionCalculator,
        df: pd.DataFrame,
        right: str,
    ) -> None:
        self.df = calculator.calculate_theta(df, right)

    def calc_rho(
        self,
        calculator: OptionCalculator,
        df: pd.DataFrame,
        right: str,
    ) -> None:
        self.df = calculator.calculate_rho(df, right)

    def calc_opt_price(
        self,
        calculator: OptionCalculator,
        df: pd.DataFrame,
        right: str,
    ) -> None:
        self.df = calculator.calculate_opt_price(df, right)

    def calc_total_price(self):
        self.df['total_price'] = self.df['c_price'] + self.df['p_price']

    def calc_pnl(self, calculator: PNLCalculator, df: pd.DataFrame) -> None:
        self.df = calculator.calculator_pnl(df)

    def calc_run_pnl(self, calculator: PNLCalculator,
                     df: pd.DataFrame) -> None:
             self.df = calculator.running_pnl(df)

        #pd.concat([self.df, new_col], axis = 1)


"""

class Portfolio:

    def __init__(
        self, 
        symbols: List[str], 
        moneyness: float,
        start_dt: str,
        calendar_type: EarningsScraper,
        data_src: 'DataSource',
    ) -> None:

        #self.earn_cal: pd.DataFrame = get_earnings_calendar()# call the real func
        self.securities: Dict[str, Security] = {}
        self.moneyness = moneyness
        self.earnings_cal = Calendar(calendar_type, start_dt)
        self.data_src = DataSource

        for sym in symbols:
            self.securities.update({
                sym: Security(
                    symbol=sym, 
                    moneyness = self.moneyness,
                    calendar=self.earnings_cal.get_security_calendar(sym),
                    data_source= self.data_src(symbol=sym),
                    )
                })

        for sym in symbols:
            self.





"""

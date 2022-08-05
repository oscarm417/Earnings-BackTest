from abc import ABC, abstractmethod
import pandas as pd
import portfolio
import numpy as np


class DataSource(ABC):
    def __init__(self, security: portfolio.Security) -> None:
        security.merge_spot_price(self)
        security.merge_ivol(self, right='P')
        security.merge_ivol(self, right='C')
        security.merge_strikes(self)
        security.merge_rates(self)
        security.merge_weekday(self)
        security.merge_maturity(self)

    @abstractmethod
    def get_spot_price(self) -> pd.Series:
        return pd.Series()

    @abstractmethod
    def get_ivol(self) -> pd.Series:
        return pd.Series()

    @abstractmethod
    def get_strikes(self, moneyness: float) -> pd.Series:
        return pd.Series()

    @abstractmethod
    def get_rates(self) -> pd.Series:
        return pd.Series()

    @abstractmethod
    def get_maturity(self) -> pd.Series:
        return pd.Series()

    # ! is this necessary? where does it belong
    @abstractmethod
    def get_weekday(self) -> pd.Series:
        return pd.Series()


class IB_Data(DataSource):
    def __init__(self) -> None:
        conn_obj = ""

    def get_spot_price(self) -> pd.Series:
        return pd.Series()

    def get_ivol(self) -> pd.Series:
        return pd.Series()


class GCP_Data(DataSource):
    def __init__(self) -> None:
        conn_obj = ""

    def get_spot_price(self) -> pd.Series:
        # psudo code
        return pd.Series()

    def get_ivol(self) -> pd.Series:
        return pd.Series()


class CSV_Data(DataSource):
    def __init__(self, fileName) -> None:
        self.df = pd.read_csv(fileName)
        self.df.set_index('Date', inplace=True)
        self.df.index = pd.to_datetime(
            pd.to_datetime(
                self.df.index,
                errors='coerce',
            ).strftime('%Y-%m-%d'),
            format='%Y-%m-%d',
        )

    def get_spot_price(self) -> pd.Series:
        stockPrices = self.df['spot']
        return stockPrices

    def get_ivol(self) -> pd.Series:
        stockVol = self.df['vol']
        return stockVol

    def get_strikes(self, moneyness: float) -> pd.Series:
        optionStrikes = (moneyness / 100) * self.df['spot']
        #optionStrikes = pd.read_csv(fileName)
        # return pd.Series()
        return optionStrikes

    def get_rates(self) -> pd.Series:
        rates = self.df['rate']
        return rates

    def get_weekday(self) -> pd.Series:
        self.df['weekday'] = self.df.index
        self.df['weekday'] = self.df['weekday'].apply(
            lambda x: x.date().weekday())
        self.df = self.df[self.df['weekday'].notna()]
        return self.df['weekday']

    def get_maturity(self) -> pd.Series:
        """
        Need to built function to get tradable
        strikes[time to maturity,]
        """
        self.df['maturity'] = self.df['weekday'].apply(lambda x: 4 - x)
        return self.df['maturity']
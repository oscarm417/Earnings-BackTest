from abc import ABC, abstractmethod
from yahoo_scrapper import YahooEarningsCalendar
import pandas as pd
import datetime 
import dateutil.parser



class EarningsScraper(ABC):
    """
    Calendar must return not only earnings dates, but a full time series
    of all market dates as the index with a column named "earnings call time"
    that has a flags: BMO, AMC, etc.
    """
    
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_dates(self, symbol: str) -> pd.DataFrame:
        return pd.DataFrame

class Yahoo(EarningsScraper):

    def get_dates(self, start_dt: str) -> pd.DataFrame:
        """
        yec = YahooEarningsCalendar()
        end_dt = datetime.datetime.now().strftime("%Y-%m-%d")
        earnings_list = yec.earnings_between(start_dt,end_dt)
        earnings_df = pd.DataFrame(earnings_list)
        earnings_df['Date'] = earnings_df['startdatetime'].apply(lambda x: dateutil.parser.isoparse(x).date())
        earnings_df = earnings_df.sort_values('Date')
        #remove non reported earnings for todays earnings
        earnings_df = earnings_df[earnings_df['epsactual'].notnull()]
        earnings_df.rename(columns ={'startdatetime':'earnings_time'}, inplace=True)
        earnings_df = earnings_df[earnings_df['Date'].notnull() == True].set_index('Date')
        return earnings_df
        """
        pass
    
class Nasdaq(EarningsScraper):
    def get_dates(self,start_df: str) -> pd.DataFrame:
        pass
     
class GCP(EarningsScraper):
    def get_dates(self,start_df: str) -> pd.DataFrame:
        pass

class Fidelity(EarningsScraper):
    def get_dates(self,start_df: str) -> pd.DataFrame:
        pass

class CSV(EarningsScraper):
    def __init__(self,fileName:str) -> None:
        self.earnings_df = pd.read_csv(fileName)
        self.earnings_df.set_index('Date', inplace = True)
        self.earnings_df.index = pd.to_datetime(self.earnings_df.index, format ="%Y-%m-%d" )
    def get_dates(self, start_dt: str) -> pd.DataFrame:
        startTime = datetime.datetime.strptime(start_dt,'%Y-%m-%d').date()
        earnings_df = self.earnings_df.loc[startTime:]
        return earnings_df
 



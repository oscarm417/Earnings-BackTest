from numpy.lib.shape_base import get_array_prepare
import pandas as pd
import datetime
import numpy as np
import portfolio
from blackscholes import black_scholes


class OptionCalculator:
    def __init__(self, security: 'Security') -> None:
        notional_exp = 1000000
        self.num_contracts = notional_exp / security.df['spot']
        security.calc_delta(self, df=security.df, right='p')
        security.calc_delta(self, df=security.df, right='c')
        security.calc_vega(self, df=security.df, right='p')
        security.calc_vega(self, df=security.df, right='c')
        security.calc_gamma(self, df=security.df, right='p')

        security.calc_gamma(self, df=security.df, right='c')
        security.calc_theta(self, df=security.df, right='p')
        security.calc_theta(self, df=security.df, right='c')
        security.calc_rho(self, df=security.df, right='p')
        security.calc_rho(self, df=security.df, right='c')
        security.calc_opt_price(self, df=security.df, right='p')
        security.calc_opt_price(self, df=security.df, right='c')
        

        """
        Parameters:
        K : Excercise Price X
        St: Current Stock Price X
        v : Volatility in percentage X
        r : Risk free rate in percentage X
        t : Time to expiration in days 
        type: Type of option 'c' for call 'p' for put
        default: 'c'
        """

    def calculate_delta(self, df, right) -> pd.Series:
        df[right + "_delta"] = np.nan
        # buys
        df[right + "_delta"].mask(df['transaction'] == 'buy',
                                  round(
                                      black_scholes(
                                          df['spot'],
                                          df['strike'],
                                          df['rates'],
                                          df[right + '_ivol'],
                                          df['maturity'],
                                          right,
                                      ).delta() * df['num_contracts'], 2),
                                  inplace=True)

        # sells
        df[right + "_delta"].mask(df['transaction'] == 'sell',
                                  round(
                                      black_scholes(
                                          df['spot'],
                                          df['strike'].shift(1),
                                          df['rates'],
                                          df[right + '_ivol'],
                                          df['maturity'],
                                          right,
                                      ).delta() * df['num_contracts'], 2),
                                  inplace=True)

        return df

    def calculate_vega(self, df, right) -> pd.Series:

        df[right + "_vega"] = np.nan
        # buys
        df[right + "_vega"].mask(df['transaction'] == 'buy',
                                 round(
                                     black_scholes(
                                         df['spot'],
                                         df['strike'],
                                         df['rates'],
                                         df[right + '_ivol'],
                                         df['maturity'],
                                         right,
                                     ).vega() * df['num_contracts'], 2),
                                 inplace=True)

        # sells
        df[right + "_vega"].mask(df['transaction'] == 'sell',
                                 round(
                                     black_scholes(
                                         df['spot'],
                                         df['strike'].shift(1),
                                         df['rates'],
                                         df[right + '_ivol'],
                                         df['maturity'],
                                         right,
                                     ).vega() * df['num_contracts'], 2),
                                 inplace=True)
        return df

    def calculate_gamma(self, df, right) -> pd.Series:
        df[right + "_gamma"] = np.nan
        df[right + "_gamma"].mask(df['transaction'] == 'buy',
                                  round(
                                      black_scholes(
                                          df['spot'],
                                          df['strike'],
                                          df['rates'],
                                          df[right + '_ivol'],
                                          df['maturity'],
                                          right,
                                      ).gamma() * df['num_contracts'], 2),
                                  inplace=True)

        df[right + "_gamma"].mask(df['transaction'] == 'sell',
                                  round(
                                      black_scholes(
                                          df['spot'],
                                          df['strike'].shift(1),
                                          df['rates'],
                                          df[right + '_ivol'],
                                          df['maturity'],
                                          right,
                                      ).gamma() * df['num_contracts'], 2),
                                  inplace=True)

        return df

    def calculate_theta(self, df, right) -> pd.Series:
        df[right + "_theta"] = np.nan
        # buys
        df[right + "_theta"].mask(df['transaction'] == 'buy',
                                  round(
                                      black_scholes(
                                          df['spot'],
                                          df['strike'],
                                          df['rates'],
                                          df[right + '_ivol'],
                                          df['maturity'],
                                          right,
                                      ).theta() * df['num_contracts'], 2),
                                  inplace=True)

        # sells
        df[right + "_theta"].mask(df['transaction'] == 'sell',
                                  round(
                                      black_scholes(
                                          df['spot'],
                                          df['strike'].shift(1),
                                          df['rates'],
                                          df[right + '_ivol'],
                                          df['maturity'],
                                          right,
                                      ).theta() * df['num_contracts'], 2),
                                  inplace=True)

        return df

    def calculate_rho(self, df, right) -> pd.Series:
        df[right + "_rho"] = np.nan
        # buys
        df[right + "_rho"].mask(df['transaction'] == 'buy',
                                round(
                                    black_scholes(
                                        df['spot'],
                                        df['strike'],
                                        df['rates'],
                                        df[right + '_ivol'],
                                        df['maturity'],
                                        right,
                                    ).rho() * df['num_contracts'], 2),
                                inplace=True)

        #sells
        df[right + "_rho"].mask(df['transaction'] == 'sell',
                                round(
                                    black_scholes(
                                        df['spot'],
                                        df['strike'].shift(1),
                                        df['rates'],
                                        df[right + '_ivol'],
                                        df['maturity'],
                                        right,
                                    ).rho() * df['num_contracts'], 2),
                                inplace=True)

        return df

    def calculate_opt_price(self, df, right) -> pd.Series:
        df[right + "_price"] = np.nan
        # buys
        df[right + "_price"].mask(df['transaction'] == 'buy',
                                  round(
                                      black_scholes(
                                          df['spot'],
                                          df['strike'],
                                          df['rates'],
                                          df[right + '_ivol'],
                                          df['maturity'],
                                          right,
                                      ).value() * df['num_contracts'], 2),
                                  inplace=True)

        # sells
        df[right + "_price"].mask(df['transaction'] == 'sell',
                                  round(
                                      black_scholes(
                                          df['spot'],
                                          df['strike'].shift(1),
                                          df['rates'],
                                          df[right + '_ivol'],
                                          df['maturity'],
                                          right,
                                      ).value() * df['num_contracts'], 2),
                                  inplace=True)

        return df


class PNLCalculator:
    def __init__(self, security: 'Security') -> None:
        security.calc_pnl(self, df=security.df)
        security.calc_run_pnl(self, df=security.df)

    def calculator_pnl(self, df) -> pd.Series:
        df['pnl'] = np.where(
            df['transaction'] == 'buy', 0,
            np.where(
                df['transaction'] == 'sell',
                (df['total_price'].shift(1) - df['total_price']),
                0,
            ))
        return df

    def running_pnl(self, df) -> pd.Series:
        df['run_pnl'] = df['pnl'].cumsum()
        return df

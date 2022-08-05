import numpy as np
from scipy.stats import norm


class black_scholes(object):
    def __init__(self, St=62, K=60, r=4.00, v=32.00, t=40, right='c'):
        """
        Parameters:
        K : Excercise Price
        St: Current Stock Price
        v : Volatility in percentage
        r : Risk free rate in percentage
        t : Time to expiration in days
        type: Type of option 'c' for call 'p' for put
        default: 'c'
        """

        self.right = right.lower()
        self.t = np.maximum(t / 365, 0)
        self.r = r / 100
        self.v = v / 100
        self.St = St + 0
        self.K = K + 0

        n1 = np.log(self.St / self.K)
        n2 = (self.r + (np.power(self.v, 2) / 2)) * self.t
        d = self.v * (np.sqrt(self.t))

        self.d1 = (n1 + n2) / d
        self.d1 = np.where(self.t == 0, 0, (n1 + n2) / d)
        self.d2 = self.d1 - (self.v * np.sqrt(self.t))

        if self.right == 'c':
            self.N_d1 = norm.cdf(self.d1)
            self.N_d2 = norm.cdf(self.d2)
        else:
            self.N_d1 = norm.cdf(-self.d1)
            self.N_d2 = norm.cdf(-self.d2)

    def value(self):
        A = (self.St * self.N_d1)
        B = (self.K * self.N_d2 * (np.exp(-self.r * self.t)))
        if self.right == 'c':
            val = A - B
        else:
            val = B - A
        return val

    def delta(self):

        if self.right == 'c':
            return self.N_d1
        else:
            return -self.N_d1

    def theta(self):
        if self.right == 'c':
            theta_val = (-(
                (self.St * self.v * np.exp(-np.power(self.d1, 2) / 2)) /
                (np.sqrt(8 * np.pi * self.t))) -
                         (self.N_d2 * self.r * self.K *
                          np.exp(-self.r * self.t))) / 3655
        else:
            theta_val = (
                -((self.St * self.v * np.exp(-np.power(self.d1, 2) / 2)) /
                  (np.sqrt(8 * np.pi * self.t))) +
                (self.N_d2 * self.r * self.K * np.exp(-self.r * self.t))) / 365
        return theta_val

    def rho(self):
        if self.right == 'c':
            rho_val = self.t * self.K * self.N_d2 * \
                np.exp(-self.r * self.t) / 100
        else:
            rho_val = self.t * self.K * self.N_d2 * \
                np.exp(-self.r * self.t) / 100
        return rho_val

    def gamma(self):
        gam = (np.exp(-np.power(self.d1, 2) /
                      2)) / (self.St * self.v * np.sqrt(2 * np.pi * self.t))
        return gam

    def vega(self):
        vega_val = (self.St * np.sqrt(self.t) * np.exp(
            -np.power(self.d1, 2) / 2)) / (np.sqrt(2 * np.pi) * 100)
        return vega_val


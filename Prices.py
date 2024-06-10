
import numpy as np


# Here we will have functions to retrieve prices for our proposed 'inventory' strategy
class InventoryStrategy:
    def __init__(self, prices, sigma=2, theta=0.1, k=1.5, A=140, dt=0.005, T=1) -> None:
        self.prices = prices # prices
        self.spreads = [] # here we will save spreads for use in benchmark strategy
        self.sigma = sigma # stock's volatility
        self.theta = theta # risk aversion parameter
        self.k = k # parameter for the arrival rate function
        self.A = A # parameter for the arrival rate function
        self.dt = dt # time resolution parameter
        self.T = T # terminal time
        self.inventory = 0 # current inventory
        self.pnl = 0 # current pnl

    # get bid and ask for a given moment
    def calculate_bid_ask(self, mid_price, t):
        reservation_price = mid_price - self.inventory * self.theta * (self.sigma**2) * (self.T - t)
        spr = self.theta*(self.sigma**2)*(self.T - self.dt) + (2/self.theta)*np.log(1 + (self.theta/self.k))
 
        bid_price = reservation_price - spr/2
        ask_price = reservation_price + spr/2

        self.spreads.append(ask_price - bid_price)
        
        return bid_price, ask_price
    
    # update inventory for a given moment
    def update_inventory(self, ask, bid, mid_price, t):

        lambda_a = self.A * np.exp(-self.k * (ask - mid_price))
        lambda_b = self.A * np.exp(-self.k * (mid_price - bid))
        
        if np.random.rand() < lambda_b * self.dt:
            self.inventory += 1
            self.pnl -= bid
        
        if np.random.rand() < lambda_a * self.dt:
            self.inventory -= 1
            self.pnl += ask

    def get_average_spread(self):
        return sum(self.spreads)/len(self.spreads)
    
    def run_strategy(self):
        t = 0
        ask = None
        bid = None
        for price in self.prices:
            if ask:
                self.update_inventory(ask, bid, price, t)
            bid, ask = self.calculate_bid_ask(price, t)
            t += self.dt

        self.pnl += self.inventory*self.prices[-1]

        return self.pnl, self.inventory
    
    def reset(self, prices=None):
        self.inventory = 0
        self.pnl = 0
        self.spreads = []
        if prices:
            self.prices = prices


# Benchmark strategy uses symmetric bid/ask spread where spread is the average spread of the 'inventory' strategy
class BenchmarkStrategy:
    def __init__(self, prices, spread, A=140, k=1.5, dt=0.005):
        self.prices = prices  # stock prices
        self.spread = spread  # spread to be used - in the paper it was avg spread of the other strategy
        self.inventory = 0
        self.pnl = 0
        self.A = A  
        self.k = k  
        self.dt = dt  
    
    # get bid and ask for a given moment
    def calculate_bid_ask(self, price):
        return price - self.spread / 2, price + self.spread / 2

    # update inventory for a given moment
    def update_inventory(self, bid, ask, price):
        
        lambda_a = self.A * np.exp(-self.k * (ask - price))
        lambda_b = self.A * np.exp(-self.k * (price - bid))
        
        if np.random.rand() < lambda_b * self.dt:
            self.inventory += 1
            self.pnl -= bid
        
        if np.random.rand() < lambda_a * self.dt:
            self.inventory -= 1
            self.pnl += ask

    # get pnl for a single simulation
    def run_strategy(self):
        bid = None
        ask = None
        for price in self.prices:
            if ask:
                self.update_inventory(bid, ask, price)
            bid, ask = self.calculate_bid_ask(price)

        self.pnl += self.inventory*self.prices[-1]

        return self.pnl, self.inventory
    
    # reset class between runs
    def reset(self, spread, prices=None):
        self.inventory = 0
        self.pnl = 0
        self.spread = spread
        if prices:
            self.prices = prices


    
    
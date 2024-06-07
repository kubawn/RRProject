from Prices import InventoryStrategy, BenchmarkStrategy
from RandomWalk import simulate_mid_price
import matplotlib.pyplot as plt
import numpy as np
import time

# Get the current Unix timestamp
current_time = int(time.time())

# Set the NumPy random seed using the current Unix timestamp
np.random.seed(current_time)

res_inv = []
res_bench = []

prices = simulate_mid_price(100, 2, 1, 0.005) 

for i in range(1000):
    inv = InventoryStrategy(prices=prices)
    res_inv.append(inv.run_strategy())
    bench = BenchmarkStrategy(prices=prices, spread=inv.get_average_spread())
    res_bench.append(bench.run_strategy())

num_bins = 20

# Plot histograms
plt.hist(res_inv, bins=num_bins, alpha=0.5, label='Inventory Strategy PnL')
plt.hist(res_bench, bins=num_bins, alpha=0.5, label='Benchmark Strategy PnL')

# Add labels and legend
plt.xlabel('PnL Values')
plt.ylabel('Frequency')
plt.title('Histogram of Inventory and Benchmark Strategies PnLs')
plt.legend(loc='upper right')

# Show plot
plt.show()

print(sum(res_inv)/len(res_inv))
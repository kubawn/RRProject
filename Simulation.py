from Prices import InventoryStrategy, BenchmarkStrategy
from RandomWalk import simulate_mid_price
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

def calculate_statistics(pnls):
    mean_pnl = np.mean(pnls)
    std_pnl = np.std(pnls)
    median_pnl = np.median(pnls)
    max_drawdown = np.min(pnls)
    return mean_pnl, std_pnl, median_pnl, max_drawdown

def create_comparison_table(res_inv, res_ben, inv_inv, inv_ben):
    # Calculate statistics for both strategies
    stats_inv = calculate_statistics(res_inv)
    stats_ben = calculate_statistics(res_ben)
    stats_inv2 = calculate_statistics(inv_inv)
    stats_ben2 = calculate_statistics(inv_ben)
    
    # Create a DataFrame
    data = {
        'Strategy': ['Inventory', 'Benchmark'],
        'Mean PnL': [stats_inv[0], stats_ben[0]],
        'StDev': [stats_inv[1], stats_ben[1]],
        'Final Inventory': [stats_inv2[0], stats_ben2[0]],
        'StDev(q)': [stats_inv2[1], stats_ben2[1]],
    }
    
    df = pd.DataFrame(data)
    return df

def run_simulation(n, theta=0.1):
    np.random.seed(int(time.time()))

    res_inv = []
    res_bench = []
    inv_inv = []
    inv_bench = []

    prices = simulate_mid_price(100, 2, 1, 0.005) 

    for i in range(n):
        inv = InventoryStrategy(prices=prices, theta=theta)
        pnl, f_inv = inv.run_strategy()
        res_inv.append(pnl)
        inv_inv.append(f_inv)
        bench = BenchmarkStrategy(prices=prices, spread=inv.get_average_spread())
        pnl, f_inv = bench.run_strategy()
        inv_bench.append(f_inv)
        res_bench.append(pnl)

    # Combine the PnL data to get the common range for bins
    all_pnls = res_inv + res_bench
    num_bins = 40
    bins = np.linspace(min(all_pnls), max(all_pnls), num_bins)

    # Plot histograms
    plt.hist(res_inv, bins=bins, alpha=0.5, label='Inventory Strategy PnL')
    plt.hist(res_bench, bins=bins, alpha=0.5, label='Benchmark Strategy PnL')

    # Add labels and legend
    plt.xlabel('PnL Values')
    plt.ylabel('Frequency')
    plt.title('Histogram of Inventory and Benchmark Strategies PnLs')
    plt.legend(loc='upper right')

    # Show plot
    plt.show()

    print(create_comparison_table(res_inv, res_bench, inv_inv, inv_bench))
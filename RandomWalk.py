import numpy as np
import matplotlib.pyplot as plt
import time

current_time = int(time.time())
np.random.seed(current_time)

def simulate_mid_price(S0, sigma, T, dt):
    table = [1, -1]
    N = int(T / dt)  # Number of time steps
    S = np.zeros(N)
    S[0] = S0
    
    for t in range(1, N):
        S[t] = S[t-1] + sigma * np.random.choice(table) * np.sqrt(dt) 
        # ^ I changed this because I think this is what they mean in 3.3 paragraph number 3
        
    return S

# I commented this out for now because this gets executed during import in other file 

# Parameters
# S0 = 100  # Initial stock price
# sigma = 0.2  # Volatility
# T = 1.0  # Total time period (e.g., 1 year)
# dt = 0.01  # Time step (e.g., daily steps)

# Simulate mid-price
# mid_price = simulate_mid_price(S0, sigma, T, dt)

# Plot the results
# plt.plot(mid_price)
# plt.title("Simulated Mid-Price of Stock")
# plt.xlabel("Time Steps")
# plt.ylabel("Price")
# plt.show()

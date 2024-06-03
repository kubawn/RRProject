import numpy as np
import matplotlib.pyplot as plt

def simulate_mid_price(S0, sigma, T, dt):
    
    N = int(T / dt)  # Number of time steps
    W = np.random.normal(0, np.sqrt(dt), N)  # Brownian increments
    S = np.zeros(N)
    S[0] = S0
    
    for t in range(1, N):
        S[t] = S[t-1] + sigma * W[t-1]
        
    return S

# Parameters
S0 = 100  # Initial stock price
sigma = 0.2  # Volatility
T = 1.0  # Total time period (e.g., 1 year)
dt = 0.01  # Time step (e.g., daily steps)

# Simulate mid-price
mid_price = simulate_mid_price(S0, sigma, T, dt)

# Plot the results
plt.plot(mid_price)
plt.title("Simulated Mid-Price of Stock")
plt.xlabel("Time Steps")
plt.ylabel("Price")
plt.show()

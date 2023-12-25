import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon
import random

# Set the mean of the exponential distribution
mean = 37
scale = 1 / mean
plt.figure(figsize = (8, 4))
plt.hist([random.expovariate(scale) for i in range(100000)], bins = 100)
plt.show()

'''''
# Calculate the scale parameter (inverse of the rate parameter)
scale = 1 / mean
scale=mean

# Generate random samples from the exponential distribution
data = np.random.exponential(scale, size=1000)

# Plot the histogram
#plt.hist(data, bins=80, density=True, alpha=0.7, color='blue', label='Histogram')

# Plot the probability density function (PDF) of the exponential distribution
x = np.linspace(0, np.max(data), 100)
pdf = expon.pdf(x, scale=scale)
plt.plot(x, pdf, 'r-', lw=2, label='Exponential PDF')

# Set labels and title
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.title(f'Exponential Distribution with Mean {mean}')

# Add legend
plt.legend()

# Show the plot
plt.show()
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import time
from data_vent import wind_data

# Collecting wind data from multiple dimensions in a dataset
bins = 100
all_ventU = []
all_ventV = []
for temps in range(10):
    for pression in range(6):
        for case_longitude in range(len(wind_data["data"][temps][pression])):
            for case_latitude in range(len(wind_data["data"][temps][pression][case_longitude])):
                all_ventU.append(wind_data["data"][temps][pression][case_longitude][case_latitude][0])
                all_ventV.append(abs(wind_data["data"][temps][pression][case_longitude][case_latitude][1]))


# Trimming data: Remove top 5% of data
lower_bound, upper_bound = np.percentile(all_ventU, [5, 95])
all_ventU_trimmed = [u for u in all_ventU if lower_bound<=u and  u <= upper_bound]

# Standardizing data: Divide by standard deviation
all_ventU_mean = np.mean(all_ventU)
std_ventU = np.std(all_ventU_trimmed)
all_ventU_standardized = (all_ventU_trimmed) / std_ventU

all_ventU_standardized = np.abs(all_ventU_standardized)

# Generating histogram data to fit distributions
y, x = np.histogram(all_ventU_standardized, bins=bins, density=True)
x = (x[1:] + x[:-1]) / 2  # Compute bin centers for better fit visualization
y = y / np.sum(y)  # Normalize the histogram

# List of distributions to try
dist_names = ['norminvgauss', 'pearson3', 'powerlaw', 'powerlognorm', 'powernorm', 'rice', 'recipinvgauss', 'semicircular', 't', 'triang', 'uniform', 'vonmises', 'vonmises_line', 'wald', 'weibull_min', 'weibull_max', 'wrapcauchy','pareto', 't', 'lognorm', 'invgamma', 'invgauss', 'loggamma', 'alpha', 'chi', 'chi2', 'expon','norm','halfnorm', 'hypsecant', 'laplace', 'levy','gengamma', 'genlogistic', 'genpareto', 'gennorm', 'halfgennorm', 'levy_l', 'logistic', 'maxwell', 'mielke', 'nakagami']

sse = np.inf  # Initialize sse very high to find the minimum
sse_thr = 0.01 # Threshold for SSE to decide on the best fit

# Fit each distribution to the data and find the best fitting distribution
for name in dist_names:
    print(f"Fitting {name} distribution")
    dist = getattr(scipy.stats, name)
    param = dist.fit(all_ventU)  # Fit distribution
    arg = param[:-2]
    loc = param[-2]
    scale = param[-1]
    pdf = dist.pdf(x, *arg, loc=loc, scale=scale)  # Probability Density Function
    model_sse = np.sum((y - pdf) ** 2)  # Sum of Squared Estimate of errors

    # Update the minimum sse and best fitting parameters if current model_sse is the new minimum
    if model_sse < sse:
        best_pdf = pdf
        sse = model_sse
        best_name = name
        best_loc = loc
        best_scale = scale
        best_arg = arg
        if sse < sse_thr:
            break
        

# Plot the data and the best fitting distribution
plt.figure(figsize=(12, 8))
plt.plot(x, y, label="Data Histogram")
plt.plot(x, best_pdf, label=f"Best Fit: {best_name}", linewidth=3)
plt.legend(loc='upper right')
plt.show()

# Output details of the best fit
print("Selected Model:", best_name)
print("Location parameter:", best_loc)
print("Scale parameter:", best_scale)
print("Other arguments:", best_arg)
print("SSE:", sse)

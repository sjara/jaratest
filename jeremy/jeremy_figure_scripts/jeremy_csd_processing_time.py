from elephant.current_source_density import estimate_csd
from neo import AnalogSignal
import quantities as pq

import numpy as np
import matplotlib.pyplot as plt
import time

elapsed_time_list = []

for parsing_variable in np.arange(5,26,5)[::-1]:
    start_time = time.time()  # Record start time
    
    # Find the mean of the uncollapsed psth
    mean_psth = psth_uncollapsed.mean(axis=0)
    # Take a subset of channels
    mean_psth = mean_psth[...,::parsing_variable]

    coords2 = [(elem,) for elem in range(mean_psth.shape[-1])]
    neo_lfp_personal2 = AnalogSignal(mean_psth*bitVolts, units="uV", sampling_rate = sampleRate*pq.Hz)
    neo_lfp_personal2.annotate(coordinates = coords2 * pq.mm)

    # Time consuming part
    csd_not_np2 = estimate_csd(neo_lfp_personal2, method="KCSD1D")

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Compute elapsed time
    elapsed_time_list.append([parsing_variable,elapsed_time])
    print(f"Parsing via every {parsing_variable}'th channel: {elapsed_time:.4f} seconds")

'''
Linear regression done by chatgpt
'''

x = np.array(elapsed_time_list[::-1]).T[0]
y = np.array(elapsed_time_list[::-1]).T[1]

# Perform linear regression in log-space
log_y = np.log(y)
coeffs = np.polyfit(x, log_y, 1)
poly_eq = np.poly1d(coeffs)

# Generate fitted y values
y_fit = np.exp(poly_eq(x))

plt.scatter(x, y, label="Data Points")
plt.plot(x, y_fit, color='red', linestyle='--', label="Linear Fit (Log-Scale)")

plt.yscale('log')

plt.xlabel("Step Index (every n steps)")
plt.ylabel("CSD estimation time (s)")
plt.title("CSD Estimation Time vs. Number of Channel Divisions")

# Show plot
plt.show()


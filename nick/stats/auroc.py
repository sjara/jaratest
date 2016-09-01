import numpy as np
import matplotlib.pyplot as plt

data = np.random.normal(1, 1, 1000)
data2 = np.random.normal(2, 1, 1000)

values1, base1 = np.histogram(data, bins=40)
values2, base2 = np.histogram(data2, bins=40)

cumulative1 = np.cumsum(values1)
cumulative2 = np.cumsum(values2)

plot(cumulative1/1000.0, cumulative2/1000.0)

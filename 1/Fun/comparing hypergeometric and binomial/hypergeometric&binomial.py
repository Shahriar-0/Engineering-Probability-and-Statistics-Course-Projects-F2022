import numpy as np
from scipy.special import comb
import matplotlib.pyplot as plt

N = 100
n = 50
M = 20
k = np.arange(0, M, 1)

fig, ax = plt.subplots(1, 2)

y = comb(M, k) * comb(N - M, n - k) / comb(N, n)
ax[0].plot(k, y)

y2 = comb(n, k) * ((M / N) ** k) * (((N - M) / N) ** (n - k))
ax[0].plot(k, y2)

n = 10
y = comb(M, k) * comb(N - M, n - k) / comb(N, n)
ax[1].plot(k, y)

y2 = comb(n, k) * ((M / N) ** k) * (((N - M) / N) ** (n - k))
ax[1].plot(k, y2)

plt.show()
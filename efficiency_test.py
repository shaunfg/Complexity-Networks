import numpy as np
import random
import matplotlib.pyplot as plt

def plot_bar(z,title = "Oslo Model"):
    heights = np.cumsum(z[::-1])[::-1] #indexing to reverse list
    plt.figure(figsize= (8,5))
    plt.bar(np.arange(1,len(z)+1,1),heights)
    plt.title(title)
    plt.ylabel("Heights")
    plt.xlabel("sites")

def Oslo(L, plot=False, p=1 / 2, N_recurrents=1000, title=None):
    """
    Parameters
    L: Number of sites 
    plot: Plots heights if true
    p: probability
    N_recurrents: Number of recurrent runs after reaching steady state
    """
    # Allows for change in probabilities
    n = int(1 / p)  # Number of thresholds, from probability
    prob = [p] * n
    z_ths = np.arange(1, n + 1, 1)  # Generates possible thresholds [1,2,...]
    #     print(z_ths)

    # Initialisation
    z = [0] * L
    z_th = [np.random.choice(z_ths, p=prob) for x in range(L)]

    # Variables for testing
    avalanches = []
    end_value = 0
    z_avg_steady = []
    steady = False  # To
    N_full_avalanche = 0  # Tracks full avalanches
    configurations = []  # Find number of unique configurations
    outflux = 0

    while end_value < N_recurrents:

        # Drive
        z[0] += 1

        abc = [x > y for x, y in zip(z, z_th)]
        # Relaxation - Checks all slopes z relaxed, before driving again
        while any(abc) == True:  # z[i] > z_th[i]:
            s = 0
            for i in range(len(z)):
                if z[i] > z_th[i]:
                    s += 1
                    if i == 0:
                        z[0] = z[0] - 2
                        z[1] = z[1] + 1

                    elif i == len(z) - 1:  # index 0,...,L-1 ; len to L
                        z[-1] = z[-1] - 1
                        z[-2] = z[-2] + 1
                        if steady == True: outflux += 1
                    else:
                        z[i] = z[i] - 2
                        z[i + 1] = z[i + 1] + 1
                        z[i - 1] = z[i - 1] + 1

                    # Only resets if topples
                    z_th[i] = random.choice(z_ths)

                # If avalance size is whole length of sites
                if s == L:
                    steady = True
                    N_full_avalanche += 1

                if steady == True:
                    end_value += 1
                    z_avg_steady.append(np.cumsum(z[::-1])[::-1][0])
                avalanches.append(s)
            abc = [x > y for x, y in zip(z, z_th)]
        configurations.append(z[:])
        # Check
        if any(x > max(z_ths) for x in z) == True:
            raise ValueError("Not all sites relaxed")

    # Obtains cumulative sum of slopes, to represent heights
    heights = np.cumsum(z[::-1])[::-1]  # indexing to reverse list

    if plot == True:
        plot_bar(z, title=title)

    #     print(outflux)
    return heights, z, np.mean(z_avg_steady), configurations


Oslo(100, p=1 / 2, plot=True, N_recurrents=10)
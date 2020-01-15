#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 21:45:26 2020

@author: ShaunGan
"""

import numpy as np
import random
import matplotlib.pyplot as plt

def plot_bar(z,title = "Oslo Model"):
    heights = np.cumsum(z[::-1])[::-1] #indexing to reverse list
#     plt.figure(figsize= (8,5))
    plt.bar(np.arange(1,len(z)+1,1),heights)
    plt.title(title)
    plt.ylabel("Heights")
    plt.xlabel("sites")
    
class Oslo:
    """
    Parameters
    L: Number of sites 
    plot: Plots heights if true
    p: probability
    N_recurrents: Number of recurrent runs after reaching steady state
    """
    
    def __init__(self,L):
        self.L = L



    def run(self, plot=False, p =[1/2,1/2], N_recurrents=10,title=None, check_slopes = False):

        z = [0] * self.L

        # Allows for change in probabilities
        n = len(p)  # Number of thresholds, from probability
        z_ths = np.arange(1, n + 1, 1)  # Generates possible thresholds [1,2,...]

        # Initialisation
        z_th = [random.choice(z_ths) for x in range(self.L)]

        # Variables for testing
        end_value = 0
        avalanches = []
        z_avg_steady = []
        steady = False  # To
        N_full_avalanche = 0  # Tracks full avalanches
        configurations = []  # Find number of unique configurations
        delta_heights = [0]

        while end_value < N_recurrents:

            # Drive
            z[0] += 1
            s= 0
            del_h = 1
            slopes_to_relax = [0]

            # Relaxation - Checks all slopes z relaxed, before driving again
            while len(slopes_to_relax) != 0:
                check_slopes = slopes_to_relax
                next_slopes = []
                for i in slopes_to_relax:
                    if z[i] > z_th[i]:
                        s += 1
                        if i == 0:
                            z[i] = z[i] - 2
                            z[i+1] = z[i+1] + 1

                            if z[i+1] == z_th[i+1] + 1:
                                next_slopes.append(i+1)

                        elif i == len(z) - 1:  # index 0,...,L-1 ; len to L
                            z[len(z) - 1] = z[len(z) - 1] - 1
                            z[len(z) - 2] = z[len(z) - 2] + 1

                            steady = True
                            del_h = 0

                            if z[len(z) - 2] == z_th[len(z) - 2] + 1:
                                next_slopes.append(len(z) - 2)

    #                         if steady == True: outflux += 1
                        else:
                            if z[i+1] == z_th[i+1] + 1:
                                next_slopes.append(i+1)

                            z[i] = z[i] - 2
                            z[i + 1] = z[i + 1] + 1
                            z[i - 1] = z[i - 1] + 1

                            if z[i+1] == z_th[i+1] + 1:
                                next_slopes.append(i+1)
                            if z[i-1] == z_th[i-1] + 1:
                                next_slopes.append(i-1)

                        z_th[i] = random.choice(z_ths)

                        if z[i] > z_th[i]:
                            next_slopes.append(i)
                    else:
                        pass

                if len(next_slopes) > 0:
                    # Finds unique next slopes.
                    slopes_to_relax = list(set(next_slopes))

                else:
                    slopes_to_relax = []

    #                 print("slopes are zero",s,L)

                # If avalance size is whole length of sites
    #             if s == L:
    # #                 print(s,z)
    #                 steady = True
    #                 N_full_avalanche += 1

                if steady == True:
                    end_value += 1
                    z_avg_steady.append(np.cumsum(z[::-1])[::-1][0])
                avalanches.append(s)
                delta_heights.append(del_h)
            configurations.append(z[:])

            # Check
            if check_slopes == True:
                if any(x > max(z_ths) for x in z) == True:
                    print(z,z_th)
                    print(check_slopes)

                    raise ValueError("Not all sites relaxed")

        # Obtains cumulative sum of slopes, to represent heights
        final_heights = np.cumsum(z[::-1])[::-1]  # indexing to reverse list

        if plot == True:
            plot_bar(z)

        return final_heights, z, np.mean(z_avg_steady), configurations,delta_heights


Oslo = Oslo(512)

Oslo.run(plot = True,N_recurrents = 10)
plt.show()
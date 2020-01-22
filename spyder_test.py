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
    
    def __init__(self,L, p =[1/2,1/2]):
        self.p = p
        self.L = L

    def run(self, plot=False, N_recurrents=None,title=None, check_slopes = False,N_runs = None):

        z = [0] * self.L

        # Allows for change in probabilities
        n = len(self.p)  # Number of thresholds, from probability
        z_ths = np.arange(1, n + 1, 1)  # Generates possible thresholds [1,2,...]

        # Initialisation
        z_th = [random.choice(z_ths) for x in range(self.L)]

        # Variables for testing
        end_value = 0
        avalanches = []
        z_avg_steady = []
        crossover = False  # To
        N_full_avalanche = 0  # Tracks full avalanches
        configurations = []  # Find number of unique configurations
        self.delta_heights = [0]
        self.cross_over_time = 0
        cross_over_time = 0

        if N_runs != None:
            N_count = N_runs
        elif N_recurrents != None:
            N_count = N_recurrents
        
        while end_value < N_count:

            # Drive
            z[0] += 1
            s = 0
            del_h = 1
            slopes_to_relax = [0]
            
            if end_value % 1000 == 0:
                print(end_value)

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
                            if crossover == False: cross_over_time += 1
                            del_h -= 1

                        elif i == len(z) - 1:  # index 0,...,L-1 ; len to L
                
                            z[len(z) - 1] = z[len(z) - 1] - 1
                            z[len(z) - 2] = z[len(z) - 2] + 1
                            crossover = True
                            if z[len(z) - 2] == z_th[len(z) - 2] + 1:
                                next_slopes.append(len(z) - 2)
#                             if steady == True: outflux += 1
                            
                            if self.cross_over_time == 0: self.cross_over_time = cross_over_time

                        else:
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
                        if crossover == False: cross_over_time += 1
                        pass

                if len(next_slopes) > 0:
                    # Finds unique next slopes.
                    slopes_to_relax = list(set(next_slopes))

                else:
                    slopes_to_relax = []

                # If avalance size is whole length of sites
    #             if s == L:
    # #                 print(s,z)
    #                 steady = True
    #                 N_full_avalanche += 1


                avalanches.append(s)
            # out of loop
            if N_runs != None:
                end_value +=1
            elif crossover == True:
                end_value += 1
                z_avg_steady.append(np.cumsum(z[::-1])[::-1][0])
#             else:
#                 raise ValueError("Not Counting!!")

                
            self.delta_heights.append(del_h)
                
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
        self.z = z

        return final_heights, z, np.mean(z_avg_steady), configurations
    
    def get_heights(self,plot = True):
#         print(len(self.z))
        heights = np.cumsum(self.delta_heights)
        time = np.arange(1,len(heights)+1,1)
        if plot == True:
            plt.xlabel("Time")
            plt.ylabel("Height")
            plt.title("Height of pile against time")
            plt.plot(time,heights,label = "L = {}".format(self.L))
        return time, heights
    
    def get_cross_over_times(self):
#         plt.axvline(self.cross_over_time)
        return self.cross_over_time

import time 

start = time.time()

check = Oslo(256)
check.run(N_runs = 1000000)
check.get_heights()
check.get_cross_over_times()

end = time.time()

print(end-start)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 21:45:26 2020

@author: ShaunGan
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd

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
        self.avalanches = []
        z_avg_steady = []
        crossover = False  # To
        N_full_avalanche = 0  # Tracks full avalanches
        self.configurations = [[0]*self.L]  # Find number of unique STABLE configurations
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
            if crossover == False: cross_over_time += 1
            # Relaxation - Checks all slopes z relaxed, before driving again
            while len(slopes_to_relax) != 0:
                check_slopes = slopes_to_relax
                next_slopes = []
                for i in slopes_to_relax:
                    if z[i] > z_th[i]:
                        s += 1
                        print(end_value,s,slopes_to_relax,z,z_th)
                        if i == 0:
                            z[i] = z[i] - 2
                            z[i+1] = z[i+1] + 1
                            if z[i+1] == z_th[i+1] + 1:
                                next_slopes.append(i+1)
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
                        pass

                if len(next_slopes) > 0:
                    # Finds unique next slopes.
                    slopes_to_relax = list(set(next_slopes))

                else:
                    slopes_to_relax = []
                    
                # out of for loop 
            self.avalanches.append(s)
            # out of while loop
            if N_runs != None:
                end_value +=1
            elif crossover == True:
                end_value += 1
                z_avg_steady.append(np.cumsum(z[::-1])[::-1][0])
#             else:
#                 raise ValueError("Not Counting!!")

                
            self.delta_heights.append(del_h)
                
            self.configurations.append(z[:].copy())
#             print(self.configurations)

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

        return final_heights, z, np.mean(z_avg_steady), self.configurations
    
    def get_heights(self,plot = True):
#         print(len(self.z))
        heights = np.cumsum(self.delta_heights)
#         print(self.delta_heights)
        time = np.arange(1,len(heights)+1,1)
        if plot == True:
            plt.xlabel("Time")
            plt.ylabel("Height")
            plt.title("Height of pile against time")
            plt.plot(time,heights,label = "L = {}".format(self.L))
        return time, heights

    def get_heights_attractor(self,plot = False):
        times, heights = self.get_heights(plot = False)
#         print(times)
#         print(self.cross_over_time)
        times_crossed = times[self.cross_over_time:]
#         print(times_crossed)
        # Shift so T starts at zero
        times_crossed -= self.cross_over_time
        heights_crossed = heights[self.cross_over_time +1:]
        
        avg_height = 1/times_crossed[-1] * sum(heights_crossed)
        avg_height_sq = 1/times_crossed[-1] * sum(heights_crossed**2)
        
        self.std_dev = np.sqrt(avg_height_sq - avg_height **2)
        
        if plot == True:
            plt.plot(times_crossed,heights_crossed)
            
        return avg_height
    
    def get_std_heights(self):
        return self.std_dev
    
    def get_cross_over_times(self):
#         plt.axvline(self.cross_over_time)
        return self.cross_over_time

    def get_probability_heights(self):
        """
        Creats a dataframe of heights, and their counts from the configurations
        
        Returns a list of normalised probabilities form height = 0
        """
        
        sums = [sum(x) for x in self.configurations]
        df = pd.DataFrame({"Configurations": self.configurations,"Heights":sums})
        count_heights =pd.DataFrame(df["Heights"].value_counts().sort_index().reset_index())
        count_heights.columns = ["height","count"]
        
        heights = count_heights["height"].to_list()
        
        counts = np.array(count_heights["count"].to_list())
        N_observed = len(df) # Number of all configurations observed
        probs = counts/N_observed
#         print(count_heights)

        return [heights,probs]

    def get_avalanche(self):
        return self.avalanches
    
check = Oslo(4)
a,b,c,configs = check.run(N_runs = 1000)
a,b = check.get_heights()
check.get_heights_attractor()
check.get_probability_heights()
check.get_avalanche()
# check.get_std_heights()
# check.get_cross_over_times()
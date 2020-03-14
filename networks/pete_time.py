import numpy as np
import random

def likesample(l, n):
    """Random numbers"""
    sample = []
    count = 0
    while count < n:
        new = random.choice(l)
        if new not in sample:
            sample.append(new)
            count +=1
    return sample

def random_walk_graph2(n, m, q):
    """Random walk graph."""
    startnodes = list(range(m))
    repeats = startnodes + []
    finaledges = []
    newnode = m
    myrand = np.random.random()
    adj = [[j for j in range(m)] for i in range(m)]
    adjremoved = [adj[i].remove(i) for i in range(m)]

    while newnode < n:
        adj.append([])
        repeats.append(newnode)
        for newedge in startnodes:
            while q > myrand:
                alladj = [item for item in adj if newedge in item]
                if alladj == []:
                    break
                myadj = random.choice(alladj)
                mynewadj = [x for x in myadj if x != newedge]
                if mynewadj == []:
                    break
                newedge = random.choice(mynewadj)
                myrand = np.random.random()
            myrand = np.random.random()
            adj[-1].append(newedge)
            adj[newedge].append(newnode)
            finaledges.append((newedge, newnode))
        startnodes = likesample(repeats, m)
        myrand = np.random.random()
        newnode += 1
    return finaledges

finaledges = random_walk_graph2(10000, 3, 0.5)
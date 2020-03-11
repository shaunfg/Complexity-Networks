import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from collections import Counter
from logbin230119 import logbin
import pandas as pd
from scipy import stats

print(pd.__version__)


def multidimensional_shifting(num_samples, sample_size, elements, probabilities):
    # replicate probabilities as many times as `num_samples`
    replicated_probabilities = np.tile(probabilities, (num_samples, 1))

    # get random shifting numbers & scale them correctly
    random_shifts = np.random.random(replicated_probabilities.shape)
    random_shifts /= random_shifts.sum(axis=1)[:, np.newaxis]

    # shift by numbers & find largest (by finding the smallest of the negative)
    shifted_probabilities = random_shifts - replicated_probabilities
    return np.argpartition(shifted_probabilities, sample_size, axis=1)[:, :sample_size]

class Barabasi_Albert():

    def __init__(self, time_limit, m, m_start=None):
        """
        time_limit: run time until this value
        m: number edges to add every time a new vertex is added
        m0: int, set up initial graph.
        """

        if m_start == None:
            m_start = m
        G0 = nx.complete_graph(m_start)  # Start with complete graph, so that unbiased

        flatten = lambda l: [item for sublist in l for item in sublist]
        self.m0 = m_start
        self.m = m
        self.G = G0
        self.preferential_list = flatten([[x] * (m_start - 1) for x in range(m_start)])
        #         print(self.preferential_list)
        self.time_limit = time_limit

        if self.m > m_start:
            raise ValueError("m value must be less than initial graph value")

    def drive_pref(self,draw = False):
        for t in range(self.time_limit):
            node = t + self.m0  # Find the node number

            connections = []
            vertices = [node]

            for i in range(self.m):
                vertex = random.choice(self.preferential_list)
                while vertex in vertices:
                    vertex = random.choice(self.preferential_list)
                vertices.append(vertex)

                link = (node, vertex)
                # Save nodes to connect on graph
                connections.append(link)

                # Add to preferential list, one by one if m > 1. add last to prevent self-loops
                self.preferential_list.extend(link)

            if draw == True:
                self.G.add_node(node)
                self.G.add_edges_from(connections)

        df = self._get_counts()
        return df

    #             print(connections)

    def drive_random(self,draw = False):
        nodes = list(self.G.nodes)

        for t in range(self.time_limit):
            node = t + self.m0  # Find the node number
            nodes.append(node)
            connections = []
            vertices = [node]

            for i in range(self.m):
                vertex = random.choice(nodes)
                # Prevents multi loops
                while vertex in vertices:
                    vertex = random.choice(nodes)
                vertices.append(vertex)

                link = (node, vertex)
                # Save nodes to connect on graph
                connections.append(link)

                # Add to preferential list, one by one if m > 1. add last to prevent self-loops
                self.preferential_list.extend(link)
            if draw == True:

                self.G.add_node(node)
                self.G.add_edges_from(connections)

        df = self._get_counts()
        return df

    def drive_walk(self, q):

        if q == 1:
            raise ValueError("q must be less than 1")

        # Create list neighbours from a complete graph
        self.neighbours = [[x for x in range(self.m0) if x != i] for i in range(self.m0)]

        # Get list of nodes
        nodes = list(self.G.nodes)

        for t in range(self.time_limit):
            node = t + self.m0  # Find the node number
            connections = []  # Empty List for to list all connections required
            self.neighbours.append([])  # Append empty list for new node
            disallowed_vertices = [node]

            nodes.append(node)

            for i in range(self.m):


                # Pick an initial vertex
                vertex = random.choice(nodes)  # Can't pick itself, as not aded to the list yet

                # Prevents node from selecting the same vertex as run before from m=0,1,...
                while vertex in disallowed_vertices:
                    vertex = random.choice(nodes)

                    # Continue walking with a probability of q
                while q > random.uniform(0, 1):

                    #                     print("Node = ",node,"Vertex = ",vertex,self.neighbours[vertex],"disallowed",disallowed_vertices)

                    # Choose a neighbour of the target vertex.
                    vertex = random.choice(self.neighbours[vertex])

                    # Prevents self loops
                    while vertex in disallowed_vertices:
                        vertex = random.choice(self.neighbours[vertex])
                disallowed_vertices.append(vertex)

                #                 print("Node = ",node,"Vertex = ",vertex,self.neighbours[vertex],"disallowed",disallowed_vertices)

                # Save vertices connected to, used to prevent multi links

                # Create tuple to connect nodes
                link = (node, vertex)

                # Save neighbours, in an adjacency list.
                self.neighbours[node].append(vertex)
                self.neighbours[vertex].append(node)

                # Save nodes to connect on graph
                connections.append(link)

            self.G.add_node(node)
            self.G.add_edges_from(connections)

        df = self._get_counts()
        return df

    def get_degrees(self):
        return np.array(self.preferential_list)

    def _get_counts(self):
        counts = dict(Counter(self.preferential_list))

        df = pd.DataFrame(counts.items(), columns=['Node', 'Degrees'])
        df = df.set_index('Node')
        return df

    def draw(self):
        nx.draw(self.G, with_labels=True, font_weight='bold')


if __name__ == "__main__":
    repeats = 10
    m_starting = 5
    m_add = 5
    times = [1, 10, 100, 1000, 10000, 100000]

    degrees_all = []
    k_maxes_random = []
    for i in range(len(times)):
        print("Calulating time t = ", times[i])
        degrees_total = []
        k_maxes_random.append([])
        for N in range(repeats):
            print("--Repeat ", N)
            Ba_1 = Barabasi_Albert(time_limit=times[i], m=m_add, m_start=m_starting)
            df = Ba_1.drive_random()
            degrees_total.extend(df.Degrees.values)
            k_maxes_random[i].append(max(df.Degrees.values))
        x, y = logbin(degrees_total, scale=1.2)
        plt.title("Degree Distribution, (m = {}, m0 = {})".format(m_add, m_starting))
        plt.xlabel("Number of Degrees (k)")
        plt.ylabel("Probability of degree $p(k)$")
        plt.loglog(x, y, label="t = {}".format(times[i]))
        degrees_all.append(degrees_total)
    plt.legend()

    #     fit_log(x,y,label = r"$p_{\infty}(k)\propto k^{-3}$")
    #     expected_values = fit_master_EQ(m=2,k=x)
    #     plt.legend()
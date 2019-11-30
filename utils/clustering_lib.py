import numpy as np
import pandas as pd
import math


def distance(v1, v2):
    d = 0
    
    for i in range(len(v1)):
        d += (v1[i]-v2[i])**2
    
    return math.sqrt(d)


class Kmeans:

    def __init__(self, k, n_features):
        self.C = np.zeros((k, n_features))
        self.K = k
        self.n = n_features
        self.Cluster = {i+1:[] for i in range(k)}


    def random_centers(self, data):
        
        for f in range(self.n):
            self.C[:,f] = np.random.uniform(data[:,f].min(), data[:,f].max(), size=(self.K,))


    def closest_center(self, vector):
        distances = np.zeros(self.K)
        center = 1
        
        for k in range(self.K):
            distances[k] = distance(self.C[k], vector)

            if k > 0 and distances[k] < distances[k-1]:
                center = k+1

        return center


    def clustering(self, data):

        for i in range(len(data)):
            c = self.closest_center(data[i])
            self.Cluster[c].append(data[i])
            

    def update_centers(self):

        for k in range(self.K):
            midpoint = np.mean(self.Cluster[k+1], axis=0)
            
            if len(self.Cluster[k+1]) != 0:
                self.C[k] = midpoint
            else:
                continue
            
        self.Cluster = {i+1:[] for i in range(self.K)}
            
            
    def cost_function(self):
        cost = 0
        
        for k in range(self.K):
            for point in self.Cluster[k+1]:
                cost += distance(point, self.C[k])**2
                
        return cost
       

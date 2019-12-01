import numpy as np
import pandas as pd
import math


# this function calculates the distance between two vectors
def distance(v1, v2):
    d = 0
    
    for i in range(len(v1)):
        d += (v1[i]-v2[i])**2
    
    return math.sqrt(d)



class Kmeans:
    
    # once a Kmeans object is created with "k" clusters, an array of zeros is defined
    # in which we will store the coordinates of the centroids and an empty list in which 
    # we will insert the points belonging to each of the "k" clusters
    def __init__(self, k, n_features):
        self.C = np.zeros((k, n_features))
        self.K = k
        self.n = n_features
        self.Cluster = {i+1:[] for i in range(k)}


    # to initialize centroids randomly, as explained in main.ipynb
    def random_centers(self, data):
        
        for f in range(self.n):
            self.C[:,f] = np.random.uniform(data[:,f].min(), data[:,f].max(), size=(self.K,))


    # given a point (or vector) it returns the nearest centroid, or the cluster to which such point belongs
    def closest_center(self, vector):
        distances = np.zeros(self.K)
        center = 1
        
        # evaluate the distance from each centroid
        for k in range(self.K):
            distances[k] = distance(self.C[k], vector)

            if k > 0 and distances[k] < distances[k-1]:
                # when the evaluated distance becomes the shortest, instead the center is "k+1" 
                # because the clusters names start from 1 instead of 0 as the index "k"
                center = k+1

        return center


    # it scrolls all the data and adds each of them to a cluster in the dictionary created initially
    def clustering(self, data):

        for i in range(len(data)):
            c = self.closest_center(data[i])
            self.Cluster[c].append(data[i])
            

    # updates the coordinates of the centroids with the amidpoint of the data belonging 
    # to the cluster defined by that centroid
    def update_centers(self):

        for k in range(self.K):
            midpoint = np.mean(self.Cluster[k+1], axis=0)
            
            # if a cluster has no element, its centroid is not updated because this gives 
            # problem in the main code
            if len(self.Cluster[k+1]) != 0:
                self.C[k] = midpoint
            else:
                continue
        
        # it is necessary to empty the dictionary to fill it with new clusters
        self.Cluster = {i+1:[] for i in range(self.K)}
            
    
    # this function evaluates the cost function of k-means algo
    def cost_function(self):
        cost = 0
        
        for k in range(self.K):
            for point in self.Cluster[k+1]:
                cost += distance(point, self.C[k])**2
                
        return cost
       

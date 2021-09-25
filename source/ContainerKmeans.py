"""
Code for running kmeans clustering to solve an instance of CSP.

Stony Brook University, NY, February 2016
"""

from Cluster import Cluster
from clustering_algorithms import hierarchical_clustering, kmeans_clustering, closestCorner
from clustering_matplotlib import plot_clusters
import time

__author__ = 'CalebAndrade'

#******************************************************************************
# Code to load data tables
#******************************************************************************

def readFile(filename):
    """ Read data file """
    
    data = []
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            row = line.split(',')
            data.append([row[0], float(row[1]), float(row[2]), int(row[3]), float(row[4])])
    
    print "\nLoaded", len(data), "data points"
    return data

#******************************************************************************
# Load data, compute a CSP Kmeans solution and visualize results
#******************************************************************************

def main():
    args = parse_args()
    
    data = readFile(args.infile1)
    k = int(args.infile2)
    m = int(args.infile3)
    
    # build an initial cluster list, each point as a single cluster
    singletons = [Cluster(set([x[0]]), x[1], x[2], x[3], (x[1], x[2])) for x in data ]
     
    # compute clusters
    tic = time.clock()
    cluster_list = kmeans_clustering(singletons, k, m)	
    toc = time.clock()
    print "Displaying", len(cluster_list), "k-means clusters"
    print "Iterations", m

    # compute minimal dominant point with l1-norm for each cluster
    corners = [cluster.corner() for cluster in cluster_list]
    
    # reassign points to closest corner
    cluster_reassign = closestCorner(singletons, corners)[0]

    # draw clusters
    plot_clusters(data, cluster_list, fs = 10, weights_on = False) 
    plot_clusters(data, cluster_reassign, fs = 10, weights_on = False) 

    # compare costs
    lower_bound = sum([x[3]*(x[1] + x[2]) for x in data])
    cost1 = sum([cluster.cost() for cluster in cluster_list])
    cost2 = sum([cluster.cost() for cluster in cluster_reassign])
    print "Total cost CSP kmeans        ", cost1
    print "Total cost reassigned points ", cost2
    print "Total cost lower_bound       ", lower_bound
    print "Appx ratio to lower_bound    ", cost2 / lower_bound
    print "Running time                 ", toc - tic


def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('infile1', help ='data table file')
        parser.add_argument('infile2', help ='number of clusters')
        parser.add_argument('infile3', help ='number of iterations')
        return parser.parse_args()


if __name__ == '__main__':
    main()
    
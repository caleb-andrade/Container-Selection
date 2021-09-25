"""
Naive brute force implementation to solve CSP.

Stony Brook University, NY, February 2016
"""

from ContainerPTAS import readFile, plot2D, potentialContainer
from clustering_matplotlib import plot_clusters
from clustering_algorithms import closestCorner
from itertools import combinations
from Cluster import Cluster
import time

__author__ = 'CalebAndrade'

#******************************************************************************
# Main method
#******************************************************************************        

def main():
    args = parse_args()
    
    data = readFile(args.infile1)
    k = int(args.infile2)
    
    print "Displaying", k, "optimal clusters"

    # build an initial cluster list, each point as a single cluster
    singletons = [Cluster(set([x[0]]), x[1], x[2], x[3], (x[1], x[2])) for x in data ]
       
    # Build set of potential container points (PCP)
    potential_container = potentialContainer(data)
    print "Number of potential container points", len(potential_container)
    
    # Brute force...
    tic = time.clock()
    best = (float('inf'), [])
    i = 0
    for corners in combinations(potential_container, k):
        i += 1
        cluster_list, count = closestCorner(singletons, corners)
        if count == len(singletons):
            cost = sum([cluster.cost() for cluster in cluster_list])
            if cost < best[0]:
                best = cost, cluster_list
    toc = time.clock()

    print "Total combinations", i
    print "Best cost", best[0]
    print "Running time", toc - tic
    plot_clusters(data, best[1], fs = 4, weights_on = False)
   
        
def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('infile1', help ='data table file')
        parser.add_argument('infile2', help ='number of clusters')
        return parser.parse_args()

if __name__ == '__main__':
    main()
    
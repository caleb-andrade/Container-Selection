# Kmeans Clustering approach to the Container Selection Problem (CSP)
Stony Brook University, NY, February 2016.


This is a Kmeans Clustering approach to solve the continuous version of the
Container Selection Problem (CSP) in two dimensions.

## Motivation

Nagarajan, Schieber et al have proposed a PTAS to solve CSP that involve possible
practical drawbacks, in terms of running time, for reasonable data sizes and
precision. Therefore, a scalable and faster approach is needed to manage medium
and larga datasets, at the cost ,perhaps, of an approximation guarantee.

A Kmeans clustering approach is a natural choice given its ease of implementation
and fast running time. Certain insights about the similarities between CSP and
Kmeans have led to this approach.

## Using/Browsing the Code

The source/ directory contains all the needed code and some sample datasets.

### Container Selection Problem PTAS

	ContainerPTAS.py

Example of running PTAS running time estimate:

	./ContainerPTAS.py data_111.csv 5 on

This runs PTAS pre-processing on a dataset of 111 points, with 5 rays and plotting 
'on', returning a rough estimate of running times and also explanatory plots.

### Container Selection Problem Kmeans

	Cluster.py
	clustering_algorithms.py
	clustering_matplotlib.py
	ContainerKmeans.py

Example of running Kmeans for CSP:

	./ContainerKmeans.py data_3108.csv 10 5

This runs Kmeans on a dataset of 3108 points, for k = 10 and 5 iterations, returning
the respective plots with the associated total costs of the objective function.

--
Caleb Andrade. 
Stony Brook University, NY.
February 2016.
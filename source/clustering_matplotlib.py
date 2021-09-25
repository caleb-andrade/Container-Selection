"""
Code for plotting 2D point clusters using matplotlib.
Principles of Computing Specialization by Rice University & Coursera, 2015.
Modified by Caleb Andrade.

Stony Brook University, NY, February 2016.
"""

import math
import matplotlib.pyplot as plt

__author__ = 'Luay Nakhleh, Scott Rixner, Joe Warren'

# Define colors for clusters.
COLORS = ['Red', 'Blue', 'Aqua', 'Yellow', 'Fuchsia', 'Green', 'Lime', 'Maroon',
		  'Navy', 'Olive', 'Orange', 'Purple', 'Brown', 'Teal', 'Magenta']

#******************************************************************************
# Helper functions
#******************************************************************************

def circle_area(pop):
	"""
	Compute area of data point's circle proportional to weight
	"""
	return math.pi * pop / (200.0 ** 2)


def plot_clusters(data_table, cluster_list, fs = 10, weights_on = True):
	"""
	Create a plot of clusters of data points
	"""

	fips_to_line = {}
	for line_idx in range(len(data_table)):
		fips_to_line[data_table[line_idx][0]] = line_idx
	 
	# Scale plot 
	x_range = max([cluster._corner[0] for cluster in cluster_list])
	y_range = max([cluster._corner[1] for cluster in cluster_list])
	plt.figure(figsize=(fs, int(fs*float(y_range) / x_range))) # adjust image size
	axes = plt.gca() # set plot's x and y ranges
	axes.set_xlim([0,1 + int(1.05*x_range)])
	axes.set_ylim([0,1 + int(1.05*y_range)])
   
	# plotting visualization lines
	for cluster_idx in range(len(cluster_list)):
		cluster = cluster_list[cluster_idx]
		cluster_color = COLORS[cluster_idx % len(COLORS)]
		cluster_center = (cluster.horiz_center(), cluster.vert_center())
		for fips_code in cluster.fips_codes():
			line = data_table[fips_to_line[fips_code]]
			plt.plot( [cluster_center[0], line[1]],[cluster_center[1], line[2]], cluster_color, lw=1, zorder = 2)

	# plotting data points
	for cluster_idx in range(len(cluster_list)):
		cluster = cluster_list[cluster_idx]
		cluster_color = COLORS[cluster_idx % len(COLORS)]
		for fips_code in cluster.fips_codes():
			line = data_table[fips_to_line[fips_code]]
			size = 5
			if weights_on: # if dots are to be drawn according to their weight
				size = circle_area(line[3])
			plt.scatter(x = [line[1]], y = [line[2]], s = size, lw = 1,
						facecolors = cluster_color, edgecolors = cluster_color, zorder = 1)
		
	# plotting cluster centroids
	for cluster_idx in range(len(cluster_list)):
		cluster = cluster_list[cluster_idx]
		cluster_color = COLORS[cluster_idx % len(COLORS)]
		cluster_center = (cluster.horiz_center(), cluster.vert_center())
		
		plt.scatter(x = [cluster_center[0]], y = [cluster_center[1]], s =  10, lw = 1,
					facecolors = "black", edgecolors = "black", zorder = 4)

	# plotting bounding boxes 
	for cluster_idx in range(len(cluster_list)):
		cluster_color = COLORS[cluster_idx % len(COLORS)] 
		c = cluster_list[cluster_idx]
		plt.plot( [c._corner[0], c._corner[0]], [0, c._corner[1]], cluster_color, lw=1, zorder = 3)
		plt.plot( [0, c._corner[0]], [c._corner[1], c._corner[1]], cluster_color, lw=1, zorder = 3)
  
	plt.show()

"""
This code pre-processes a dataset of n points, following the ideas of
Schieber et al in the Container Selection Problem PTAS for 2D.
The purpose is to give a rough estimate of the running time, for a given
precision (number of rays)

Stony Brook University, NY, February 2016
"""

import math
from matplotlib import pyplot as plt
from ContainerKmeans import readFile

__author__ = 'CalebAndrade'

#******************************************************************************
# Code to make a simple data point plot
#******************************************************************************

def plot2D(points, color_value, size, fs):
    """ Plots a set of 2D points """
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    x_range = max(x)
    y_range = max(y)
    # adjust image size
    plt.figure(figsize=(fs, 1 + int(fs*float(y_range) / x_range))) 
    axes = plt.gca() # set plot's x and y ranges
    axes.set_xlim([0,1 + int(1.05*x_range)])
    axes.set_ylim([0,1 + int(1.05*y_range)])
    plt.scatter(x, y, s = size, lw = 0, color = color_value)
    plt.show()

                
#******************************************************************************
# Code to pre-process data points
#******************************************************************************

def potentialContainer(data):
    """ Build set of potential container points """
    
    x_set = [point[1] for point in data] # y coordinates of points
    y_set = [point[2] for point in data] # x coordinates of points
        
    # build all possible potential container points, without repeats
    potential_container = set([]) 
    for x in x_set:
        for y in y_set:
            potential_container.add((x, y))
            
    return list(potential_container)
  

def findSection(points, slopes):
    """ Build hash of the sections to which points belong """
    
    sections = {slope:[] for slope in slopes} # initialize hash
    # compare point's slope with slopes
    for point in points:
        for slope in slopes:
            if slope <= point[1] / point[0]: 
                sections[slope].append(point)
                break
    
    return sections


def transPoint(point, slope1, slope2):
    """ Single container point transformation """
    
    # compute deltas
    delta_v = point[0]*slope2 - point[1]
    if slope1 == 0:
        delta_u = float('inf')
    else:
        delta_u = point[1]/slope1 - point[0]
    
    # decide what transformation to apply
    if delta_u < delta_v:
        return (point[0] + delta_u, point[1]), slope1
    else:
        return (point[0], point[1] + delta_v), slope2  
        

def profileRT(transformed):
    """ A rough estimate of running time in years to compute profiles """
    
    profiles = 1 
    for line in transformed.values():
        if len(line) > 0:
            profiles *= len(line)
    print "Total profiles: ", profiles
    avg_ray = sum([len(line) for line in transformed.values()])/len(transformed)
    speed = 60*60*24*365*(10**9) # considering 1x10^9 ops/sec
    profile_runtime = float(profiles)/speed
    print "Profile construction running time (years): ", profile_runtime
    print "Rough estimate total running time (years): ", avg_ray*profile_runtime/2
    

def transPC(potential_container, num_slices):
    """ Transform potential container points """
    
    theta = math.pi / (2*num_slices)
    epsilon = 2*theta
    print "\nEpsilon: ", epsilon
    
    # sort slopes decreasingly
    slopes = sorted([math.tan(i*theta) for i in range(num_slices)], reverse = True)
    sections = findSection(potential_container, slopes)
    
    transformed = {slope:[] for slope in slopes}
    for slope1 in sections.keys():
        for point in sections[slope1]:
            idx = slopes.index(slope1)
            if idx == 0:
                slope2 = float('inf')
            else:
                slope2 = slopes[idx - 1]
            
            t_point, slope = transPoint(point, slope1, slope2)
            transformed[slope].append(t_point)

    profileRT(transformed)    
    
    return transformed   

#******************************************************************************
# Main method
#******************************************************************************        

def main():
    args = parse_args()
    
    data = readFile(args.infile1)
    etha = int(args.infile2)
    plotting = str(args.infile3)
    
    # Build set of potential container points (PCP)
    potential_container = potentialContainer(data)
    
    # Build set of transformed potential container points (TPCP)
    transformed = transPC(potential_container, etha)
    trans_points = []
    for value in transformed.values():
        trans_points += value
        
    # plotting
    if plotting == 'on':
        plot2D([(point[1], point[2]) for point in data], 'red', 5, 10) # input 
        plot2D(potential_container, 'blue', 5, 10) # potential container points
        plot2D(trans_points, 'green', 5, 10) # transformed container points

        
def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('infile1', help ='data table file')
        parser.add_argument('infile2', help ='number of rays')
        parser.add_argument('infile3', help ='plotting (on/off)')
        return parser.parse_args()

if __name__ == '__main__':
    main()
    
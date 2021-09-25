# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 10:10:19 2016

@author: Caleb Andrade
"""

import random

def randomPoints(value_range, n):
    """ generates a list of random points in the plane """
    
    data_file = open("random_points.csv", "w")
    for i in range(1, n + 1):
        w = 1 # weight of point
        x = value_range*random.random() #random.randint(1, value_range)
        y = value_range*random.random() #random.randint(1, value_range)
        # data point (ID, x, y, weight, error)
        data_file.write(str(i)+', '+str(x)+', '+str(y)+', '+str(w)+', 0\n')
        
    data_file.close()
    
def counterExample(n):
    """ generates a counter example """
    
    data_file = open("counter_example.csv", "w")
    for i in range(n-1):
        w = 1 # weight of point
        # data point (ID, x, y, weight, error)
        data_file.write(str(4*i+1)+', '+str(i+1)+', '+str(n)+', '+str(w)+', 0\n')
        data_file.write(str(4*i+2)+', '+str(i+1)+', '+str(n-1)+', '+str(w)+', 0\n')
        data_file.write(str(4*i+3)+', '+str(n)+', '+str(i+1)+', '+str(w)+', 0\n')
        data_file.write(str(4*i+4)+', '+str(n-1)+', '+str(i+1)+', '+str(w)+', 0\n')
        
    data_file.close()

    def main():
        """
        Generates n random points uniformly distributed in 
        value_range x value_range
        """
        n = 50
        value_range = 100

        randomPoints(value_range, 50)

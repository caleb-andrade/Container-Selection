"""
Cluster class 
Principles of Computing Specialization by Rice University & Coursera, 2015.
Modifications: averaged_risk was eliminated; corner was added to the class;
cost was added to the class. By Caleb Andrade.
"""

import math

__author__ = 'Luay Nakhleh, Scott Rixner, Joe Warren'


class Cluster:
    """
    Class for creating and merging clusters
    """
    
    def __init__(self, fips_codes, horiz_pos, vert_pos, population, corner):
        """
        Create a cluster
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._corner = corner
        
        
    def __repr__(self):
        """
        String representation
        """
        rep = "Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._corner) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of ID'S
        """
        return self._fips_codes
    
    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center
    
    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center
    
    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population
    
    def corner(self):
        """
        Get the upper right _corner of cluster's bounding box
        """
        return self._corner
        
    def cost(self):
        """
        Compute the cost as || corner ||*total_population.
        """
        return self._total_population*(self._corner[0] + self._corner[1])   
        
    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center, self._vert_center,
                               self._total_population, self._corner)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
#        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2) # euclidean
        return abs(vert_dist) + abs(horiz_dist) # manhattan
        
    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relatively populations of each
        cluster in computing a new center
        
        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))
 
            # compute weights for averaging
            self_weight = float(self._total_population)                        
            other_weight = float(other_cluster.total_population())
            self._total_population = self._total_population + other_cluster.total_population()
            self_weight /= self._total_population
            other_weight /= self._total_population
                    
            # update center using weights.
            self._vert_center = self_weight * self._vert_center + other_weight * other_cluster.vert_center()
            self._horiz_center = self_weight * self._horiz_center + other_weight * other_cluster.horiz_center()

            # update corner by selecting corner's coordinates from each cluster
            self._corner = (max(self._corner[0], other_cluster._corner[0]),
                            max(self._corner[1], other_cluster._corner[1]))

            return self

    def cluster_error(self, data_table):
        """
        Input: data_table
        
        Output: The error as the sum of the square of the distance from each point
        in the cluster to the cluster center (weighted by its population)
        """
        # Build hash table to accelerate error computation
        fips_to_line = {}
        for line_idx in range(len(data_table)):
            line = data_table[line_idx]
            fips_to_line[line[0]] = line_idx
        
        # compute error as weighted squared distance from counties to cluster center
        total_error = 0
        counties = self.fips_codes()
        for county in counties:
            line = data_table[fips_to_line[county]]
            singleton_cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
            singleton_distance = self.distance(singleton_cluster)
            total_error += (singleton_distance ** 2) * singleton_cluster.total_population()
        return total_error
            
        
            

        
    
    
            
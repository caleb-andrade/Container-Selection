"""
Clustering algorithms implementation: kmeans and hierarchical clustering.
This code was written as part of a project from Principles of Computing 
Specialization by Rice University & Coursera, 2015.
"""

from Cluster import Cluster

__author__ = 'CalebAndrade'

#******************************************************************************
# Code for closest pairs of clusters
#******************************************************************************

def pair_distance(cluster_list, idx1, idx2):
    """ Compute distance between two clusters in a list """
    
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """ Compute distance between closest pair of clusters, brute force """

    answer = (float('inf'), -1, -1)
    for idx1 in range(len(cluster_list)):
        for idx2 in range(idx1 + 1, len(cluster_list)):
            temp = pair_distance(cluster_list, idx1, idx2)
            if temp[0] < answer[0]:
                answer = temp
    
    return answer


def fast_closest_pair(cluster_list):
    """
    Compute distance between closest pair of clusters, divide and conquer 
    
    Input: cluster_list is list of clusters SORTED such that horizontal 
    positions of their centers are in ascending order
    """
    
    size = len(cluster_list)
    if size < 4:
        return slow_closest_pair(cluster_list)
    half = size / 2
    lcl = [] # left cluster list
    rcl = [] # right cluster list
    for idx in range(half):
        lcl.append(cluster_list[idx])
    for idx in range(half, size):
        rcl.append(cluster_list[idx])
    left_ans = fast_closest_pair(lcl)
    right_ans = fast_closest_pair(rcl)
    if left_ans[0] < right_ans[0]:
        temp_ans = left_ans
    else:
        temp_ans = (right_ans[0], right_ans[1] + half, right_ans[2] + half)
    mid = 0.5*(cluster_list[half - 1].horiz_center() + cluster_list[half].horiz_center())
    cps_ans = closest_pair_strip(cluster_list, mid, temp_ans[0])
    
    if cps_ans[0] < temp_ans[0]:
        return cps_ans
    else:
        return temp_ans


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e, the maximum horizontal
    distance that a cluster can lie from the center line)
    """
    
    temp_list = []
    for idx in range(len(cluster_list)):
        if abs(cluster_list[idx].horiz_center() - horiz_center) <= half_width:
            temp_list.append([cluster_list[idx], idx])
    temp_list.sort(key = lambda item: item[0].vert_center()) # sort by vert_center
    size = len(temp_list)
    ans = (float('inf'), -1, -1)
    for idx1 in range(size - 1):
        temp_ans = (float('inf'), -1, -1)
        for idx2 in range(idx1 + 1, min(idx1 + 4, size)):
            temp = temp_list[idx1][0].distance(temp_list[idx2][0])
            if temp < temp_ans[0]:
                temp_ans = (temp, idx1, idx2)
        if temp_ans[0] < ans[0]:
            ans = temp_ans
    if len(temp_list) > 0:
        ind = [temp_list[ans[1]][1], temp_list[ans[2]][1]]
    else:
        return (float('inf'), -1, -1)
    
    return (ans[0], min(ind), max(ind))            
        
#******************************************************************************
# Code for hierarchical clustering
#******************************************************************************


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    """
    
    # sort by horiz_center
    cluster_list.sort(key = lambda cluster: cluster.horiz_center()) 
    while len(cluster_list) > num_clusters:
        temp = fast_closest_pair(cluster_list)
        clust2 = cluster_list.pop(temp[2])
        clust1 = cluster_list.pop(temp[1])
        clust1.merge_clusters(clust2)
        binary_insert(cluster_list, clust1)
    
    return cluster_list
        

def binary_insert(cluster_list, cluster):
    """ 
    Inserts cluster in cluster_list according to its horiz_center 
    """
    
    top = len(cluster_list)
    low = 0
    if cluster.horiz_center() < cluster_list[0].horiz_center():
        cluster_list.insert(0, cluster)
        return       
    while top != low + 1:
        mid = (low + top) /2
        if cluster.horiz_center() < cluster_list[mid].horiz_center():
            top = mid
        else:
            low = mid            
    cluster_list.insert(top, cluster)
        

#******************************************************************************
# Code for k-means clustering
#******************************************************************************

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: cluster_list does not mutate
    """

    ans = [] # this list to store clusters with highest weight (sorted)
    cen = [] # this list to store the initial centers as tuples
    temp = list(cluster_list)
    temp.sort(key = lambda cluster: cluster.total_population())
    temp.reverse()
    for idx in range(num_clusters):
        ans.append(temp[idx].copy())
        cen.append((ans[idx].horiz_center(), ans[idx].vert_center()))
   
    for dummy_i in range(num_iterations):
        clusters = [Cluster(set([]), cen[idx][0], cen[idx][1], 0, (0, 0)) for idx in range(num_clusters)]
        for num in range(len(cluster_list)):
            best = (float('inf'), -1)
            for idx in range(num_clusters):
                temp = cluster_list[num].distance(ans[idx])
                if temp < best[0]:
                    best = (temp, idx)
            clusters[best[1]].merge_clusters(cluster_list[num])
        for idx in range(num_clusters):
            ans[idx] = clusters[idx].copy()
            cen[idx] = (clusters[idx].horiz_center(), clusters[idx].vert_center())
    
    return ans


def closestCorner(singletons, corners):
    """ Cluster points with respect to closest dominant corner """

    # initialize new clusters
    clusters = [Cluster(set([]), 0, 0, 0, (0, 0)) for corner in corners] 
     
    count = 0   
    for point in singletons:
        best = (float('inf'), (0, 0))
        for corner in corners:
            # measure distance from point to corner
            dist = abs(corner[0]-point.horiz_center()) + abs(corner[1]-point.vert_center())
            # verify that corner dominates point
            if point.horiz_center()<= corner[0] and point.vert_center() <= corner[1]:
                if dist < best[0]:
                    best = (dist, corner)

        if best[1] != (0, 0): # feasibility sanity check
            count += 1 # keep track of how many points were clustered
            idx = corners.index(best[1])
            clusters[idx].merge_clusters(point)

    return clusters, count 
    
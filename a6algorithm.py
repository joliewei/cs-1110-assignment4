"""
Primary algorithm for k-Means clustering

This file contains the Algorithm class for performing k-means clustering.  While it is
the last part of the assignment, it is the heart of the clustering algorithm.  You
need this class to view the complete visualizer.

Jolie Wei jw2493 and Jacob Yetter jay53
04/16/19
"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6checks
import a6dataset
import a6cluster


class Algorithm(object):
    """
    A class to manage and run the k-means algorithm.

    INSTANCE ATTRIBUTES:
        _dataset [Dataset]: the dataset which this is a clustering of
        _clusters [list of Cluster]: the clusters in this clustering (not empty)
    """


    # Part A
    def __init__(self, dset, k, seeds=None):
        """
        Initializes the algorithm for the dataset ds, using k clusters.

        If the optional argument seeds is supplied, it will be a list of indices into the
        dataset that specifies which points should be the initial cluster centroids.
        Otherwise, the clusters are initialized by randomly selecting k different points
        from the database to be the cluster centroids.

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter k: the number of clusters
        Precondition: k is an int, 0 < k <= dset.getSize()

        Paramter seeds: the initial cluster indices (OPTIONAL)
        Precondition seeds is None, or a list of k valid indices into dset.
        """
        assert a6checks.is_dset(dset)
        assert type(k)==int and 0<k<= dset.getSize()
        assert seeds==None or a6checks.is_seed_list(seeds,k,dset.getSize())

        self._dataset=dset
        self._clusters=[]

        if seeds==None:
            indices=random.sample(range(dset.getSize()),k)
            for x in indices:
                cluster = a6cluster.Cluster(dset, dset.getPoint(x))
                self._clusters.append(cluster)
        else:
            for i in seeds:
                cluster = a6cluster.Cluster(dset, dset.getPoint(i))
                self._clusters.append(cluster)


    def getClusters(self):
        """
        Returns the list of clusters in this object.

        This method returns the attribute _clusters directly.  Any changes made to this
        list will modify the set of clusters.
        """

        return self._clusters


    # Part B
    def _nearest(self, point):
        """
        Returns the cluster nearest to point

        This method uses the distance method of each Cluster to compute the distance
        between point and the cluster centroid. It returns the Cluster that is closest.

        Ties are broken in favor of clusters occurring earlier self._clusters.

        Parameter point: The point to compare.
        Precondition: point is a list of numbers (int or float), with the same dimension
        as the dataset.
        """
        assert a6checks.is_point(point)
        assert len(point)==self._dataset.getDimension()


        list_distances=[]
        for i in self._clusters:
            centroid_distance=i.distance(point)

            list_distances.append(centroid_distance)

        smallest_distance=min(list_distances)
        cluster=list_distances.index(smallest_distance)
        return self._clusters[cluster]


    def _partition(self):
        """
        Repartitions the dataset so each point is in exactly one Cluster.
        """
        for c in self._clusters:
            c.clear()

        points_in_dataset=self._dataset.getContents()

        for p in range(len(points_in_dataset)):

            cluster=self._nearest(self._dataset.getPoint(p))

            cluster.addIndex(p)


    # Part C
    def _update(self):
        """
        Returns True if all centroids are unchanged after an update; False otherwise.

        This method first updates the centroids of all clusters'.  When it is done, it
        checks whether any of them have changed. It then returns the appropriate value.
        """
        list_centroids=[]
        for cluster in self._clusters:
            centroid=cluster.update()
            list_centroids.append(centroid)

        for bool in list_centroids:
            if bool==False:
                return False
        return True


    def step(self):
        """
        Returns True if the algorithm converges after one step; False otherwise.

        This method performs one cycle of the k-means algorithm. It then checks if
        the algorithm has converged and returns the appropriate value.
        """
        self._partition()
        if self._update()==True:
            return True
        else:
            return False


    # Part D
    def run(self, maxstep):
        """
        Continues clustering until either it converges or maxstep steps (which ever comes first).

        Parameter maxstep: an int >= 0.
        """
        # Call step repeatedly, up to maxstep times, until the algorithm
        # converges. Stop after maxstep iterations even if the algorithm has not
        # converged.
        # You do not need a while loop for this.  Just write a for-loop, and exit
        # the for-loop (with a return) if you finish early.

        for times in range(maxstep):
            new_cluster=self.step()
            if new_cluster==True:
                return None


    def findTotalError(self):
        """
        Returns: a float representing the sum of the errors of all the centroids.

        For example, if we have two centroids and they have errors of 2.0 and 3.0 respectively,
        then the total error would be 5.0 and we would return 5.0.

        Hint: the method and findError() would be helpful in the function.
        """
        all_clusters=0
        for centroid in self._clusters:
            num = centroid.findError()
            all_clusters += num
        return all_clusters

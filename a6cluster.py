"""
Cluster class for k-Means clustering

This file contains the class cluster, which is the second part of the assignment.  With
this class done, the visualization can display the centroid of a single cluster.

Jolie Wei jw2493 and Jacob Yetter jay53
04/16/19
"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6checks
import a6dataset


class Cluster(object):
    """
    A class representing a cluster, a subset of the points in a dataset.

    A cluster is represented as a list of integers that give the indices in the dataset
    of the points contained in the cluster.  For instance, a cluster consisting of the
    points with indices 0, 4, and 5 in the dataset's data array would be represented by
    the index list [0,4,5].

    A cluster instance also contains a centroid that is used as part of the k-means
    algorithm.  This centroid is an n-D point (where n is the dimension of the dataset),
    represented as a list of n numbers, not as an index into the dataset. (This is because
    the centroid is generally not a point in the dataset, but rather is usually in between
    the data points.)

    INSTANCE ATTRIBUTES:
        _dataset [Dataset]: the dataset this cluster is a subset of
        _indices [list of int]: the indices of this cluster's points in the dataset
        _centroid [list of numbers]: the centroid of this cluster
        _name [str]: an optional label for the centroid. Can be the empty string
    EXTRA INVARIANTS:
        len(_centroid) == _dataset.getDimension()
        0 <= _indices[i] < _dataset.getSize(), for all 0 <= i < len(_indices)
    """


    # Part A
    def __init__(self, dset, centroid,name=""):
        """
        Initializes a new empty cluster whose centroid is a copy of <centroid>

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter centroid: the cluster centroid
        Precondition: centroid is a list of dset.getDimension() numbers

        Parameter name: the name of the cluster centroid
        Precondition: a string, possibly empty
        """
        assert a6checks.is_dset, "dset is not an instance of Dataset"
        assert type(centroid)==list
        assert len(centroid)==dset.getDimension()
        assert a6checks.is_name, "name is not a string"

        self._dataset=dset
        copy_centroid=[]

        if centroid!=[]:
            for x in centroid:
                copy_centroid.append(x)

        self._centroid=copy_centroid

        self._name=name
        self._indices=[]


    def getCentroid(self):
        """
        Returns the centroid of this cluster. Does not return a copy.

        This getter method is to protect access to the centroid.
        """
        return self._centroid


    def getName(self):
        """
        Returns the name of this centroid.

        This getter method is to protect access to the centroid.
        """

        return self._name


    def setName(self,name):
        """
        Sets the name of this centroid.

        Precondition: name is a string
        """
        self._name=name


    def getIndices(self):
        """
        Returns the indices of points in this cluster

        This method returns the attribute _indices directly.  Any changes made to this
        list will modify the cluster.
        """

        return self._indices


    def addIndex(self, index):
        """
        Adds the given dataset index to this cluster.

        If the index is already in this cluster, this method leaves the
        cluster unchanged.

        Precondition: index is a valid index into this cluster's dataset.
        That is, index is an int in the range 0.._dataset.getSize()-1.
        """
        assert type(index)==int
        assert 0 <= index <self._dataset.getSize()

        if index in self._indices :
            pass
        else:
            self._indices.append(index)


    def clear(self):
        """
        Removes all points from this cluster, but leave the centroid unchanged.
        """
        self._indices.clear()


    def getContents(self):
        """
        Returns a new list containing copies of the points in this cluster.

        The result is a list of list of numbers.  It has to be computed from the indices.
        """
        new_list=[]
        for points in self._indices:
            new_list.append(self._dataset.getPoint(points))
        return new_list


    # Part B
    def distance(self, point):
        """
        Returns the euclidean distance from point to this cluster's centroid.

        Parameter point: The point to be measured
        Precondition: point is a list of numbers (int or float), with the same dimension
        as the centroid.
        """
        assert a6checks.is_point(point)
        assert len(point) == len(self._centroid)

        distance=0

        for int in range (len(self._centroid)):
            distance +=(point[int] - self._centroid[int])**2
        distance = math.sqrt(distance)
        return distance


    def getRadius(self):
        """
        Returns the maximum distance from any point in this cluster, to the centroid.

        This method loops over the contents to find the maximum distance from the centroid.
        """
        list_distances=[]
        for sublists in self.getContents():
            x=self.distance(sublists)
            list_distances.append(self.distance(sublists))

        return max(list_distances)



    def update(self):
        """
        Returns True if the centroid remains the same after recomputation; False otherwise.

        This method recomputes the _centroid attribute of this cluster. The new _centroid
        attribute is the average of the points of _contents (To average a point, average
        each coordinate separately).

        Whether the centroid "remained the same" after recomputation is determined by
        numpy.allclose.  The return value should be interpreted as an indication of whether
        the starting centroid was a "stable" position or not.

        If there are no points in the cluster, the centroid. does not change.
        """
        contents=self.getContents()
        if len(contents)==0:
            pass

        dimension=self._dataset.getDimension()

        list_sum = [0]*dimension
        for points in self.getContents():
        #    if row index is 0 then append to outside list
            for i in range(len(points)):
                list_sum[i] += points[i]

        divde_by=len(contents)

        for n in range(len(list_sum)):
            list_sum[n]=list_sum[n]/divde_by



        #check if list_sum == original centriod
        final= numpy.allclose(self._centroid, list_sum)

        self._centroid=list_sum
        return final


    def findError(self):
        """
        Returns: a float representing the total error of the centroid.

        The total error is calculated as the total squared distance from every point
        belonging to that centroid to the center of the centroid.

        For example, if their is 2 points, one 1 unit from the center and another point
        2 units from the center the error for this centroid would be 5 as we have
        1 * 1 + 2 * 2 = 5.

        Thus we would return 5.0

        Hint: The method distance() will he helpful.
        """
        error=0
        for x in self.getContents():
            distance=self.distance(x)
            error+=distance**2
        return error


    # PROVIDED METHODS: Do not modify!
    def __str__(self):
        """
        Returns a String representation of the centroid of this cluster.
        """
        return str(self._centroid)


    def __repr__(self):
        """
        Returns an unambiguous representation of this cluster.

        You do NOT have to use this function in your implementation if you do not want
        to. This provides more infomation for assert statements and can be used
        in place of the str method however, this method is deemed out of scope for
        A6 ,so do not stress if you do not understand __repr__.
        """
        return str(self.__class__) + str(self)

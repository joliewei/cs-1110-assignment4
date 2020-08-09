"""
Dataset for k-Means clustering

This file contains the class Dataset, which is the very first part of the assignment.
You cannot do anything in this assignment (except run the unit test) before this class
is finished.

Jolie Wei jw2493 and Jacob Yetter jay53
04/16/19
"""
import math
import random
import numpy
import a6helpers


# For checking preconditions
import a6checks

# CLASSES FOR THE ASSIGNMENT
class Dataset(object):
    """
    A class representing a dataset for k-means clustering.

    The data is stored as a list of list of numbers (ints or floats).  Each component
    list is a data point.

    INSTANCE ATTRIBUTES:
        _dimension: the point dimension for this dataset
                    [int > 0. Value never changes after initialization]
        _contents:  the dataset contents
                    [a list of lists of numbers (float or int), possibly empty.
    EXTRA INVARIANTS:
        The number of columns in _contents is equal to _dimension.  That is, for every
        item _contents[i] in the list _contents, len(_contents[i]) == dimension.

    None of the attributes should be accessed directly outside of the class Dataset
    (e.g. in the methods of class Cluster or KMeans). Instead, this class has getter and
    setter style methods (with the appropriate preconditions) for modifying these values.
    """


    def __init__(self, dim, contents=None,song_ids=[]):
        """
        Initializes a database for the given point dimension.

        The optional parameter contents is the initial value of the attribute _contents.
        When assigning contents to the attribute _contents it COPIES the list contents.
        If contents is None, the initializer assigns _contents an empty list. The
        parameter contents is None by default.

        The optional parameter song_ids is the initial value of the attribute _song_ids.
        If song_ids is the empty list, the initializer assigns _song_ids an empty list. The
        parameter song_ids is the empty list by default.

        Parameter dim: The dimension of the dataset
        Precondition: dim is an int > 0

        Parameter contents: the dataset contents
        Precondition: contents is either None or it is a table of numbers (int or float).
        If contents is not None, then contents if not empty and the number of columns is
        equal to dim.

        Parameter song_ids: the ids of songs in the playlist.
        Precondition: song_ids is either the empty list or a list of the same length of contents
        """
        assert a6checks.is_dimension(dim),'dim is not a valid dimension'
        assert a6checks.is_point_list(contents),'contents are not valid contents'
        assert a6checks.is_song_id(song_ids),'song_ids is not a valid son_id'
        self.dim = dim
        copy_contents=[]


        if contents!=None:
            for row in contents:
                point=[]
                for item in row:
                    point.append(item)
                copy_contents.append(point)

        self._contents = copy_contents

        self._song_ids = song_ids


    def getDimension(self):
        """
        Returns the point dimension of this data set
        """
        return self.dim


    def getSongIds(self):
        """
        Returns the song ids of this data set
        """
        return self._song_ids


    def getSize(self):
        """
        Returns the number of elements in this data set.
        """
        if self._contents==None:
            return 0
        else:
            return len(self._contents)


    def getContents(self):
        """
        Returns the contents of this data set as a list.

        This method returns the attribute _contents directly.  Any changes made to this
        list will modify the data set.  If you want to access the data set, but want to
        protect yourself from modifying the data, use getPoint() instead.
        """
        if self._contents==None:
            return []
        else:
            return self._contents


    def getPoint(self, i):
        """
        Returns a COPY of the point at index i in this data set.

        Often, we want to access a point in the data set, but we want a copy to make sure
        that we do not accidentally modify the data set.  That is the purpose of this
        method.

        If you actually want to modify the data set, use the method getContents().
        That returns the list storing the data set, and any changes to that
        list will alter the data set.

        Parameter i: the index position of the point
        Precondition: i is an int that refers to a valid position in 0..getSize()-1
        """
        assert type(i)==int

        copy_point=[]
        for items in self._contents[i]:
            copy_point.append(items)
        return copy_point


    def addPoint(self,point):
        """
        Adds a COPY of point at the end of _contents.

        This method does not add the point directly. It adds a copy of the point.

        Precondition: point is a list of numbers (int or float),  len(point) = _dimension."""

        assert a6checks.is_point(point)
        assert len(point)==self.dim

        copy_point=[]
        for items in point:
            copy_point.append(items)
        self._contents.append(copy_point)



    def standardize(self):
        """
        Standardizes the contents of dataset.

        Modifies every point.
        """
        l = self.getContents()
        if len(l) == 0:
            return
        for dim in range(len(l[0])):
            mean = a6helpers.find_mean(l,dim)
            std = a6helpers.find_std(l,dim)
            for x in range(len(l)):
                if std != 0:
                    l[x][dim] = (l[x][dim] - mean)/std

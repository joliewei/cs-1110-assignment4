"""
Helper functions for k-Means clustering

This file contains the functions for enforcing preconditions for k-means clustering.
We have written the first for you.  You will probably want to write others.

Jolie Wei jw2493 and Jacob Yetter jay53
04/16/19
"""
import math
import random
import numpy
import a6dataset


def is_point(value):
    """
    Returns True if value is a list of int or float

    Parameter value: a value to check
    Precondition: value can be anything
    """
    if not(type(value)==list):
        return False
    #[1.0,2]
    # status = True
    for x in value:
        # # point = True
        if not (type(x)==int or type(x)==float):
            return False
        # if (type(x)!=int and type(x)!=float)):
        #     status =  False
    return True


# ADD MORE HELPER FUNCTIONS FOR ASSERTS HERE
def is_point_list(value):
    """
    Returns True if value is a 2d list of int or float

    This function also checks that all points in value have same dimension.

    Parameter value: a value to check
    Precondition: value can be anything
    """
    if value == None:
        return True
    if type(value)!= list:
        return False
    for i in range(len(value)):

        if not is_point(value[i]):
            return False
        if i!=len(value)-1 and len(value[i])!=len(value[i+1]):
            return False
    return True


def is_seed_list(value, k, size):
    """
    Returns True if value is k-element list of indices between 0 and (len - 1).

    Parameter value: a value to check
    Precondition: value can be anything

    Parameter k: The required list size
    Precondition: k is an int > 0

    Paramater size: The database size
    Precondition: size is an int > 0
    """
    if not(type(k)==int and k>0):
        return False
    if not(type(size)==int and size>0):

        return False

    if len(value)==k:
        for element in value:
            if not(element>=0 and element<(size)):
                return False
        return True


def is_dimension(value):
    """
    Returns True if value is an integer greater than 0

    Parameter value: a value to check
    Precondition: value can be anything
    """

    return (type(value)==int and value > 0)


def is_song_id(value):
    """
    Returns True if value is either an empty list a list of the same length of
    contents

    Parameter value: a value to check
    Precondition: value can be anything
    """
    return (value == [] or len(value)==len(contents))


def is_dset(value):
    """
    Returns True if dset is an instance of Dataset

    Parameter value: a value to check
    Precondition: value can be anything
    """

    return isinstance(value, a6dataset.Dataset)


def is_centroid(value):
    """
    Returns True if centroid is a list of dset.getDimension() numbers

    Parameter value: a value to check
    Precondition: value can be anything
    """

    return type(value)==list and len(value)==getDimension


def is_name(value):
    """
    Returns True if name is string

    Parameter value: a value to check
    Precondition: value can be anything
    """

    return type(name)==str

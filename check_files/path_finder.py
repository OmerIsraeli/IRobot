import socket
import time
import pickle

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from roboviz import MapVisualizer
import numpy as np
from scipy.interpolate import interp1d


def get_directions(map,loc,theta):
    """

    :param map: map of {1,2,3} where 1 is empty, 2 is visited , 3 blocked
    :param loc: my locations
    :param theta: the direction of Rufus
    :return: the track for rufus
    """

    ##
    map_areas= parse_map(map)
    area_loc= find_my_area(map,loc)
    loc1,loc2=find_2_best_areas(map_areas)
    next_loc=find_next_loc(map_areas,area_loc,loc1,loc2,loc)
    track = build_track(map_areas,loc, next_loc,theta)
    return track





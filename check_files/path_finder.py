import socket
import time
import pickle

# from breezyslam.algorithms import RMHC_SLAM
# from breezyslam.sensors import RPLidarA1 as LaserModel
# from roboviz import MapVisualizer
import numpy as np

# from scipy.interpolate import interp1d


NUMBER_OF_ROWS = 10
NUMBER_OF_COLS = 10


def get_directions(map, loc, theta):
    """

    :param map: map of {1,2,3} where 1 is empty, 2 is visited , 3 blocked
    :param loc: my locations
    :param theta: the direction of Rufus
    :return: the track for rufus
    """

    # parsing the map areas
    map_areas = parse_map(map, NUMBER_OF_ROWS, NUMBER_OF_COLS)

    # find the area of the cur location of rufus in (i,j)
    area_loc = find_my_area(map, loc)

    # find the best areas for getting forward
    loc1= find_best_area(area,map_areas)

    #
    next_loc = find_next_loc(map_areas, area_loc, loc1, loc)
    track = build_track(map_areas, loc, next_loc, theta)
    return track


def parse_map(map, nor, noc):
    map = np.resize(map, (map.shape[0] + nor - map.shape[0] % nor, map.shape[1] + noc - map.shape[1] % noc))
    map_areas = [[map[nor * i:nor * (i + 1), noc * j:noc * (j + 1)] for j in range(map.shape[1])] for i in
                 range(map.shape[0])]
    return np.array(map_areas)


def find_my_area(loc, nor, noc):
    return [loc[0] // nor, loc[1] // noc]


def find_best_area(area_loc, areas):
     best_loc = (0,0)
     best_loc_param = 0
     for i in range(area_loc[0]):
         for j in range(area_loc[1]):
             pass




def find_next_loc(map_areas, area_loc, loc1, loc2, loc):
    pass


def build_track(map_areas, loc, next_loc, theta):
    pass


nor = NUMBER_OF_ROWS
noc = NUMBER_OF_COLS
arr = np.array([[1, 1], [1, 1]])
map = np.pad(arr, (0, nor - arr.shape[0] % nor), (0, noc - arr.shape[1] % noc), 'constant', constant_values=(0, 0))
print(map)

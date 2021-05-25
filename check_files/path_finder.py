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
EMPTY = 1
VISITED = 2
BLOCKED = 3


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
    loc1 = find_best_area(area_loc, map_areas)

    # find our next loc
    next_loc = find_next_loc(map, map_areas, area_loc, loc1, loc)

    # build track of rufus
    track = build_track(map_areas, loc, next_loc, theta)

    track = adjust_track(track)
    return track


def parse_map(map, nor, noc):
    map = np.resize(map, (map.shape[0] + nor - map.shape[0] % nor, map.shape[1] + noc - map.shape[1] % noc))
    map_areas = [[map[nor * i:nor * (i + 1), noc * j:noc * (j + 1)] for j in range(map.shape[1])] for i in
                 range(map.shape[0])]
    return np.array(map_areas)


def find_my_area(loc, nor, noc):
    return [loc[0] // nor, loc[1] // noc]


def find_best_area(area_loc, areas):
    best_loc = [0, 0]
    best_loc_param = 0
    for i in range(area_loc[0]):
        for j in range(area_loc[1]):
            dist = np.sqrt((i - area_loc[0]) ** 2 + (j - area_loc[1]) ** 2)
            param = dist * np.count_nonzero(areas[i, j] == EMPTY)
            if param < best_loc_param:
                best_loc_param = param
                best_loc = [i, j]
    return best_loc


def find_next_loc(map, map_areas, area_loc, loc1, loc):
    # loc1 = [int(map.shape[0]/NUMBER_OF_ROWS*(loc1[0]+1/2)),int(map.shape[1]/NUMBER_OF_COLS*(loc1[1]+1/2))]
    # area_loc_new = [int(map.shape[0]/NUMBER_OF_ROWS*(area_loc[0]+1)-1),int(map.shape[1]/NUMBER_OF_COLS*(area_loc[
    #                                                                                                         1]+1)-1)]
    # m, c = np.linalg.lstsq(np.array([loc, loc1]), [loc[1], loc1[1]], rcond=None)[0]
    new_loc = loc
    if area_loc[0] < loc1[0]:
        if (area_loc[1] > loc1[1]):
            new_loc = [int(map.shape[0] / NUMBER_OF_ROWS) - 1, 0]
        else:
            new_loc = [int(map.shape[0] / NUMBER_OF_ROWS) - 1, int(map.shape[1] / NUMBER_OF_COLS) - 1]
    else:
        if (area_loc[1] > loc1[1]):
            new_loc = [0, 0]
        else:
            new_loc = [0, int(map.shape[1] // NUMBER_OF_COLS) - 1]
    return new_loc


def change_angle_to_hor(idx_hor, theta):
    if idx_hor:
        if theta < 90 or theta > 270:
            return 'd', abs(90 - theta)
        else:
            return 'a', abs(90 - theta)
    else:
        if theta < 90 or theta > 270:
            return 'd', abs(270 - theta)
        else:
            return 'a', abs(270 - theta)


def change_angle_to_ver(idx_hor, idx_ver):
    if idx_hor:
        if idx_ver:
            return 'a', 90
        else:
            return 'd', 90
    else:
        if idx_ver:
            return 'd', 90
        else:
            return 'a', 90


def build_track(map, loc, next_loc, theta):
    idx_hor= loc[0]< next_loc[0]
    idx_ver= loc[1]<next_loc[1]
    track = []
    d, angle = change_angle_to_hor(idx_hor, theta)
    track += [d, angle]
    timee = time.time()
    flag = True
    while time.time() - timee < 30 and flag:
        for i in range(map.shape[1] // NUMBER_OF_COLS):
            track += ['w', 0]
            loc = [loc[0] + 1, loc[1]]
            if map[loc] == BLOCKED or loc[1] == next_loc[1]:
                d, angle = change_angle_to_ver(idx_hor, idx_ver)
                track += [d, angle]
                for j in range(map.shape[0] // NUMBER_OF_ROWS):
                    track += ['w', 0]
                    loc = [loc[0], loc[1] + 1]
                    if map[loc] == BLOCKED or loc[0] == next_loc[0]:
                        break
                break
        if loc[0] == next_loc[0] and loc[1] == next_loc[1]:
            flag = False
    return track


def adjust_track(track):
    new_track= []
    for step in track:
        if len(new_track)==0:
            new_track += [step]
        else:
            if new_track[-1][0]== step[0] and new_track[-1][0]=='w':
                new_track[-1][1]+=1
            else:
                new_track += [step]
    return new_track

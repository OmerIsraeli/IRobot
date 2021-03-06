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


def get_directions(next_loc,loc, theta,track,idx_hor):

    # build track of rufus
    if len(track)==0:
        d,angle=change_angle_to_hor(idx_hor,theta)
        track =[(d,0.5,angle)]
    elif idx_hor!= loc[0]<next_loc[0]:
        d,angle=change_angle_to_ver(idx_hor,loc[1]<next_loc[1])
        track = [(d, 0.5, angle)]
    else:
        track= [track[-1]]
    track += [('w',0.5,0)]

    # track = adjust_track(track)
    return track


def parse_map(map, nor, noc):
    map = np.resize(map, (map.shape[0] + nor - map.shape[0] % nor, map.shape[1] + noc - map.shape[1] % noc))
    map_areas = [[map[nor * i:nor * (i + 1), noc * j:noc * (j + 1)] for j in range(NUMBER_OF_COLS)] for i in
                 range(NUMBER_OF_ROWS)]
    return np.array(map_areas)


#TODO check if i have mistake
def find_my_area(loc, nor, noc):
    return [int(loc[0] // nor), int(loc[1] // noc)]


def find_best_area(area_loc, areas):
    best_loc = [0, 0]
    best_loc_param = 0
    for i in range(area_loc[0]):
        for j in range(area_loc[1]):
            dist = np.sqrt((i - area_loc[0]) ** 2 + (j - area_loc[1]) ** 2)
            param = dist / np.count_nonzero(areas[i, j] == EMPTY)
            if param < best_loc_param or i == j == 0:
                best_loc_param = param
                best_loc = [i, j]
    return best_loc


def find_next_loc(map, map_areas, area_loc, next_loc_area):
    # next_loc_area = [int(map.shape[0]/NUMBER_OF_ROWS*(loc1[0]+1/2)),int(map.shape[1]/NUMBER_OF_COLS*(loc1[1]+1/2))]
    # area_loc_new = [int(map.shape[0]/NUMBER_OF_ROWS*(area_loc[0]+1)-1),int(map.shape[1]/NUMBER_OF_COLS*(area_loc[
    #                                                                                                         1]+1)-1)]
    # m, c = np.linalg.lstsq(np.array([loc, loc1]), [loc[1], loc1[1]], rcond=None)[0]
    if area_loc[0] < next_loc_area[0]:
        if area_loc[1] > next_loc_area[1]:
            new_loc = [int(map.shape[0] // NUMBER_OF_ROWS) - 1, 0]
        else:
            new_loc = [int(map.shape[0] // NUMBER_OF_ROWS) - 1, int(map.shape[1] // NUMBER_OF_COLS) - 1]
    else:
        if area_loc[1] > next_loc_area[1]:
            new_loc = [0, 0]
        else:
            new_loc = [0, int(map.shape[1] // NUMBER_OF_COLS) - 1]
    new_loc=[next_loc_area[0]*int(map.shape[0] // NUMBER_OF_ROWS)+new_loc[0],next_loc_area[1]*int(map.shape[1] //
                                                                                                 NUMBER_OF_COLS)+new_loc[1]]
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

#
# def build_track(map, loc, next_loc, theta):
#     idx_hor = loc[0] < next_loc[0]
#     idx_ver = loc[1] < next_loc[1]
#     track = []
#
#     track += [d, 0, angle]
#     steps = 0
#     not_reached_dst = True
#     while steps < 30 and not_reached_dst:
#         for i in range(map.shape[1] // NUMBER_OF_COLS):
#             track += ['w', 1, 0]
#             loc = [loc[0] + 1, loc[1]]
#             steps += 1
#             if map[loc] == BLOCKED or loc[1] == next_loc[1]:
#                 d, angle = change_angle_to_ver(idx_hor, idx_ver)
#                 track += [d, 0, angle]
#                 for j in range(map.shape[0] // NUMBER_OF_ROWS):
#                     track += ['w', 1, 0]
#                     loc = [loc[0], loc[1] + 1]
#                     if map[loc] == BLOCKED or loc[0] == next_loc[0]:
#                         break
#                 break
#         if loc[0] == next_loc[0] and loc[1] == next_loc[1]:
#             not_reached_dst = False
#     return track+['w',1,0]


def adjust_track(track):
    new_track = []
    for step in track:
        if len(new_track) == 0:
            new_track += [step]
        else:
            if new_track[-1][0] == step[0] and new_track[-1][0] == 'w':
                new_track[-1][1] += 1
            else:
                new_track += [step]
    return new_track


def get_next_loc(map,loc,theta):
    """
    :param map: map of {1,2,3} where 1 is empty, 2 is visited , 3 blocked
    :param loc: my locations
    :param theta: the direction of Rufus
    :return: the new location of rufus
    """

    # parsing the map areas
    map_areas = parse_map(map, map.shape[0]//NUMBER_OF_ROWS, map.shape[1]//NUMBER_OF_COLS)

    # find the area of the cur location of rufus in (i,j)
    area_loc = find_my_area(loc,  map.shape[0]//NUMBER_OF_ROWS, map.shape[1]//NUMBER_OF_COLS)

    # find the best areas for getting forward
    next_loc_area = find_best_area(area_loc, map_areas)

    # find our next loc
    next_loc = find_next_loc(map, map_areas, area_loc, next_loc_area)
    return next_loc
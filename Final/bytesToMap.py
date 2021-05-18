import numpy as np
MAP_SIZE_PIXELS = 500


def b2img(bytearray ,mapbytes, pixels = MAP_SIZE_PIXELS):
    map = np.zeros((pixels, pixels))
    for i in range(pixels):
        for j in range(pixels):
            map[i][j] = mapbytes[i * pixels + j]
    return map
    

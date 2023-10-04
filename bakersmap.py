# SPDX-FileCopyrightText: Ondřej Surý
#
# SPDX-License-Identifier: WTFPL

import numpy as np

def bakers_rev(arr):
    shape = arr.shape

    n_y = shape[0]
    n_x = shape[1]
    h_x = int(n_x / 2)
    d_y = 2 * n_y

    orig = np.empty(shape, dtype=np.uint8)
    
    for y2 in range(n_y):
        for x2 in range(n_x):

            x3 = int(x2 / 2)
            y3 = 2 * y2 + 1 - (x2 % 2)

            if (y3 < n_y):
                x4 = int(x3 + (n_x / 2))
                y4 = y3
            else:
                x4 = x3
                y4 = y3 - n_y

            orig[int(y4), int(x4)] = arr[y2, x2]
    
    return orig


def bakers(arr):
    shape = arr.shape

    n_y = shape[0]
    n_x = shape[1]
    h_x = int(n_x / 2)
    d_y = 2 * n_y

    fold = np.empty(shape, dtype=np.uint8)
    
    for y0 in range(n_y):
        for x0 in range(n_x):

            if (x0 < h_x):
                x1 = x0
                y1 = y0 + n_y
            else:
                x1 = x0 - h_x
                y1 = y0

            x2 = 2 * x1 + 1 - (y1 % 2)
            y2 = y1 / 2

            fold[int(y2), int(x2)] = arr[y0, x0]
    
    return fold

def bytes2array(size, bytes_):
    x_size, y_size = size
    arr = np.zeros((y_size, x_size), dtype=np.uint8)
    i = 0

    bytes = np.unpackbits(np.array(bytes_, dtype=np.uint8))
    
    for y in range(y_size):
        for x in range(x_size):
            if i < bytes.shape[0]:
                arr[y][x] = bytes[i]
                i += 1
            else:
                break
        if i >= bytes.shape[0]:
            break

    return arr

def array2bytes(size, arr_):
    x_size, y_size = int(size[0] / 8), size[1]
    i = 0
    bytes = np.empty(x_size * y_size, dtype=np.uint8)
    arr = np.packbits(arr_, axis=1)
    for y in range(y_size):
        for x in range(x_size):
            if i < bytes.shape[0]:
                bytes[i] = arr[y][x]
                i += 1
            else:
                break
        if i >= bytes.shape[0]:
            break

    return bytes.tobytes()
    
import sys

np.set_printoptions(threshold=sys.maxsize, edgeitems=sys.maxsize, linewidth=sys.maxsize)

# Create an initial 2D array with desired values
# array_size = 10
# initial_array = bytes2array((array_size, array_size), b"hidden text hidden text hidden text")

# print("====== initial ======")
# print(initial_array)

# N = 1019
    
# Apply Baker's map to the initial 2D array
# transformed_array = initial_array
# for n in range(N):
#     transformed_array = bakers(transformed_array)

# print("====== transformed ======")
# print(transformed_array)

# Apply reverse Baker's map to the transformed 2D array
# retransformed_array = transformed_array
# for n in range(N):
#     retransformed_array = bakers_rev(retransformed_array)

# print("====== retransformed ======")
# print(retransformed_array)

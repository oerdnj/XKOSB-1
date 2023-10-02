#!/usr/bin/env python3

# SPDX-FileCopyrightText: Ondřej Surý
#
# SPDX-License-Identifier: WTFPL

import sys,tempfile
import numpy as np
import pyqrcode
from PIL import Image
from pathlib import Path

import bakersmap

def usage():
    print(f"{sys.argv[0]} <file.png> 'visible text' 'hidden text'")

if len(sys.argv) != 4:
    usage()

crouching_tiger = sys.argv[2]

hidden_dragon = sys.argv[3]

qr = pyqrcode.create(crouching_tiger)

_, fn = tempfile.mkstemp(suffix=".png")

qr.png(fn, scale=8)
with Image.open(fn) as im:
    x_size, y_size = int(im.size[0] / 8) , im.size[1]
    arr = bakersmap.bytes2array((x_size, y_size), im.tobytes())
    
Path.unlink(fn)

x_offset = 8
y_offset = 8*8

xx_size = x_size - (2 * x_offset) - 1
yy_size = y_size - (2 * y_offset) - 1

xor = bakersmap.bytes2array((xx_size, yy_size), bytearray(hidden_dragon, "UTF-8"))

N=1019

for n in range(N):
    xor = bakersmap.bakers(xor)

narr = np.array(arr, dtype=np.uint8)
for y in range(yy_size):
    for x in range(xx_size):
        narr[y + y_offset][x + x_offset] ^= xor[y][x]

new_im = Image.frombytes(data=bakersmap.array2bytes((x_size, y_size), narr), mode='1', size=im.size)

new_im.save(sys.argv[1])

#!/usr/bin/env python3

# SPDX-FileCopyrightText: Ondřej Surý
#
# SPDX-License-Identifier: WTFPL

import sys,tempfile
import numpy as np
from array import array
import pyqrcode
from PIL import Image
from pathlib import Path

import bakersmap

def usage():
    print(f"{sys.argv[0]} <file.png> 'visible text' 'hidden text'")

if len(sys.argv) != 4:
    usage()

crouching_tiger = sys.argv[2]

hidden_dragon = sys.argv[3].encode('UTF-8')

qr = pyqrcode.create(crouching_tiger, mode='binary', encoding='UTF-8')

_, fn = tempfile.mkstemp(suffix=".png")

qr.png(fn, scale=8)
with Image.open(fn) as im:
    x_size, y_size = im.size
    arr = bakersmap.bytes2array((x_size, y_size), array('B', im.tobytes()))
    
Path.unlink(fn)

xarr = bakersmap.bytes2array((x_size, y_size), array('B', hidden_dragon))

#N=1019
N=13

for n in range(N):
    xarr = bakersmap.bakers(xarr)

narr = np.array(arr, dtype=np.uint8)
for y in range(y_size):
    for x in range(x_size):
        narr[y][x] ^= xarr[y][x]

new_im = Image.frombytes(data=bakersmap.array2bytes((x_size, y_size), narr), mode='1', size=im.size)

new_im.save(sys.argv[1])

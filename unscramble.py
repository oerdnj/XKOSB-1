#!/usr/bin/env python3

# SPDX-FileCopyrightText: Ondřej Surý
#
# SPDX-License-Identifier: WTFPL

import sys, tempfile
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import pyqrcode
from pathlib import Path
from array import array

import bakersmap

def usage():
    print(f"{sys.argv[0]} <file.png>")

if len(sys.argv) != 2:
    usage()

with Image.open(sys.argv[1]) as im:
    x_size, y_size = im.size
    arr = bakersmap.bytes2array((x_size, y_size), array('B', im.tobytes()))

qr = decode(im)
crouching_tiger = qr[0].data.decode('UTF-8')

qr = pyqrcode.create(crouching_tiger, mode='binary', encoding='UTF-8')

_, fn = tempfile.mkstemp(suffix=".png")

qr.png(fn, scale=8)
with Image.open(fn) as im:
    xarr = bakersmap.bytes2array((x_size, y_size), array('B', im.tobytes()))

Path.unlink(fn)

narr = np.array(arr, dtype=np.uint8)
for y in range(y_size):
    for x in range(x_size):
        narr[y][x] ^=  xarr[y][x]

#N=1019
N=13

for n in range(N):
    narr = bakersmap.bakers_rev(narr)
        
hidden_dragon = bakersmap.array2bytes((x_size, y_size), narr).decode('UTF-8')
        
print(hidden_dragon)

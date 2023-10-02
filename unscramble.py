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

import bakersmap

def usage():
    print(f"{sys.argv[0]} <file.png>")

if len(sys.argv) != 2:
    usage()

with Image.open(sys.argv[1]) as im:
    x_size, y_size = int(im.size[0] / 8) , im.size[1]
    arr = bakersmap.bytes2array((x_size, y_size), im.tobytes())

qr = decode(im)
crouching_tiger = qr[0].data.decode('UTF-8')

qr = pyqrcode.create(crouching_tiger)

_, fn = tempfile.mkstemp(suffix=".png")

qr.png(fn, scale=8)
with Image.open(fn) as im:
    xor_arr = bakersmap.bytes2array((x_size, y_size), im.tobytes())

Path.unlink(fn)

x_offset = 8
y_offset = 8*8

xx_size = x_size - (2 * x_offset) - 1
yy_size = y_size - (2 * y_offset) - 1

narr = np.empty((yy_size, xx_size), dtype=np.uint8)
for y in range(yy_size):
    for x in range(xx_size):
        narr[y][x] = arr[y + y_offset][x + x_offset] ^ xor_arr[y + y_offset][x + x_offset]

N=1019

for n in range(N):
    narr = bakersmap.bakers_rev(narr)
        
hidden_dragon = bakersmap.array2bytes((xx_size, yy_size), narr).decode("UTF-8")
        
print(hidden_dragon)

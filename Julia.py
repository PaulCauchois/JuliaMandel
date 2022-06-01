# Créé par Paul Cauchois, licence CC-BY 4.0
from PIL import Image as im
import time
import numpy as np
import math
import os

im.MAX_IMAGE_PIXELS = None
# Parameters :
hor = 4096
ver = int(9 * hor / 16)
Uleft = -1.9 + 1.2j
Lower = -0.2j
c = -0.70+0.32j
Saturation = 240
Value = 184
color_cycle = 232
color_start = color_cycle*2/3
n = 500
# - - - - - - - -
R = (1 + math.sqrt(1 + 4 * abs(c))) / 2
Lright = Lower + (Uleft - Lower).imag * hor / ver
step = (Lright - Uleft).real / (hor - 1)


def julia_iter(plane, n_iter):
    N_iters = np.zeros_like(plane, dtype=np.int64)
    for i in range(n_iter):
        print(f"    • Iteration #{i + 1}/{n_iter}.")
        N_iters = np.where(np.abs(plane) < R, N_iters + 1, N_iters)
        plane = np.where(np.abs(plane) < R, np.square(plane) + c, plane)
    return N_iters

space = np.zeros((ver, hor), dtype=complex)
N = np.zeros_like(space, dtype=np.uint16)

print("Creating matrix...")
t = time.time()
for x in range(hor):
    for y in range(ver):
        z = Uleft + x * step - y * step * 1j
        space[y][x] = z
matrix_time = time.time() - t
print(f"Done in {matrix_time} seconds.")

print("Computing set :")
t = time.time()
N = julia_iter(space, n)
comp_time = time.time() - t
print(f"Done in {time.time() - t} seconds.")
print("Creating image :")

print("    • Computing Hue")
H = np.where(N == n, np.zeros_like(N), np.floor(255 * np.array(((N+color_start) / color_cycle) % 1)))
print("    • Computing Saturation")
S = np.where(N == n, 0, Saturation)
print("    • Computing Value")
V = np.where(N == n, 0, Value)

I = np.stack((H, S, V))
I = np.uint8(np.moveaxis(I, 0, -1))

image = im.fromarray(I, mode="HSV")
new = image.convert("RGB")

try:
    os.mkdir(f"Pictures/Julia set of {c}")
    print("Folder not found, creating...")
except FileExistsError:
    print("Folder found, adding new picture...")

new.save(f"Pictures/Julia set of {c}/{hor},{color_cycle}@{n} from {Uleft}.png")
print("Picture added")
'''
print("Creating log file...")
with open(f"Pictures/Julia set of {c}/{hor},{color_cycle}@{n} from {Uleft}.log", 'w') as log:
    log.write(f"c = {c}\n"
              f"Dimensions : {hor} by {ver} pixels\n"
              f"Number of pixels = {hor * ver}\n"
              f"Upper left corner = {Uleft}\n"
              f"Lower bound = {Lower}\n"
              f"Color cycle length = {color_cycle}\n"
              f"Radius of convergence = {R}\n----------\n"
              f"Time to create matrix = {matrix_time} seconds\n"
              f"Pixels per second = {hor * ver / matrix_time}\n"
              f"Time to compute set = {comp_time} seconds\n"
              f"Time per iteration = {comp_time / n} seconds\n"
              f"Pixels per second = {hor * ver * n / comp_time}\n"
              f"____________________")
'''

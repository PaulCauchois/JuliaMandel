# Créé par Paul Cauchois, licence CC-BY 4.0
from PIL import Image as im
import time
from numba import cuda, jit
import numpy as np
import math
import os

im.MAX_IMAGE_PIXELS = None
# Parameters :
hor = 32768
ver = int(9 * hor / 16)
Uleft = -2.3 + 1.2j
Lower = 0
color_start = 0
color_cycle = 64
Saturation = 255
Value = 255
n = 200
# - - - - - - - -
R = 2
Lright = Lower + (Uleft - Lower).imag * hor / ver
step = (Lright - Uleft).real / (hor - 1)


def mandel_iter(plane, n_iter):
    N_iters = np.zeros_like(plane, dtype=np.int64)
    T = np.copy(plane)
    Easy = np.logical_not(np.logical_or(np.abs(plane - 1 / 4) < 1 / 2 - 1 / 2 * np.cos(np.angle(plane - 1 / 4)),
                         np.abs(plane + 1) < 1 / 4))
    for i in range(n_iter):
        print(f"    • Iteration #{i + 1}/{n_iter}.")
        N_iters = np.where(np.abs(T) < R, N_iters + 1, N_iters)
        T = np.where(np.logical_and(Easy, T<R), np.square(T) + plane, T)
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
N = mandel_iter(space, n)
comp_time = time.time() - t
print(f"Done in {time.time() - t} seconds.")
print("Creating image :")

print("    • Computing Hue")
H = np.where(N == n, np.zeros_like(N), 255 * np.array(((N+color_start) / color_cycle) % 1))
print("    • Computing Saturation")
S = np.where(N == n, 0, Saturation)
print("    • Computing Value")
V = np.where(N == n, 0, Value)

I = np.stack((H, S, V))
I = np.uint8(np.moveaxis(I, 0, -1))

image = im.fromarray(I, mode="HSV")
new = image.convert("RGB")

try:
    os.mkdir(f"Pictures/Mandelbrot set")
    print("Folder not found, creating...")
except FileExistsError:
    print("Folder found, adding new picture...")

new.save(f"Pictures/Mandelbrot set/{hor},{color_cycle}@{n} from {Uleft}.png")
print("Picture added")

print("Creating log file...")
with open(f"Pictures/Mandelbrot set/{hor},{color_cycle}@{n} from {Uleft}.log", 'w') as log:
    log.write(f"Dimensions : {hor} by {ver} pixels\n"
              f"Number of pixels = {hor * ver}\n"
              f"Upper left corner = {Uleft}\n"
              f"Lower bound = {Lower}\n"
              f"Color cycle length = {color_cycle}\n"
              f"Time to create matrix = {matrix_time} seconds\n"
              f"Pixels per second = {hor * ver / matrix_time}\n"
              f"Time to compute set = {comp_time} seconds\n"
              f"Time per iteration = {comp_time / n} seconds\n"
              f"Pixels per second = {hor * ver * n / comp_time}\n"
              f"____________________")

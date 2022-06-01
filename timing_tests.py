# Créé par Paul Cauchois, licence CC-BY 4.0
import timeit
import numpy as np
import math


def plane_1(hor, ver, Uleft, step):
    space = np.zeros((hor, ver), dtype=complex)
    for x in range(hor):
        for y in range(ver):
            z = Uleft + x * step - y * step * 1j
            space[x][y] = z
    return space


def plane_2(hor, ver, Uleft, step):
    p1 = ((x, x * step) for x in range(hor))
    p2 = [(y, y * step * 1j) for y in range(ver)]
    space = np.zeros((hor, ver), dtype=complex)

    while True:
        try:
            x, xcalc = next(p1)
            for y, ycalc in p2:
                space[x][y] = Uleft+xcalc-ycalc

        except StopIteration:
            break
    return space

def mandel_iter(plane, n_iter):
    N_iters = np.zeros_like(plane, dtype=np.int64)
    T = np.copy(plane)
    Easy = np.logical_or(np.abs(plane - 1 / 4) < 1 / 2 - 1 / 2 * np.cos(np.angle(plane - 1 / 4)),
                         np.abs(plane + 1) < 1 / 4)
    for i in range(n_iter):
        print(f"    • Iteration #{i + 1}/{n_iter}.")
        N_iters = np.where(np.abs(T) < 2, N_iters + 1, N_iters)
        T = np.where(np.abs(T)<2, np.square(T) + plane, T)
    return N_iters
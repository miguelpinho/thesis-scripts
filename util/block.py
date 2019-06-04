from random import randint, choice
import numpy as np

def round_block(prc, block):
    return (prc+block-1) & -block

blocks = [2, 4, 8, 16, 32, 64, 128]

for i in range(100):
    x = randint(0, 1000)
    b = choice(blocks)
    res = round_block(x, b)
    print("x={}, b={} --> res={}, div={}".
            format(x, b, res, res/b))



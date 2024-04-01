import sys
import random
import numpy as np
import MountainCarController as mc

initialized_list = list(np.zeros(32, int))

def random_flip(lookup_list):
    for i in lookup_list:
        if random.random() >= 0.9:
            i = 0 if i == 1 else 1
    return lookup_list

mc.lookup_list = random_flip(initialized_list)
mc.render_mode = None

mc.initialize()


for _ in range(100):
    mc.update()



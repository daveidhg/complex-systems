import pycxsimulator
import gymnasium as gym
from pylab import *

lookup_list = [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]

render_mode = 'human'
truncated = False
terminated = False
seed = 22

def wrapping_slice(lst, *args):
    return [lst[i % len(lst)] for i in range(*args)]

def bin_list_to_int(bin_list):
    return_val = 0
    for i, num in enumerate(bin_list): 
        return_val += num * (2 ** (4 - i))
    return return_val

def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

def concat_lists(*args):
    return_list = []
    for arg in args:
        return_list.extend(arg)
    return return_list

def observation_to_binary_list(observation, config):
    upper_bound = 127
    lower_bound = 0
    bin_pos = bin(int(round(scale_number(observation[0], lower_bound, upper_bound, -1.2, 0.6), 0)))
    bin_vel = bin(int(round(scale_number(observation[1], lower_bound, upper_bound, -0.07, 0.07), 0)))
    bin_pos = '0' * (9 - len(bin_pos)) + bin_pos[2:]
    bin_vel = '0' * (9 - len(bin_vel)) + bin_vel[2:]
    last_line = config[-1]
    pos_list = list(map(int, bin_pos))
    vel_list = list(map(int, bin_vel))
    return concat_lists(last_line[:6], pos_list, last_line[13:19], vel_list, last_line[26:])

def initialize():
    global env, config, iter_count, truncated, terminated, observation, seed # list global variables
    iter_count = 0
    env = gym.make(id='MountainCar-v0', render_mode=render_mode)
    observation, _ = env.reset(seed=seed)
    truncated = False
    terminated = False
    config = [observation_to_binary_list(observation, [[0 for _ in range(32)]])] 

def observe():
    global config # list global variables
    cla() # to clear the visualization space
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    # visualize system states

def update():
    global env, config, iter_count, terminated, truncated, observation

    # We take 5 iterations to let the algorithm get initialized before making a move.
    # To use the observations, we represent it in two 7 bit values for position and velocity.
    if iter_count % 10 == 0 and iter_count != 0:
        sample = mean(config[-1])
        controller_output = 0 if sample < 0.45 else 2 if sample > 0.55 else 1
        observation, reward, terminated, truncated, info = env.step(controller_output)
        config = [observation_to_binary_list(observation, config)]
    last_update = config[-1]
    this_update = []

    # We use the 4 closest neighbors of an observation to determine 
    # what value from the lookup string we should use to update the current element.
    for i in range(len(last_update)):
        this_update.append(lookup_list[bin_list_to_int(wrapping_slice(last_update, i - 2, i + 3))])
    config.append(this_update)
    iter_count += 1
    # update system states for one discrete time step

if __name__ == "__main__":
    pycxsimulator.GUI().start(func=[initialize, observe, update])

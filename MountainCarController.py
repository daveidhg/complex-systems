import pycxsimulator
import gymnasium as gym
from pylab import *

lookup_list = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1]

render_mode = 'human'
truncated = False
terminated = False

def wrapping_slice(lst, *args):
    return [lst[i % len(lst)] for i in range(*args)]

def bin_list_to_int(bin_list):
    return_val = 0
    for i, num in enumerate(bin_list): 
        return_val += num * (2 ** (4 - i))
    return return_val

def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

def observation_to_binary_list(observation):
    upper_bound = 127
    lower_bound = 0
    bin_pos = bin(int(round(scale_number(observation[0], lower_bound, upper_bound, -1.2, 0.6), 0)))
    bin_vel = bin(int(round(scale_number(observation[1], lower_bound, upper_bound, -0.07, 0.07), 0)))
    bin_pos = '0' * (9 - len(bin_pos)) + bin_pos[2:]
    bin_vel = '0' * (9 - len(bin_vel)) + bin_vel[2:]
    return list(map(int, bin_pos + bin_vel))

def initialize():
    global env, config, iter_count, truncated, terminated, observation # list global variables
    iter_count = 0
    env = gym.make(id='MountainCar-v0', render_mode=render_mode)
    observation, _ = env.reset()
    truncated = False
    terminated = False
    config = [observation_to_binary_list(observation)] 
    
def observe():
    global config # list global variables
    cla() # to clear the visualization space
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    # visualize system states

def update():
    global env, config, iter_count, terminated, truncated, observation

    # We take 5 iterations to let the algorithm get initialized before making a move.
    # To use the observations, we represent it in two 7 bit values for position and velocity.
    if iter_count % 5 == 0 and iter_count != 0:
        sample = mean([config[-1][4], config[-1][8], config[-1][10], config[-1][13]])
        controller_output = 0 if sample < 0.45 else 2 if sample > 0.55 else 1
        observation, reward, terminated, truncated, info = env.step(controller_output)
        config = [observation_to_binary_list(observation)]
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

import pycxsimulator
import sys
import gymnasium as gym
from pylab import *

def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

lookup_string = sys.argv[1]

def observation_to_binary_list(observation):
    upper_bound = 127
    lower_bound = 0
    bin_pos = bin(int(round(scale_number(observation[0], lower_bound, upper_bound, -1.2, 0.6), 0)))
    bin_vel = bin(int(round(scale_number(observation[1], lower_bound, upper_bound, -0.07, 0.07), 0)))
    bin_pos = '0' * (10 - len(bin_pos)) + bin_pos[2:]
    bin_vel = '0' * (10 - len(bin_vel)) + bin_vel[2:]
    return list(map(int, bin_pos + bin_vel))

def initialize():
    global env, config # list global variables
    env = gym.make(id='MountainCar-v0', render_mode="human")
    state, _ = env.reset()
    config = [observation_to_binary_list(state)] 
    
def observe():
    global config # list global variables
    cla() # to clear the visualization space
    imshow(config, vmin = 0, vmax = 2, cmap = cm.binary)
    # visualize system states

def update():
    global env, config
    controller_output = int(round(mean(config), 0))
    observation, reward, terminated, truncated, info = env.step(controller_output)
    scaled_pos_vel = observation_to_binary_list(observation)
    print(scaled_pos_vel)
    # scaled_position = scale_number(observation[0], 0, 2, -1.2, 0.6,)
    # scaled_velocity = scale_number(observation[1], 0, 2, -0.07, 0.07)
    #print(observation, [scaled_position, scaled_velocity])
    config = [scaled_pos_vel] 
    # update system states for one discrete time step


pycxsimulator.GUI().start(func=[initialize, observe, update])
print("I AM NOT HERE")
pycxsimulator.GUI().runEvent()


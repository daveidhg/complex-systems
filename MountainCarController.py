import pycxsimulator
import gymnasium as gym
from pylab import *

def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

def initialize():
    global env, config # list global variables
    env = gym.make(id='MountainCar-v0', render_mode="human")
    state, _ = env.reset()
    position, velocity = state
    config = [[position, velocity, 1]] 
    
def observe():
    global config # list global variables
    cla() # to clear the visualization space
    imshow(config, vmin = 0, vmax = 2, cmap = cm.Spectral)
    # visualize system states

def update():
    global env, config
    controller_output = int(round(mean(config), 0))
    print(controller_output)
    observation, reward, terminated, truncated, info = env.step(controller_output)
    scaled_position = scale_number(observation[0], 0, 2, -1.2, 0.6,)
    scaled_velocity = scale_number(observation[1], 0, 2, -0.07, 0.07)
    #print(observation, [scaled_position, scaled_velocity])
    config = [[scaled_position, scaled_velocity, controller_output]] 
    # update system states for one discrete time step


pycxsimulator.GUI().start(func=[initialize, observe, update])


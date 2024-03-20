import pycxsimulator
import gymnasium as gym
from pylab import *
import random

def initialize():
    global env, config # list global variables
    env = gym.make(id='MountainCar-v0', render_mode="human")
    state, _ = env.reset()
    position, velocity = state
    config = [[position, velocity, 1]] # Change to the actual values we are supposed to use
    
def observe():
    global observation, config # list global variables
    cla() # to clear the visualization space
    imshow(config, vmin = 0, vmax = 1, cmap = cm.Spectral)
    # visualize system states

def update():
    global env, observation, config
    controller_output = random.randint(0, 2)
    observation, reward, terminated, truncated, info = env.step(controller_output)
    print(observation)
    config = [[observation[0], observation[1], controller_output]] # Change to the actual values we are supposed to use
    # update system states for one discrete time step

pycxsimulator.GUI().start(func=[initialize, observe, update])


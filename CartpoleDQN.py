import gymnasium as gym
import time

env = gym.make(id='MountainCar-v0', render_mode="human")
(state, _) = env.reset()
x, velocity = state
print(state)

# simulate the environment
episodeNumber = 200
timeSteps = 50
time_a = 0.01
time_b = 0.01
timeStepsList = []
for episodeIndex in range(episodeNumber):
    start = time.time()
    if episodeNumber - episodeIndex == 4:
        env = gym.make(id='MountainCar-v0', render_mode='human')
        time_a = 0.1
        time_b = 1
    else:
        print(episodeIndex)
    env.reset()
    env.render()
    for timeIndex in range(timeSteps):
        timeStepsList.append(timeIndex)
        random_action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(random_action)
        if episodeNumber - episodeIndex <= 4:
            print(f"------------------------------------------------------\n"
                  f"Observations: {observation}, \nReward: {reward}, \nTerminated: {terminated}, \n"
                  f"Truncated: {truncated}, \nInfo: {info}, \nEpisode: {episodeIndex}, \n"
                  f"Step: {timeIndex}, \nMax Step: {max(timeStepsList)}, \nRandom_action: {random_action}\n"
                  f"------------------------------------------------------\n")
            time.sleep(time_a)
        if terminated:
            time.sleep(time_b)
            break
    stop = time.time()

env.close()


import pycxsimulator
from pylab import *

# import necessary modules
# define model parameters

def initialize():
    global env, config # list global variables
    env = gym.make(id='MountainCar-v0', render_mode="human")
    (state, _) = env.reset()
    position, velocity = state
    config = zeros([1, 100]) # Change to the actual values we are supposed to use
    
def observe():
    global observation, config # list global variables
    cla() # to clear the visualization space
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    # visualize system states

def update():
    global env, action, observation, config
    controller_output = 0
    observation, reward, terminated, truncated, info = env.step(controller_output)
    config = append(config, zeros[1, 100]) # Change to the actual values we are supposed to use
    # update system states for one discrete time step

pycxsimulator.GUI().start(func=[initialize, observe, update])

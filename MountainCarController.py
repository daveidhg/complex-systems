import pycxsimulator
import gymnasium as gym
env = gym.make("MountainCar-v0", render_mode='human')
_, _ = env.reset()


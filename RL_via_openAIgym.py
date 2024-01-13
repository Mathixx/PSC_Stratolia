import gym
from gym import spaces
import numpy as np




class CustomEnvironment(gym.Env):


    def __init__(self):
        super(CustomEnvironment, self).__init__()

        # Define your observation space and action space
        self.observation_space = spaces.Discrete(4) #tableau 4D discret, temps, longitude, latitude, pression, 

        self.action_space = spaces.Discrete(3)  # Change this to suit your environment

        # Initialize your custom variables here

    def reset(self):
        # Reset the environment to its initial state
        # Return the initial observation
        pass

    def step(self, action):
        # Execute the given action in the environment
        # Return the next observation, reward, done flag, and additional information
        pass

    def render(self, mode='human'):
        # Optional: Visualize the environment
        pass

    def close(self):
        # Optional: Cleanup code
        pass

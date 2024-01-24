import gym
from gym import spaces
import numpy as np
import pandas as pd

class BalloonNavigationEnv(gym.Env):
    def __init__(self, goal_x, goal_y):
        #Définir des coordonnée que l'on souhaite atteindre
        self.g_x = goal_x
        self.g_y = goal_y

        #Charger les données de vents
        self.winds = self.get_init_winds()

        #Définir le format de l'espace d'observations
        low_obs = np.array([-50, -50, -20, 0] + [-10] * (8000))
        high_obs = np.array([50,50,20,100] + [10] * (8000))
        self.observation_space = spaces.Box(low=low_obs, high=high_obs, dtype=np.float32)

        #Définition de l'espace des actions : monter, rester à la même altitude, déscendre
        self.action_space = spaces.Discrete(3) 


    def reset(self):
        # Initialiser l'environnement : on se place à l'origine
        self.state = [0,0,0,0]
        initial_observation = np.concatenate([
            self.state,
            self.winds
        ])
        return initial_observation


    def get_init_winds(self):
        #Charger les données de vent
        file_path = 'simple_winds.csv'
        df = pd.read_csv(file_path)
        return df.values
    
    def get_winds(self, x,y,z,t):
        #Déterminer la valeur du vent à une coordonnée donnée
        w_x = x//10
        w_y = y //10
        w_z = z // 10
        w_t = t//10       
        return  self.winds[w_x,w_y,w_z,w_t]
    
    def rewards(self,x,y):
        #Les rewards sont calculés à partir de la distance au point que le souhaite atteindre
        return -(abs(x - self.g_x) + abs(y-self.g_y))

    def step(self, action):
        #Mise à jour de l'environnement après une action donnée
        t = self.state[4]+1
        winds = self.get_winds(x,y,z,t)

        z = self.state[2] + action - 1
        x = self.state[0] + winds[0]
        y = self.state[1] + winds[1]
     
        self.state = [x,y,z,t]

        observation = np.concatenate([
            self.state,
            self.get_init_windst(0)
        ])
        info = {}

        return observation, self.reward(x,y), (x==self.g_x and y==self.g_y), info

    def render(self, mode='human'):
        #Pas d'affichage graphique pour l'instant
        pass


import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam



def build_model(states, actions, layers):
    #Construction d'un modèle de réseau de neuronnes dense
    model = Sequential()
    model.add(Dense(layers[0][0], layers[0][1], input_shape=states))
    for l in layers[1:] :
        model.add(Dense(l[0], activation=l[1]))
    model.add(Dense(actions, activation='linear'))
    return model


#Entrainement du modèle

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, 
                  nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)
    return dqn

dqn = build_agent(model, actions)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])
dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)
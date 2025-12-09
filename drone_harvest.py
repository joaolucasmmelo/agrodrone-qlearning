import numpy as np
import matplotlib.pyplot as plt
import random
import copy
import time
import os

# configs do ambiente
GRID_SIZE = 5
NUM_EPISODES = 3000
MAX_STEPS = 25
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EXPLORATION_RATE = 1.0
EXPLORATION_DECAY = 0.997
MIN_EXPLORATION = 0.01

ENERGY_COST = 0.1

# pontos
REWARDS = {
    'wheat': 1.5,
    'tomato': 2,
    'carrot': 3,
    'rock': -10,
    'empty': -1
}

# probabilidades
PROBS = [0.45, 0.35, 0.15, 0.05]
ITEMS = ['wheat', 'tomato', 'carrot', 'rock']

def render_farm(grid, drone_pos, step_num=0, score=0):
    icons = {
        'wheat': '🌾',
        'tomato': '🍅',
        'carrot': '🥕',
        'rock': '🪨',
        'empty': '🟫'
    }
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"--- PASSO {step_num} | PONTOS: {score:.1f} ---")
    print(f"Bateria: {MAX_STEPS - step_num}/{MAX_STEPS}")
    
    for x in range(GRID_SIZE):
        row_str = ""
        for y in range(GRID_SIZE):
            if (x, y) == drone_pos:
                row_str += "🚁 "
            else:
                item = grid[x, y]
                row_str += icons.get(item, '❓') + " "
        print(row_str)
    print("-------------------------------")
    time.sleep(0.5)

# ambiente
class HarvestEnv:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.state = (0, 0)
        # cria o mapa
        self.master_grid = np.random.choice(ITEMS, size=(self.grid_size, self.grid_size), p=PROBS)
        while self.master_grid[0,0] == 'rock':
             self.master_grid[0,0] = 'empty'
             
        self.grid = copy.deepcopy(self.master_grid)
        self.total_score = 0

    def reset(self):
        self.state = (0, 0)
        self.total_score = 0
        self.grid = copy.deepcopy(self.master_grid)
        return self.state

    def step(self, action):
        x, y = self.state

        if action == 0: x = max(0, x - 1)
        elif action == 1: x = min(self.grid_size - 1, x + 1)
        elif action == 2: y = max(0, y - 1)
        elif action == 3: y = min(self.grid_size - 1, y + 1)

        new_state = (x, y)
        
        # calculos
        item = self.grid[x, y]
        reward = REWARDS[item]
        
        reward -= ENERGY_COST
        
        # Logica de consumo:
        # Se for planta -> colhe e vira empty
        # Se for pedra -> quebra o drone (penalidade aplicada), vira empty ou fica la.
        # Vamos assumir que ele limpa o terreno (consome) mesmo sendo ruim, ou apenas passa.
        if item != 'empty':
            self.grid[x, y] = 'empty'
        
        self.state = new_state
        return new_state, reward

# agente
class QLearningAgent:
    def __init__(self, actions):
        self.actions = actions
        self.q_table = np.zeros((GRID_SIZE, GRID_SIZE, len(actions)))

    def choose_action(self, state, epsilon):
        if random.uniform(0, 1) < epsilon:
            return random.choice(self.actions)
        else:
            x, y = state
            return np.argmax(self.q_table[x, y])

    def learn(self, state, action, reward, next_state):
        x, y = state
        nx, ny = next_state
        old_value = self.q_table[x, y, action]
        next_max = np.max(self.q_table[nx, ny])
        
        new_value = old_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * next_max - old_value)
        self.q_table[x, y, action] = new_value

# fase treino
env = HarvestEnv()
agent = QLearningAgent(actions=[0, 1, 2, 3])
rewards_per_episode = []
epsilon = EXPLORATION_RATE

print("Iniciando treinamento com obstáculos...")

for episode in range(NUM_EPISODES):
    state = env.reset()
    
    sx, sy = state
    if env.grid[sx, sy] != 'empty': env.grid[sx, sy] = 'empty'

    total_reward = 0
    
    for _ in range(MAX_STEPS):
        action = agent.choose_action(state, epsilon)
        next_state, reward = env.step(action)
        agent.learn(state, action, reward, next_state)
        state = next_state
        total_reward += reward
        
    rewards_per_episode.append(total_reward)
    
    if epsilon > MIN_EXPLORATION:
        epsilon *= EXPLORATION_DECAY

print("Treinamento Concluído!")

# demo visual
print("\nPreparando demonstração do drone treinado...")
time.sleep(2)

curr_state = env.reset()
total = 0

sx, sy = curr_state
if env.grid[sx, sy] != 'empty': env.grid[sx, sy] = 'empty'

render_farm(env.grid, curr_state, step_num=0, score=total)

for step in range(1, MAX_STEPS + 1):
    x, y = curr_state
    action = np.argmax(agent.q_table[x, y])
    
    next_s, reward = env.step(action)
    total += reward
    curr_state = next_s
    
    render_farm(env.grid, curr_state, step_num=step, score=total)

print(f"\nViagem finalizada! Pontuação Final: {total:.2f}")
print("Feche o gráfico para encerrar o programa")

# grafico final
plt.figure(figsize=(10, 5))
plt.plot(rewards_per_episode)
plt.title('Aprendizado do Drone (Evitando Pedras)')
plt.xlabel('Episódios')
plt.ylabel('Pontuação Acumulada')
plt.grid(True)
plt.show()
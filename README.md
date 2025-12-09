# 🚁 AgroDrone AI: Q-Learning Harvest

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Finished-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

Este projeto é uma implementação prática de **Aprendizado por Reforço (Reinforcement Learning)** utilizando o algoritmo **Q-Learning**. O objetivo é treinar um drone autônomo para navegar em uma fazenda (grid 5x5), maximizando a colheita de vegetais valiosos e aprendendo a evitar obstáculos (pedras) e desperdício de bateria.

## 🧠 Como Funciona

O agente (drone) não conhece as regras do jogo inicialmente. Ele aprende através de milhares de episódios de tentativa e erro, preenchendo uma **Q-Table** que mapeia a melhor ação possível para cada posição do mapa.

O ambiente é gerado proceduralmente com as seguintes probabilidades:
- **Trigo (45%)**
- **Tomate (35%)**
- **Cenoura (15%)**
- **Pedra (5%)**

## 🏆 Sistema de Recompensas

Para que a IA aprenda o comportamento desejado, o sistema de pontuação foi calibrado da seguinte forma:

| Item | Emoji | Recompensa (Pontos) | Descrição |
| :--- | :---: | :---: | :--- |
| **Cenoura** | 🥕 | **+3.0** | Alta prioridade de colheita. |
| **Tomate** | 🍅 | **+2.0** | Média prioridade. |
| **Trigo** | 🌾 | **+1.5** | Baixa prioridade, mas útil. |
| **Vazio** | 🟫 | **-1.0** | Penalidade por andar sem colher. |
| **Pedra** | 🪨 | **-10.0** | Obstáculo perigoso (deve ser evitado). |
| **Energia** | 🔋 | **-0.1** | Custo de movimento por passo. |

> **Nota:** A alta penalidade da pedra (-10) ensina o drone a contornar obstáculos, mesmo que o caminho seja mais longo.

## 🛠️ Tecnologias Utilizadas

* **Python** (Linguagem base)
* **NumPy** (Cálculos matemáticos e manipulação da Q-Table)
* **Matplotlib** (Plotagem do gráfico de aprendizado ao final)
* **OS/Time** (Visualização e animação no terminal)

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/agrodrone-qlearning.git](https://github.com/seu-usuario/agrodrone-qlearning.git)
   cd agrodrone-qlearning

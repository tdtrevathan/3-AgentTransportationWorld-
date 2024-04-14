# Multi-Agent Simulation Project

## Description
This project is a Python-based simulation of a multi-agent environment where agents interact within a world to perform tasks involving pickup and delivery. The simulation incorporates reinforcement learning algorithms (Q-learning and SARSA) to enable agents to learn and optimize their paths and strategies over time. This project is designed to explore the dynamics of learning in multi-agent systems and demonstrate the effectiveness of different exploration strategies.

## Components
- **Experiment.py**: Defines the `Experiment` class that sets up and runs the experiments using various configurations.
- **groupProject.py**: Acts as the main entry point for setting up the world, agents, and running experiments.
- **LearningAlgorithm.py**: Implements Q-learning and SARSA algorithms to provide learning capabilities to agents.
- **my_enums.py**: Contains enumerations used throughout the project to maintain consistent references to agent types, actions, and algorithms.
- **PdWorld.py**: Establishes the simulation environment where agents operate.
- **Visualizer.py**: Provides functionality for visualizing the agents' paths and behaviors within the simulation.

## Setup
Our main file is named `groupProject.py` -- to run the program, please go to `groupProject.py`. The `groupProject.py` file is the controller script for this project. This file calls the functions created from the classes contained in other files -- which allows the setup of the environment, execution (exploring), policies, constraints, and visualization methods. The `groupProject.py` file presents a more readable representation of each of our experiments and what parameters changes throughout each experiment. Scroll down to the bottom `groupProject.py` there you will see a selection of data visualization options from the `Visualizer` class. The program has both shared and separate Q-tables available to visualize. To prevent visualizing data you don't need, you can comment out the parts you don't need, since it will take a  considerable amount time to visualize everything.
import numpy as np
import pandas as pd
import main as m

class QLearningTable:
    def __init__(self, actions, learning_rate=0.9, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.q_table_final = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def choose_action(self, observation):
        self.check_state_exist(observation)

        if np.random.uniform() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        else:
            action = np.random.choice(self.actions)
        return action

    ### Если он сталкнется с границей или будет в клетке пожара
    ### Признак клетки fire 1 0
    def learn(self, state, action, reward, next_state, fire):
        self.check_state_exist(next_state)
        q_predict = self.q_table.loc[state, action]

        if next_state != 0 and fire != 1:
            q_target = reward + self.gamma * self.q_table.loc[next_state, :].max()
        else:
            q_target = reward

        self.q_table.loc[state, action] += self.lr * (q_target - q_predict)

        return self.q_table.loc[state, action]

    def update(self, observation, fireman):
        steps = []
        all_costs = []

        for episode in range(1000):
            m.QGameOfLife.reset(fireman)
            i = 0
            cost = 0

            while True:
                observation = m.QGameOfLife.render()
                action = self.choose_action(str(observation))
                observation_, reward, done = m.QGameOfLife.move_fireman(action)
                cost += self.learn(str(observation), action, reward, str(observation_))
                observation = observation_
                i += 1

                if done:
                    steps += [i]
                    all_costs += [cost]
                    break
        m.QGameOfLife.final(fireman)
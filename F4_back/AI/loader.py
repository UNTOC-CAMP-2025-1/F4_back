import numpy as np
import os
from .dqn_model import DQN

# npz 파일에서 가중치 불러오기
base_dir = os.path.dirname(__file__)
weights_path = os.path.join(base_dir, "dqn_weights.npz")
weights = np.load(weights_path)
# 각 레이어의 가중치와 편향
w1, b1 = weights["w1"], weights["b1"]
w2, b2 = weights["w2"], weights["b2"]
w3, b3 = weights["w3"], weights["b3"]

# ReLU 함수 정의
def relu(x):
    return np.maximum(0, x)

def predict_direction(state_x, state_y, player_x, player_y, boost):
    weights = np.load("AI/weights/dqn_weights.npz")

    W = weights["W"]  # shape: (8, 5) → 8 actions, 5 input dims

    state_vec = np.array([state_x, state_y, player_x, player_y, boost])  # shape: (5,)
    q_values = np.dot(W, state_vec)  # shape: (8,)
    return int(np.argmax(q_values))
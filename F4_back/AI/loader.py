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

    # 간단한 추론 (예시) — 가장 높은 가중치 index 반환
    # 실제로는 Colab에서 이 추론을 실행해야 함 (혹은 numpy만 쓰는 로직이면 OK)
    q_values = (
        weights["w1"] * state_x +
        weights["w2"] * state_y +
        weights["w3"] * player_x +
        weights["w4"] * player_y +
        weights["w5"] * boost
    )  # shape: (action_dim,)
    return int(np.argmax(q_values))
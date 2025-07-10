import numpy as np
import os, torch
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

# 추론 함수
def predict_direction(state_x, state_y, player_x, player_y):
    x = np.array([[state_x, state_y, player_x, player_y]])  # shape: (1, 4)

    x = relu(np.dot(x, w1) + b1)
    x = relu(np.dot(x, w2) + b2)
    x = np.dot(x, w3) + b3

    return int(np.argmax(x))  # 가장 높은 Q값의 인덱스를 행동으로 반환

def predict_direction(state):
    weights = np.load("AI/weights/dqn_weights.npz")
    model = DQN()
    model.load_state_dict({k: torch.tensor(v) for k, v in weights.items()})
    model.eval()

    state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        q_values = model(state)
        action = q_values.argmax().item()
    return action
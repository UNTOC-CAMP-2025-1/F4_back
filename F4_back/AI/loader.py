import numpy as np

# npz 파일에서 가중치 불러오기
weights = np.load("~/untocF4/F4_back/F4_back/AI/dqn_weights.npz")

# 각 레이어의 가중치와 편향
W1, b1 = weights['W1'], weights['b1']
W2, b2 = weights['W2'], weights['b2']
W3, b3 = weights['W3'], weights['b3']

# ReLU 함수 정의
def relu(x):
    return np.maximum(0, x)

# 추론 함수
def predict_direction(state_x, state_y, player_x, player_y):
    x = np.array([[state_x, state_y, player_x, player_y]])  # shape: (1, 4)

    x = relu(np.dot(x, W1) + b1)
    x = relu(np.dot(x, W2) + b2)
    x = np.dot(x, W3) + b3

    return int(np.argmax(x))  # 가장 높은 Q값의 인덱스를 행동으로 반환
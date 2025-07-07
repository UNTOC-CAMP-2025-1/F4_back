import torch

class DummyModel:
    def __init__(self):
        pass

    def __call__(self, x):
        # 아무거나 예측하게 함 (ex: 항상 0번 방향)
        return torch.tensor([[1.0, 0.0, 0.0, 0.0]])

model = DummyModel()

def predict_direction(state_x, state_y, player_x, player_y):
    # 더미 추론 함수
    return 0  # 항상 0번 방향으로 행동
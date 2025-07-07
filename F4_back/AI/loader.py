try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    print("[경고] torch가 설치되어 있지 않아 모델을 로드할 수 없습니다.")
    TORCH_AVAILABLE = False

from dqn_model import DQN

if TORCH_AVAILABLE:
    model = DQN(input_dim=4, output_dim=4)  # 입력/출력 차원은 실제 상황에 맞게 조정
    model.load_state_dict(torch.load("tiniworm_dqn_model.pt", map_location=torch.device("cpu")))
    model.eval()
else:
    model = None

def predict_direction(state):
    if not TORCH_AVAILABLE or model is None:
        print("[오류] torch 미설치 상태이거나 모델이 로드되지 않았습니다.")
        return -1  # 또는 기본 행동 리턴

    with torch.no_grad():
        state_tensor = torch.tensor(state, dtype=torch.float32)
        q_values = model(state_tensor)
        return int(torch.argmax(q_values).item())
try:
    import torch
    TORCH_AVAILABLE = True
except Exception as e:
    print(f"[경고] torch import 실패: {e}")
    torch = None
    TORCH_AVAILABLE = False

from dqn_model import DQN

if TORCH_AVAILABLE:
    try:
        model = DQN(input_dim=4, output_dim=4)  # 입력/출력 차원은 실제 환경에 맞게 수정
        model.load_state_dict(torch.load("tiniworm_dqn_model.pt", map_location=torch.device("cpu")))
        model.eval()
    except Exception as e:
        print(f"[경고] torch 모델 로드 실패: {e}")
        model = None
else:
    model = None

def predict_direction(state):
    if not TORCH_AVAILABLE or model is None:
        print("[오류] torch 미설치 상태이거나 모델이 로드되지 않았습니다.")
        return -1  # 기본 행동 리턴

    try:
        with torch.no_grad():
            state_tensor = torch.tensor(state, dtype=torch.float32)
            q_values = model(state_tensor)
            return int(torch.argmax(q_values).item())
    except Exception as e:
        print(f"[오류] 추론 중 문제 발생: {e}")
        return -1
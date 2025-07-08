from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import torch
import torch.nn as nn

router = APIRouter()

class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 8)
        )

    def forward(self, x):
        return self.net(x)

model = DQN()
model.load_state_dict(torch.load("dqn_model.pth", map_location=torch.device("cpu")))
model.eval()

class BotState(BaseModel):
    state_x: float
    state_y: float
    player_x: float
    player_y: float

@router.post("/bot_decide")
def decide_action(data: BotState):
    try:
        input_tensor = torch.tensor([[data.state_x, data.state_y, data.player_x, data.player_y]], dtype=torch.float32)
        with torch.no_grad():
            output = model(input_tensor)
            action = torch.argmax(output, dim=1).item()
        return {"action": action}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
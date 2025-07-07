from AI.loader import predict_direction
from AI_bot.AI_bot_schema import StateInput

def decide_ai_action(state: StateInput) -> int:
    return predict_direction(
        state.state_x, state.state_y,
        state.player_x, state.player_y
    )
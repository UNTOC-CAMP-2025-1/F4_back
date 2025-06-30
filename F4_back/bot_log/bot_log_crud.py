import math
import random
from bot_log.bot_log_schema import BotFullState, Position


def angle_to_direction(angle: float) -> int:
    return int((angle % (2 * math.pi)) / (math.pi / 4))


def decide_greedy(state: BotFullState) -> int:
    min_dist = float('inf')
    target = None
    for jewel in state.jewels:
        dx = jewel.x - state.bot_head.x
        dy = jewel.y - state.bot_head.y
        dist = math.hypot(dx, dy)
        if dist < min_dist:
            min_dist = dist
            target = jewel

    if target:
        angle = math.atan2(target.y - state.bot_head.y, target.x - state.bot_head.x)
        return angle_to_direction(angle)
    else:
        return random.randint(0, 7)


def decide_evasive(state: BotFullState) -> int:
    danger_threshold = 3.0

    def is_near_body(pos: Position):
        for enemy in state.enemies:
            for part in enemy.body:
                if math.hypot(pos.x - part.x, pos.y - part.y) < danger_threshold:
                    return True
        return False

    safe_directions = []
    for dir_idx in range(8):
        angle = dir_idx * (math.pi / 4)
        new_x = state.bot_head.x + math.cos(angle)
        new_y = state.bot_head.y + math.sin(angle)
        if not is_near_body(Position(x=new_x, y=new_y)):
            safe_directions.append(dir_idx)

    if safe_directions:
        return random.choice(safe_directions)
    else:
        return random.randint(0, 7)


def decide_aggressive_boost(state: BotFullState) -> dict:
    min_dist = float('inf')
    target = None
    for enemy in state.enemies:
        dx = enemy.head.x - state.bot_head.x
        dy = enemy.head.y - state.bot_head.y
        dist = math.hypot(dx, dy)
        if dist < min_dist:
            min_dist = dist
            target = enemy.head

    if target:
        angle = math.atan2(target.y - state.bot_head.y, target.x - state.bot_head.x)
        direction = angle_to_direction(angle)

        should_boost = (
            min_dist < 5.0 and
            state.bot_length > 5 and
            state.can_boost is True
        )

        return {
            "action": direction,
            "boost": should_boost
        }

    return {
        "action": random.randint(0, 7),
        "boost": False
    }


def decide_random(state: BotFullState) -> int:
    return random.randint(0, 7)


STRATEGY_MAP = {
    1: decide_greedy,
    2: decide_evasive,
    3: decide_random,
    4: decide_aggressive_boost
}


def decide_action_from_strategy(state: BotFullState):
    strategy_fn = STRATEGY_MAP.get(state.strategy_id, decide_random)
    return strategy_fn(state)

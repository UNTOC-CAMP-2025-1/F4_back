from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from functools import partial
from leader_board.leader_board_crud import get_top_users_from_game_sessions
from leader_board.leader_board_schema import LeaderBoardEntry

router = APIRouter()

get_leaderboard_db = partial(get_db, domain="leader_board")

@router.get("/top", response_model=list[LeaderBoardEntry])
def read_top_users():
    top_users = get_top_users_from_game_sessions()
    return [
        {
            "rank": i + 1,
            "user_name": row.user_name,
            "user_score": row.max_score
        } for i, row in enumerate(top_users)
    ]
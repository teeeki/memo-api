from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.crud.memo import MemoCRUD
from app.config.database import get_db
from pydantic import BaseModel

# memoのレスポンスモデル
class MemoResponse(BaseModel):
    username: str
    title: str
    summary: str
    content: str

router = APIRouter()

@router.post("/create-memo")
async def create_memo():
    pass


@router.get("/get-memos", response_model=List[MemoResponse], tags=["memo"])
async def get_memos_endpoint(
    user_id: List[int] = Query(None),
    session: Session = Depends(get_db),
    # current_username: str = Depends(get_current_username),
):
    # 認証済みであることを保証するための依存性。現状はフィルターしないが今後拡張可能。
    # _ = current_username
    result = MemoCRUD.get_memos_by_user_ids(session, user_id=user_id)
    return [MemoResponse(**memo) for memo in result]


# backend/app/api/__init__.py
from fastapi import APIRouter

from app.api import auth

# API 라우터 통합
api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)

# 태스크 등 추가 라우터 (로드 실패해도 auth는 문서에 반영됨)
try:
    from app.api import task
    api_router.include_router(task.router)
except Exception:
    pass
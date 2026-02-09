# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# 앱을 먼저 생성 (api_router 로드 실패해도 서버는 기동)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
    }


@app.get("/health")
def health_check():
    """서버 상태 확인 (나중에 DB, Redis 연결도 체크)"""
    return {"status": "healthy"}


# API 라우터는 나중에 로드 (schemas/services 등 미구현 시에도 서버는 동작)
try:
    from app.api import api_router
    app.include_router(api_router)
except Exception as e:
    import logging
    logging.getLogger(__name__).warning("API router not loaded: %s", e)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

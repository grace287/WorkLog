# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base는 맨 위에 정의 (alembic 등에서 settings 없이 import 가능)
Base = declarative_base()

_engine = None
_SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        from app.core.config import settings
        _engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            echo=settings.DEBUG,
        )
    return _engine


def _get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_get_engine(),
        )
    return _SessionLocal


def __getattr__(name: str):
    """하위 호환: engine / SessionLocal 접근 시 지연 생성"""
    if name == "engine":
        return _get_engine()
    if name == "SessionLocal":
        return _get_session_factory()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def get_db():
    """
    FastAPI dependency로 사용
    각 요청마다 새로운 DB 세션 제공
    """
    db = _get_session_factory()()
    try:
        yield db
    finally:
        db.close()
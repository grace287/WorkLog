# backend/alembic/env.py
from logging.config import fileConfig
from pathlib import Path
import os
import sys
import types

from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.ext.declarative import declarative_base
from alembic import context

# .env에서 DATABASE_URL만 로드
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass
DATABASE_URL = os.environ["DATABASE_URL"]

# Base를 env에서 직접 정의하고, app.core.database를 이 Base로 채움
# → app.core.config/settings 로드 실패와 무관하게 동작
Base = declarative_base()
_backend = Path(__file__).resolve().parents[1]
if _backend not in sys.path:
    sys.path.insert(0, str(_backend))

for _pkg in ("app", "app.core", "app.models"):
    if _pkg not in sys.modules:
        sys.modules[_pkg] = types.ModuleType(_pkg)
_db_mod = types.ModuleType("app.core.database")
_db_mod.Base = Base
sys.modules["app.core.database"] = _db_mod

# 모델 파일만 직접 로드 → Base.metadata에 테이블 등록 (패키지 __init__ 미사용)
_models_dir = _backend / "app" / "models"
import importlib.util
for _name in ("users", "task", "daily_note", "project"):
    _path = _models_dir / f"{_name}.py"
    if _path.exists():
        _spec = importlib.util.spec_from_file_location(f"app.models.{_name}", _path)
        _mod = importlib.util.module_from_spec(_spec)
        sys.modules[_spec.name] = _mod
        _spec.loader.exec_module(_mod)

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode: .env의 DATABASE_URL로 직접 연결."""
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
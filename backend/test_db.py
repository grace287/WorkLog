# backend/test_db.py
"""DB 연결 및 모델 테스트"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import SessionLocal
from app.models import Base, User
from app.core.security import get_password_hash


def test_connection():
    """DB 연결 테스트"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ DB 연결 성공!")
        db.close()
    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")


def create_test_user():
    """테스트 유저 생성"""
    db = SessionLocal()
    
    try:
        # 이미 존재하는지 확인
        existing = db.query(User).filter(User.email == "test@worklog.com").first()
        if existing:
            print("ℹ️  테스트 유저 이미 존재")
            return
        
        # 새 유저 생성
        user = User(
            email="test@worklog.com",
            username="testuser",
            full_name="Test User",
            hashed_password=get_password_hash("test1234"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"✅ 테스트 유저 생성 성공!")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        
    except Exception as e:
        print(f"❌ 유저 생성 실패: {e}")
        db.rollback()
    finally:
        db.close()


def list_users():
    """모든 유저 조회"""
    db = SessionLocal()
    users = db.query(User).all()
    
    print(f"\n📋 전체 유저 수: {len(users)}")
    for user in users:
        print(f"  - {user.username} ({user.email})")
    
    db.close()


if __name__ == "__main__":
    try:
        print("🔍 WorkLog DB 테스트\n")
        test_connection()
        create_test_user()
        list_users()
    except Exception as e:
        print(f"❌ 실행 중 오류: {e}")
        raise
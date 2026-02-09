# backend/test_auth.py
"""
인증 API 테스트 (서버 실행 중일 때 사용)

사용법:
  1. 터미널 1: uvicorn main:app --reload --host 0.0.0.0 --port 8080
  2. 터미널 2: python test_auth.py
"""
import sys

try:
    import httpx
except ImportError:
    print("httpx가 필요합니다: pip install httpx")
    sys.exit(1)

BASE_URL = "http://localhost:8080"


def test_signup():
    """회원가입 테스트"""
    print("\n📌 POST /api/auth/signup")
    r = httpx.post(
        f"{BASE_URL}/api/auth/signup",
        json={
            "email": "test@worklog.com",
            "username": "testuser",
            "password": "test1234",
            "full_name": "Test User",
        },
        timeout=10.0,
    )
    print(f"   상태: {r.status_code}")
    if r.status_code in (200, 201):
        print(f"   응답: {r.json()}")
        return True
    print(f"   응답: {r.text}")
    return False


def test_login():
    """로그인 테스트 (OAuth2 form)"""
    print("\n📌 POST /api/auth/login")
    r = httpx.post(
        f"{BASE_URL}/api/auth/login",
        data={
            "username": "test@worklog.com",  # OAuth2 스펙상 username 필드에 이메일
            "password": "test1234",
        },
        timeout=10.0,
    )
    print(f"   상태: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   token_type: {data.get('token_type')}")
        print(f"   access_token: {data.get('access_token', '')[:20]}...")
        return data.get("access_token")
    print(f"   응답: {r.text}")
    return None


def test_me(token: str):
    """내 정보 조회 (Bearer 토큰)"""
    print("\n📌 GET /api/auth/me")
    r = httpx.get(
        f"{BASE_URL}/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    print(f"   상태: {r.status_code}")
    if r.status_code == 200:
        print(f"   응답: {r.json()}")
        return True
    print(f"   응답: {r.text}")
    return False


if __name__ == "__main__":
    print("🔍 WorkLog 인증 API 테스트")
    print(f"   BASE_URL = {BASE_URL}")

    try:
        # 서버 살아있는지 확인
        r = httpx.get(f"{BASE_URL}/health", timeout=2.0)
        if r.status_code != 200:
            print("⚠️ 서버가 응답하지 않습니다. 먼저 실행하세요:")
            print("   uvicorn main:app --reload --host 0.0.0.0 --port 8080")
            sys.exit(1)
    except httpx.ConnectError:
        print("⚠️ 서버에 연결할 수 없습니다. 먼저 실행하세요:")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8080")
        sys.exit(1)

    test_signup()
    token = test_login()
    if token:
        test_me(token)

    print("\n✅ 테스트 완료")

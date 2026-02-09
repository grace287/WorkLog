# backend/test_tasks.py
"""
태스크 API 테스트 (서버 실행 중일 때 사용)

사용법:
  1. 터미널 1: uvicorn main:app --reload --host 0.0.0.0 --port 8080
  2. 터미널 2: python test_tasks.py
"""
import sys

try:
    import httpx
except ImportError:
    print("httpx가 필요합니다: pip install httpx")
    sys.exit(1)

BASE_URL = "http://localhost:8080"


def get_token():
    """로그인해서 토큰 획득"""
    r = httpx.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": "test@worklog.com", "password": "test1234"},
        timeout=10.0,
    )
    if r.status_code != 200:
        print("⚠️ 로그인 실패. 먼저 test_auth.py로 회원가입 후 실행하세요.")
        return None
    return r.json().get("access_token")


def test_create_task(token: str):
    """태스크 생성"""
    print("\n📌 POST /api/tasks")
    r = httpx.post(
        f"{BASE_URL}/api/tasks",
        json={
            "title": "테스트 태스크",
            "description": "test_tasks.py에서 생성",
            "status": "todo",
            "priority": "medium",
        },
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    print(f"   상태: {r.status_code}")
    if r.status_code in (200, 201):
        data = r.json()
        print(f"   응답: id={data.get('id')}, title={data.get('title')}")
        return data.get("id")
    print(f"   응답: {r.text}")
    return None


def test_list_tasks(token: str):
    """태스크 목록 조회"""
    print("\n📌 GET /api/tasks")
    r = httpx.get(
        f"{BASE_URL}/api/tasks",
        params={"skip": 0, "limit": 10},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    print(f"   상태: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        items = data.get("items", [])
        total = data.get("total", 0)
        print(f"   total={total}, items={len(items)}개")
        for t in items[:3]:
            print(f"     - {t.get('title')} [{t.get('status')}]")
        return True
    print(f"   응답: {r.text}")
    return False


def test_get_task(token: str, task_id: str):
    """태스크 단건 조회"""
    print(f"\n📌 GET /api/tasks/{{id}}")
    r = httpx.get(
        f"{BASE_URL}/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    print(f"   상태: {r.status_code}")
    if r.status_code == 200:
        print(f"   응답: {r.json()}")
        return True
    print(f"   응답: {r.text}")
    return False


def test_update_task(token: str, task_id: str):
    """태스크 수정"""
    print(f"\n📌 PATCH /api/tasks/{{id}}")
    r = httpx.patch(
        f"{BASE_URL}/api/tasks/{task_id}",
        json={"title": "수정된 제목", "status": "doing"},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    print(f"   상태: {r.status_code}")
    if r.status_code == 200:
        print(f"   응답: {r.json()}")
        return True
    print(f"   응답: {r.text}")
    return False


def test_delete_task(token: str, task_id: str):
    """태스크 삭제"""
    print(f"\n📌 DELETE /api/tasks/{{id}}")
    r = httpx.delete(
        f"{BASE_URL}/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    print(f"   상태: {r.status_code}")
    if r.status_code in (200, 204):
        print("   삭제 완료")
        return True
    print(f"   응답: {r.text}")
    return False


if __name__ == "__main__":
    print("🔍 WorkLog 태스크 API 테스트")
    print(f"   BASE_URL = {BASE_URL}")

    try:
        r = httpx.get(f"{BASE_URL}/health", timeout=2.0)
        if r.status_code != 200:
            print("⚠️ 서버가 응답하지 않습니다. uvicorn main:app --reload --host 0.0.0.0 --port 8080")
            sys.exit(1)
    except httpx.ConnectError:
        print("⚠️ 서버에 연결할 수 없습니다. uvicorn main:app --reload --host 0.0.0.0 --port 8080")
        sys.exit(1)

    token = get_token()
    if not token:
        sys.exit(1)

    task_id = test_create_task(token)
    test_list_tasks(token)
    if task_id:
        test_get_task(token, task_id)
        test_update_task(token, task_id)
        test_delete_task(token, task_id)

    print("\n✅ 테스트 완료")

# backend/app/api/tasks.py
"""
Task 관련 API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from app.core.database import get_db
from app.api.deps import CurrentUser
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.common import PaginatedResponse, PaginationParams, MessageResponse
from app.services.task_service import TaskService
from app.models.task import TaskStatus, TaskPriority

router = APIRouter(prefix="/tasks", tags=["태스크"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="태스크 생성"
)
def create_task(
    task_in: TaskCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    새로운 태스크를 생성합니다.
    
    - **title**: 태스크 제목 (필수)
    - **description**: 상세 설명 (선택)
    - **status**: 상태 (기본값: todo)
    - **priority**: 우선순위 (기본값: medium)
    - **due_date**: 마감일 (선택)
    """
    task = TaskService.create(db, task_in, current_user.id)
    return task


@router.get(
    "",
    response_model=PaginatedResponse[TaskResponse],
    summary="태스크 목록 조회"
)
def get_tasks(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(20, ge=1, le=100, description="가져올 최대 개수"),
    status: Optional[TaskStatus] = Query(None, description="상태 필터"),
    priority: Optional[TaskPriority] = Query(None, description="우선순위 필터"),
    search: Optional[str] = Query(None, description="검색어 (제목/설명)")
):
    """
    태스크 목록을 조회합니다.
    
    **필터링:**
    - status: todo, doing, done 중 하나
    - priority: high, medium, low 중 하나
    - search: 제목이나 설명에서 검색
    
    **정렬:**
    - 완료되지 않은 태스크가 먼저
    - 같은 상태 내에서는 order 순서대로
    
    **페이지네이션:**
    - skip: 건너뛸 개수 (0부터 시작)
    - limit: 가져올 최대 개수 (기본 20, 최대 100)
    
    **예시:**
    - `/api/tasks?skip=0&limit=20` - 첫 페이지
    - `/api/tasks?skip=20&limit=20` - 두 번째 페이지
    - `/api/tasks?status=todo&priority=high` - 미완료 + 높은 우선순위
    - `/api/tasks?search=회의` - "회의"가 포함된 태스크
    """
    # 태스크 목록
    tasks = TaskService.get_multi(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        search=search
    )
    
    # 전체 개수 (필터 적용된)
    total = TaskService.get_count(
        db=db,
        user_id=current_user.id,
        status=status
    )
    
    return PaginatedResponse.create(
        items=tasks,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get(
    "/today",
    response_model=List[TaskResponse],
    summary="오늘 할 일 조회"
)
def get_today_tasks(
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    오늘 할 일을 조회합니다.
    
    **조건:**
    - 완료되지 않은 태스크
    - 마감일이 오늘이거나 과거
    - 또는 마감일이 없는 태스크 (백로그)
    
    **정렬:**
    - 높은 우선순위 먼저
    - 같은 우선순위 내에서는 order 순서대로
    """
    tasks = TaskService.get_today_tasks(db, current_user.id)
    return tasks


@router.get(
    "/stats",
    summary="태스크 통계"
)
def get_task_stats(
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    태스크 통계를 조회합니다.

    **포함 정보:**
    - 전체 태스크 개수
    - 상태별 개수
    - 우선순위별 개수
    - 오늘 할 일 개수
    """
    total = TaskService.get_count(db, current_user.id)
    todo = TaskService.get_count(db, current_user.id, TaskStatus.TODO)
    doing = TaskService.get_count(db, current_user.id, TaskStatus.DOING)
    done = TaskService.get_count(db, current_user.id, TaskStatus.DONE)

    today_tasks = TaskService.get_today_tasks(db, current_user.id)

    return {
        "total": total,
        "by_status": {
            "todo": todo,
            "doing": doing,
            "done": done
        },
        "today_count": len(today_tasks),
        "completion_rate": round((done / total * 100) if total > 0 else 0, 1)
    }


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="태스크 상세 조회"
)
def get_task(
    task_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    특정 태스크의 상세 정보를 조회합니다.
    
    **권한:**
    - 본인이 생성한 태스크만 조회 가능
    """
    task = TaskService.get_by_id(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="태스크를 찾을 수 없습니다"
        )
    
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="태스크 수정"
)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    태스크를 수정합니다.
    
    **수정 가능한 필드:**
    - title: 제목
    - description: 설명
    - status: 상태
    - priority: 우선순위
    - due_date: 마감일
    - order: 정렬 순서
    
    **Note:**
    - 보내지 않은 필드는 변경되지 않습니다 (Partial Update)
    - null을 보내면 해당 필드를 null로 설정합니다
    """
    # 태스크 조회
    task = TaskService.get_by_id(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="태스크를 찾을 수 없습니다"
        )
    
    # 수정
    updated_task = TaskService.update(db, task, task_update)
    
    return updated_task


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    summary="태스�� 상태 변경"
)
def update_task_status(
    task_id: UUID,
    status: TaskStatus,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    태스크의 상태만 변경합니다.
    
    **상태:**
    - todo: 할 일
    - doing: 진행 중
    - done: 완료
    
    **예시:**
    ```
    PATCH /api/tasks/{task_id}/status?status=done
    ```
    """
    # 태스크 조회
    task = TaskService.get_by_id(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="태스크를 찾을 수 없습니다"
        )
    
    # 상태 변경
    task_update = TaskUpdate(status=status)
    updated_task = TaskService.update(db, task, task_update)
    
    # 완료 처리 시 completed_at 업데이트
    if status == TaskStatus.DONE:
        TaskService.complete(db, updated_task)
    
    return updated_task


@router.post(
    "/{task_id}/complete",
    response_model=TaskResponse,
    summary="태스크 완료"
)
def complete_task(
    task_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    태스크를 완료 처리합니다.
    
    **동작:**
    - status → done
    - completed_at → 현재 시간
    
    **Note:**
    - 이미 완료된 태스크도 다시 완료 처리 가능 (멱등성)
    """
    # 태스크 조회
    task = TaskService.get_by_id(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="태스크를 찾을 수 없습니다"
        )
    
    # 완료 처리
    completed_task = TaskService.complete(db, task)
    
    return completed_task


@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
    summary="태스크 삭제"
)
def delete_task(
    task_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    태스크를 삭제합니다.
    
    **주의:**
    - 삭제된 태스크는 복구할 수 없습니다 (Hard Delete)
    - 나중에 Soft Delete로 변경 가능
    """
    # 태스크 조회
    task = TaskService.get_by_id(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="태스크를 찾을 수 없습니다"
        )
    
    # 삭제
    TaskService.delete(db, task)
    
    return MessageResponse(message="태스크가 삭제되었습니다")
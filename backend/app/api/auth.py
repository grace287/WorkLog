# backend/app/api/auth.py
"""
인증 관련 API
- 회원가입
- 로그인
- 내 정보 조회
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
)
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import UserService
from app.api.deps import get_current_user, CurrentUser

router = APIRouter(prefix="/auth", tags=["인증"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    회원가입
    
    새로운 유저를 생성합니다.
    
    - **email**: 이메일 (고유값)
    - **username**: 유저명 (고유값)
    - **password**: 비밀번호 (최소 8자)
    - **full_name**: 전체 이름 (선택)
    """
    # 1. 이메일 중복 체크
    existing_user = UserService.get_by_email(db, user_in.email)
    if existing_user:
        raise UserAlreadyExistsException("이미 사용 중인 이메일입니다")

    # 2. 유저명 중복 체크
    existing_username = UserService.get_by_username(db, user_in.username)
    if existing_username:
        raise UserAlreadyExistsException("이미 사용 중인 유저명입니다")
    
    # 3. 유저 생성
    try:
        user = UserService.create(db, user_in)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="회원가입에 실패했습니다"
        )


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    로그인
    
    이메일과 비밀번호로 로그인하고 JWT 토큰을 받습니다.
    
    **OAuth2PasswordRequestForm 필드:**
    - username: 이메일을 입력하세요 (OAuth2 스펙상 필드명이 username)
    - password: 비밀번호
    
    **응답:**
    - access_token: JWT 토큰
    - token_type: "bearer"
    
    **사용법:**
    ```
    1. 이 토큰을 Authorization 헤더에 포함
    2. Authorization: Bearer {access_token}
    3. 이후 모든 API 요청에 포함
    ```
    """
    # 1. 인증 (이메일 + 비밀번호 검증)
    user = UserService.authenticate(
        db,
        email=form_data.username,  # OAuth2 스펙상 username 필드 사용
        password=form_data.password
    )
    
    if not user:
        raise InvalidCredentialsException()
    
    # 2. JWT 토큰 생성
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires
    )
    
    # 3. 토큰 반환
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUser):
    """
    내 정보 조회
    
    현재 로그인한 유저의 정보를 반환합니다.
    
    **인증 필요:** Bearer 토큰
    """
    return current_user


@router.post("/test-token", response_model=UserResponse)
def test_token(current_user: CurrentUser):
    """
    토큰 테스트
    
    JWT 토큰이 유효한지 테스트합니다.
    """
    return current_user
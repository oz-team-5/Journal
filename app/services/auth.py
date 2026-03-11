from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.models.auth import TokenBlacklist
from app.models.user import User
from app.schemas.auth import Token

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto",
)


def verify_password(password: str, hashed_password: str) -> bool:
    """비밀번호 검증 db에 있는 비밀번호와 평문비밀번호 대조"""
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호 해쉬화"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """jwt 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + (
            expires_delta
            if expires_delta
            else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """jwt 디코드"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def is_blacklisted(token: str) -> bool:
    """블랙리스트 여부 확인"""
    return await TokenBlacklist.filter(token=token).exists()


async def blacklist_token(token: str, user: User) -> None:
    """토큰을 블랙리스트에 등록"""
    payload = decode_token(token)

    exp = payload.get("exp")
    if exp is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing exp",
        )

    expired_at = datetime.fromtimestamp(exp, tz=timezone.utc)

    exists = await TokenBlacklist.filter(token=token).exists()
    if exists:
        return

    await TokenBlacklist.create(
        token=token,
        user=user,
        expired_at=expired_at,
    )


def create_access_token_for_subject(
    subject: str, expires_delta: Optional[timedelta] = None
) -> str:
    """생성시 token을 발급시켜줌"""
    return create_access_token({"sub": subject}, expires_delta=expires_delta)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """토큰검사 + 로그인 사용자 조회 + 블랙리스트 확인"""
    payload = decode_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if await is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been blacklisted",
        )
    user = await User.get_or_none(id=int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def login(username: str, password: str) -> Token:
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

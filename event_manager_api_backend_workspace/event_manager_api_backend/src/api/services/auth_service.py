from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

from ..schemas import UserCreate, UserShow, Token

# In-memory user store for demo only
users_db = {}
user_id_seq = 1

SECRET_KEY = "SUPERSECRETKEY"  # In production, set from env!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# PUBLIC_INTERFACE
def create_user(user: UserCreate) -> Optional[UserShow]:
    global user_id_seq
    # Check if username already exists
    if user.username in [u["username"] for u in users_db.values()]:
        return None
    user_obj = {
        "id": user_id_seq,
        "username": user.username,
        "hashed_password": get_password_hash(user.password)
    }
    users_db[user_id_seq] = user_obj
    user_id_seq += 1
    return UserShow(id=user_obj["id"], username=user_obj["username"])


# PUBLIC_INTERFACE
def authenticate_user(username: str, password: str) -> Optional[Token]:
    user = next((u for u in users_db.values() if u["username"] == username), None)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return Token(
        access_token=create_access_token(data={"sub": str(user["id"])}),
        token_type="bearer"
    )


def get_user_by_id(user_id: int) -> Optional[UserShow]:
    u = users_db.get(user_id)
    if u:
        return UserShow(id=u["id"], username=u["username"])
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme)) -> UserShow:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (jwt.PyJWTError, Exception):
        raise credentials_exception
    user = get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user

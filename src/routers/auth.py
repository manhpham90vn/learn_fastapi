import jwt
import datetime
from typing import Optional
from passlib.context import CryptContext
from ..models.user import User
from fastapi import APIRouter
from ..database import dbDepends
from starlette import status
from ..models.requests.register_request import RegisterRequest
from ..models.responses.register_response import RegisterResponse
from ..models.requests.login_request import LoginRequest
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import HTTPException, Depends

router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now(
        ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)] = None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return email


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
def register(db: dbDepends, request: RegisterRequest):
    user = User(request.email, request.first_name,
                request.last_name, bcrypt_context.hash(request.password), 'user')
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return RegisterResponse(id=user.id, email=user.email, first_name=user.first_name, last_name=user.last_name, role=user.role, access_token=access_token)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=RegisterResponse)
def login(db: dbDepends, request: LoginRequest):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return {"error": "Invalid credentials"}

    if not bcrypt_context.verify(request.password, user.hashed_password):
        return {"error": "Invalid credentials"}

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return RegisterResponse(id=user.id, email=user.email, first_name=user.first_name, last_name=user.last_name, role=user.role, access_token=access_token)

from passlib.context import CryptContext
from ..models.user import User
from fastapi import APIRouter, HTTPException
from ..dependency import dbDepends
from starlette import status
from ..models.requests.register_request import RegisterRequest
from ..models.responses.register_response import RegisterResponse
from ..models.requests.login_request import LoginRequest
from ..utils import create_access_token
import json

router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
def register(db: dbDepends, request: RegisterRequest):
    is_email_exist = db.query(User).filter(User.email == request.email).first()

    if is_email_exist is not None:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(request.email, request.first_name,
                request.last_name, bcrypt_context.hash(request.password), 'user')
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        data={"sub": json.dumps({"email": user.email, "id": user.id})}
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
        data={"sub": json.dumps({"email": user.email, "id": user.id})}
    )
    return RegisterResponse(id=user.id, email=user.email, first_name=user.first_name, last_name=user.last_name, role=user.role, access_token=access_token)

from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=100)
from pydantic import BaseModel, Field, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., min_length=3, max_length=100)
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=100)

from pydantic import BaseModel


class RegisterResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    access_token: str

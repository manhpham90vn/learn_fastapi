from pydantic import BaseModel, Field


class BookRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {"title": "Harry Potter", "author": "J.K. Rowling"}
        }
    }

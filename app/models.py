from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str


class TodoItem(BaseModel):
    id: int
    title: str
    done: bool
    created_at: str
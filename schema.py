from pydantic import BaseModel
class StudentCreate(BaseModel):
    name: str
    email: str
    course: str
    password: str

class StudentUpdate(BaseModel):
    name: str
    email: str
    course: str
    password: str


class StudentPatch(BaseModel):
    name: str | None = None
    email: str | None = None
    course: str | None = None
    password: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


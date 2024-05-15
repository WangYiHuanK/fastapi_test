from typing import List
from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int
    cls_id: int


class StudentCreateList(BaseModel):
    student_list: list[StudentCreate]


class ClassroomCreate(BaseModel):
    name: str
    lv: str


class ClassroomCreateList(BaseModel):
    classroom_list: list[ClassroomCreate]

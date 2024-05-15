from sqlalchemy import Column, DECIMAL, Boolean, JSON
from settings.db import BaseModel
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, ENUM


# 学生
class ClassRoom(BaseModel):
    __cn_tablename__ = "班级"
    __tablename__ = 'tb_classroom'
    name = Column(VARCHAR(100), comment='班级名称')
    lv = Column(VARCHAR(100), default='', comment='等级')


# 学生
class Student(BaseModel):
    __cn_tablename__ = "学生"
    __tablename__ = 'tb_student'
    name = Column(VARCHAR(100), comment='姓名')
    age = Column(INTEGER(100), default=0, comment='年龄')
    cls_id = Column(INTEGER(display_width=11), default=None, comment="班级主键")


custom_models = [ClassRoom, Student]

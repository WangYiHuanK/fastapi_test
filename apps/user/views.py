import calendar
import copy
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Query
from fastapi import Request
from fastapi import Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .models import Student
from .models import ClassRoom
from .schemas import *
from utils.common import CommonQueryParams
from utils.common import row_dict
from utils.resp import MyResponse
from utils.constant import RET
from utils.constant import error_map
from utils.utils import permission_required
from settings.db import get_db
from settings.db import MyPagination

StudentRouter = APIRouter(tags=['学生'])


@cbv(StudentRouter)
class StudentServer:
    request: Request

    @StudentRouter.get('/list', description='学生信息列表')
    async def get_student_list(self, common_query: CommonQueryParams = Depends(), db: Session = Depends(get_db)):
        query = [Student.is_delete == False]
        if common_query.q:
            query.append(Student.name.ilike(f'%{common_query.q}%'))
        query = db.query(Student).filter(*query)
        query = query.order_by(desc(Student.id))
        obj = MyPagination(query, common_query.page, common_query.page_size)
        return MyResponse(data=obj.data, total=obj.counts)

    @StudentRouter.post('/list', description='增加学生信息')
    async def create_students(self, students: StudentCreateList, db: Session = Depends(get_db)):
        new_student_list = []
        for student in students.student_list:
            new_student_list.append(Student(**student.dict()))
        if new_student_list:
            db.bulk_insert_mappings(Student, [obj.__dict__ for obj in new_student_list])
            db.commit()
        else:
            return MyResponse(RET.DATA_EXIST, error_map[RET.DATA_EXIST])
        return MyResponse()

    @StudentRouter.get('/list/{id}', description='学生详情信息')
    async def retrieve_student(self, id: int, db: Session = Depends(get_db)):
        query = db.query(Student).filter(Student.id == id).one_or_none()
        if query:
            data = row_dict(query)
            cls_query = db.query(ClassRoom).filter(ClassRoom.id == data['cls_id']).one_or_none()
            if cls_query:
                cls_data = row_dict(cls_query)
                data['cls_data'] = cls_data
            return MyResponse(data=data)
        return MyResponse(RET.NO_DATA, error_map[RET.NO_DATA])

    @StudentRouter.post('/list/{id}', description='删除学生信息')
    async def delete_student(self, id: int, db: Session = Depends(get_db)):
        query = db.query(Student).filter(Student.id == id).first()
        if not query:
            return MyResponse(RET.NO_DATA, error_map[RET.NO_DATA])
        query.is_delete = 1
        db.commit()
        return MyResponse()

    @StudentRouter.put('/list/{id}', description='修改学生信息')
    async def update_student(self, id: int, student: StudentCreate, db: Session = Depends(get_db)):
        query = db.query(Student).filter(Student.id == id).first()
        if not query:
            return MyResponse(RET.NO_DATA, error_map[RET.NO_DATA])
        query.name = student.name
        query.age = student.age
        query.cls_id = student.cls_id
        db.commit()
        return MyResponse()


ClassroomRouter = APIRouter(tags=['班级'])


@cbv(ClassroomRouter)
class ClassroomServer:
    request: Request

    @ClassroomRouter.get('/list', description='班级列表')
    async def get_classroom_list(self, common_query: CommonQueryParams = Depends(), db: Session = Depends(get_db)):
        query = [ClassRoom.is_delete == False]
        if common_query.q:
            query.append(ClassRoom.name.ilike(f'%{common_query.q}%'))
        query = db.query(ClassRoom).filter(*query)
        query = query.order_by(desc(ClassRoom.id))
        obj = MyPagination(query, common_query.page, common_query.page_size)
        return MyResponse(data=obj.data, total=obj.counts)

    @ClassroomRouter.post('/list', description='增加班级')
    # @permission_required(ClassRoom, 'INSERT')
    async def create_classroom(self, data: ClassroomCreateList, db: Session = Depends(get_db)):
        classrooms = [classroom.name for classroom in data.classroom_list]
        if len(classrooms) != len(set(classrooms)):
            return MyResponse(RET.DATA_EXIST, "新增班级不可重复")
        existing_name = db.query(ClassRoom.name).filter(
            ClassRoom.name.in_(classrooms)
        ).all()
        existing_name = [name[0] for name in existing_name]
        new_classrooms = []
        for classroom in data.classroom_list:
            if classroom.name in existing_name:
                classroom_id = db.query(ClassRoom).filter(ClassRoom.name == classroom.name).filter()
                if classroom_id.is_delete == False:
                    return MyResponse(RET.DATA_EXIST, f'{classroom.name}已存在')
                else:
                    classroom_id.is_delete = False
                    db.commit()
            else:
                new_classroom = ClassRoom(**classroom.dict())
                new_classrooms.append(new_classroom)
        if new_classrooms:
            db.bulk_insert_mappings(ClassRoom, [obj.__dict__ for obj in new_classrooms])
            db.commit()
        return MyResponse()

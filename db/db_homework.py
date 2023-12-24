from fastapi import HTTPException, status
import ast
from router.schemas import HomeworkRequestSchema, HomeworkResponseSchema
from sqlalchemy.orm.session import Session
from .models import DbHomework
from .one_table_homework import homework


def db_feed(db: Session):
    new_homework_list = [DbHomework(
        school=homework["school"],
        semester=homework["semester"],
        workName=homework["workName"],
        githubUrl=homework["githubUrl"],
        websiteUrl=homework["websiteUrl"],
        pptUrl=homework["pptUrl"],
        imgUrl=homework["imgUrl"],
        skill=homework["skill"],
        name=homework["name"]
    ) for homework in homework]
    db.query(DbHomework).delete()
    db.commit()
    db.add_all(new_homework_list)
    db.commit()
    db_items = db.query(DbHomework).all()
    return [HomeworkResponseSchema.from_orm(item) for item in db_items]


def create(db: Session, request: HomeworkRequestSchema):
    new_homework = DbHomework(
        school=request.school,
        semester=request.semester,
        workName=request.workName,
        githubUrl=request.githubUrl,
        websiteUrl=request.websiteUrl,
        pptUrl=request.pptUrl,
        imgUrl=request.imgUrl,
        skill=request.skill,
        name=request.name
    )
    db.add(new_homework)
    db.commit()
    db.refresh(new_homework)
    return HomeworkResponseSchema.from_orm(new_homework)


def str2List(homework_records: list):
    for record in homework_records:
        if record.skill:  # 確保 school 字段不是空的
            # 將 school 字串轉換回列表
            record.skill = ast.literal_eval(record.skill)
        if record.name:  # 確保 school 字段不是空的
            # 將 school 字串轉換回列表
            record.name = ast.literal_eval(record.name)

    return homework_records


def get_all(db: Session):
    homework = db.query(DbHomework).all()
    if not homework:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Homework not found')
    return [HomeworkResponseSchema.from_orm(item) for item in homework]



def get_homework_by_semester(semester: str, db: Session):
    homework = db.query(DbHomework).filter(DbHomework.semester == semester).all()
    if not homework:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Homework with semester = {semester} not found')
    return [HomeworkResponseSchema.from_orm(item) for item in homework]


def get_homework_by_school(school: str, db: Session):
    homework = db.query(DbHomework).filter(DbHomework.school == school).all()
    if not homework:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Homework with school = {school} not found')
    return [HomeworkResponseSchema.from_orm(item) for item in homework]
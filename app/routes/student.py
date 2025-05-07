from fastapi import APIRouter, Header, HTTPException
from app.models.schemas import StudentResponse
from database.sql import Student

router = APIRouter()

@router.get("/student", response_model=StudentResponse)
async def get_student_info(NIM: str = Header(...)):
    student = Student()

    student_info = student.read(NIM)

    if not student_info:
        raise HTTPException(status_code=404, detail="Student not found")

    nim, name, classes = student_info
    return {"nama": name, "class_uids": classes}

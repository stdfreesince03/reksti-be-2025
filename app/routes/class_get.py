from fastapi import APIRouter, HTTPException, Header
from app.models.schemas import ClassInfoResponse
from database.sql import ClassEntry, Student

router = APIRouter()

@router.get("/class", response_model=ClassInfoResponse)
async def get_class_info(class_uid: str = Header(...)):
    students = ClassEntry.read(class_uid)
    
    if not students:
        raise HTTPException(status_code=404, detail="Class not found or no students in class")

    students_info = []
    for student in students:
        students_info.append({
            "NIM": student["nim"],
            "status": student["status"]
        })
    
    return {"students": students_info}

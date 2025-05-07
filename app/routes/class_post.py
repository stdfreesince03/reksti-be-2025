from fastapi import APIRouter, HTTPException
from app.models.schemas import ClassCreateRequest, ClassCreateResponse
import uuid
from database.sql import ClassEntry

router = APIRouter()

@router.post("/class", response_model=ClassCreateResponse)
async def create_class(data: ClassCreateRequest):
    class_uid = str(uuid.uuid4())

    try:
        for nim in data.student:
            ClassEntry.create(class_uid, nim, False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create class: {e}")

    return {"status": True, "class_uid": class_uid}

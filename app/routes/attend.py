from fastapi import APIRouter, HTTPException
from app.models.schemas import AttendRequest, AttendResponse
from src.model import get_encoding_base64, compare
from database.sql import Encoding, ClassEntry

router = APIRouter()

@router.post("/attend", response_model=AttendResponse)
async def attend_class(data: AttendRequest):
    try:
        input_encoding = get_encoding_base64(data.foto_wajah)
        if input_encoding is None:
            raise ValueError("No face detected")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process photo: {str(e)}")

    stored_encoding = Encoding.read(data.NIM)
    if stored_encoding is None:
        raise HTTPException(status_code=404, detail="Student encoding not found")

    match = compare(stored_encoding, input_encoding)

    if match:
        ClassEntry.update(data.class_uid, data.NIM, True)
        return {"status": True, "message": "Attendance recorded"}
    else:
        return {"status": False, "message": "Face mismatch"}

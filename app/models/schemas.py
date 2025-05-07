from pydantic import BaseModel
from typing import List

class RegisterRequest(BaseModel):
    NIM: str
    nama_lengkap: str
    foto_wajah: str

class RegisterResponse(BaseModel):
    status: bool
    message: str

class StudentResponse(BaseModel):
    nama: str
    class_uids: List[str]

class AttendRequest(BaseModel):
    NIM: str
    class_uid: str
    foto_wajah: str

class AttendResponse(BaseModel):
    status: bool
    message: str

class ClassCreateRequest(BaseModel):
    student: List[str]

class ClassCreateResponse(BaseModel):
    status: bool
    class_uid: str

class ClassInfoResponse(BaseModel):
    students: List[dict]  # Example: [{"NIM": "123", "status": True}]

from fastapi import FastAPI
from app.routes import register, student, attend, class_post, class_get

app = FastAPI()

app.include_router(register.router)
app.include_router(student.router)
app.include_router(attend.router)
app.include_router(class_post.router)
app.include_router(class_get.router)
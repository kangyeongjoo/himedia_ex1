from fastapi import FastAPI, Form, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

#파일 업로드 코드 import
from fastapi import File, UploadFile, HTTPException
from pathlib import Path

import os

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models


# models에 정의한 모든 클래스, 연결한 DB엔진에 테이블로 생성
Base.metadata.create_all(bind=engine)

# fastapi 객체생성
app = FastAPI()

# 동영상 파일 디렉토리가 없다면 생성
UPLOAD_DIRECTORY = "./uploaded_files"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

abs_path = os.path.dirname(os.path.realpath(__file__))

# html 템플릿 객체 생성
# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(directory=f"{abs_path}/templates")

# static 폴더(정적파일 폴더)를 app에 연결
# app.mount("/static", StaticFiles(directory=f"static"))
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"))

# Dependency Injection(의존성 주임을 위한 함수) 
# yield :  FastAPI가 함수 실행을 일시 중지하고 DB 세션을 호출자에게 반환하도록 지시
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

#화면 띄우기
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).order_by(models.Todo.id.desc()).all()  # 모든 결과를 리스트로 가져옴

    # 결과가 없을 경우 빈 리스트를 사용
    if len(todos) == 0:
        todos = []

    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos
    })

#데이터 삽입하기
@app.post("/add")
def add(req: Request, title: str = Form(...), db: Session = Depends(get_db)):
    print(title)
    # Todo 객체 생성
    new_todo = models.Todo(task=title)
    # DB테이블에 create
    db.add(new_todo)
    # db 트랜젝션 완료
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# 수정할 todo 클릭했을 때
@app.get("/update/{todo_id}")
def add(req: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    print(todo.completed)
    todo.completed = not todo.completed
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# todo 삭제
@app.get("/delete/{todo_id}")
def add(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

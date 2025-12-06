from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .send_mail import send_otp_email
from . import models
from typing import List
from .database import engine, SessionLocal
from .schema import * 
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo Application",
    description="A simple Todo application with user authentication and OTP verification.",
    version="1.0.0",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to my todo application!"}

@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # check duplicate email
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # hash password
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # create otp
    code = 123456  # In real application, generate a random OTP and send via email/SMS
    otp = models.Otp(
        user_id=db_user.id,
        otp_code=code  # In real application, generate a random OTP and send via email/SMS  
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)

    send_otp_email(to_email=db_user.email, otp_code=code)
    # return user without password
    return {
        "id": getattr(db_user, "id", None),
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "email": db_user.email
    }

@app.post("/todos/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    #checking if a todo already exists
    existing = db.query(models.TodoModel).filter(models.TodoModel.title == todo.title).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"A task with this title{todo.title}, already exists."
        )
        
    db_todo=models.TodoModel(
            title = todo.title,
            subtitle = todo.subtitle,
            description = todo.description,
            owner_id = todo.owner_id,
            date = todo.date,
            time = todo.time,
            completed = False
    ) 

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


   
@app.get("/todos/", response_model=List[ReadTodo],status_code=status.HTTP_200_OK)
def get_all_todos(db: Session = Depends(get_db)):
   
    todos= db.query(models.TodoModel).all()

    if not todos :
        raise HTTPException(
            status_code=404,
            detail="No current tasks"
        )
    return todos

     
   
    
@app.put("/todos/{todo_id}",response_model=ReadTodo, status_code=status.HTTP_200_OK)
def update_todo(todo_id:int,todo: TodoUpdate, db: Session = Depends(get_db)):
    #checking if a todo already exists
    existing_todo= db.query(models.TodoModel).filter(models.TodoModel.id ==todo_id).first()
    if not existing_todo:
        raise HTTPException(
            status_code=404,
            detail=f"No current task with id{todo_id}."
        )
    
    
    if todo.title is not None:
        existing_todo.title= todo.title
    if todo.subtitle is not None:
        existing_todo.subtitle= todo.subtitle
    if todo.description is not None:
        existing_todo.description= todo.description
    if todo.date is not None:
        existing_todo.date= todo.date
    if todo.time is not None:
        existing_todo.time= todo.time
    if todo.completed is not None:
        existing_todo.completed= todo.completed

    db.commit()
    db.refresh(existing_todo) 
    return existing_todo


@app.delete("/todos/{todo_id}", response_model=DeleteTodo,status_code=status.HTTP_200_OK )
def delete_todo (todo_id:int, db:Session=Depends(get_db)):
    todo=db.query(models.TodoModel).filter(models.TodoModel.id==todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=404, detail="Todo not found"
        )

    db.delete(todo)
    db.commit()

    return DeleteTodo(message=f"Todo with id {todo_id}, deleted successfully")
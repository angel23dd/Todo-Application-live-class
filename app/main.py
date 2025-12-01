from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .send_mail import send_otp_email
from . import models
from .database import engine, SessionLocal
from .schema import UserCreate
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
from fastapi import FastAPI, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import User
from .schemas import UserResponse
from .security import security, get_current_user

app = FastAPI(title="User Service", version="1.0.0")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"service": "user", "status": "ok"}

@app.get("/users/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    current = get_current_user(credentials)
    user = db.query(User).filter(User.id == current["id"]).first()

    if not user:
        user = User(
            id=current["id"],
            email=current["email"],
            full_name=current["email"].split("@")[0],
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return UserResponse.model_validate(user)

@app.get("/users", response_model=list[UserResponse])
def list_users(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    get_current_user(credentials)
    return db.query(User).order_by(User.id).all()

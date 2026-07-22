from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.register_schema import RegisterUser
from app.auth.password import hash_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }
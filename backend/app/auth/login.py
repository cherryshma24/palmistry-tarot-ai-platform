from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.login_schema import LoginUser
from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token  # Import JWT function

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    # Find user by email
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    # User not found
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate JWT Access Token
    access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "user_id": existing_user.id
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }
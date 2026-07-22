from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.auth.jwt_handler import verify_access_token


# Clean token handling (NO Swagger OAuth confusion)
oauth2_scheme = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract token string
    payload = verify_access_token(token.credentials)

    if payload is None:
        raise credentials_exception

    # Get email from token
    email = payload.get("sub")

    if email is None:
        raise credentials_exception

    # Fetch user from DB
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user



# ===============================
# RBAC ROLE CHECKER
# ===============================

def require_role(required_role: str):
    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker
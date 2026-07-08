from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.core.security import decode_access_token
from backend.database.session import get_db
from backend.database.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(db: Session = Depends(get_db)) -> User:
    # Bypassed authentication to support local mode without login
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(
            id=1,
            name="Default User",
            email="default@example.com",
            password_hash="disabled"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

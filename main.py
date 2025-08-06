from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from schemas import UserCreate, SubscriptionCreate
import crud

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register User only
@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# Subscribe (user must already be registered)
@app.post("/subscribe/")
def subscribe(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    result = crud.create_subscription(db, subscription)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "message": "Subscription successful",
        "name": subscription.name
    }

# Referral summary endpoint
@app.get("/referral-summary/{username}")
def referral_summary(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "referral_code": user.referral_code,
        "referred_by": user.referred_by,
        "level": user.level,
        "total_referrals": user.total_referrals,
        "total_earned": user.total_earned
    }

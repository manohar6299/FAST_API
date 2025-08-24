from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from schemas import UserCreate, SubscriptionCreate, Signin
import crud
import  models


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
    
   existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
   
   if existing_user:
        return {"message": f"User '{user.username}' is already registered"}

   new_user = crud.create_user(db, user)
    
   if new_user:
        return {"message": f"User '{user.username}' registered successfully"}
   else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed"
        )
        
        
        
@app.post("/signin")
def signin(data: Signin, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == data.login) | (User.email == data.login)).first()
    if user.password != user.conform_password:
         raise HTTPException(status_code=400, detail="Passwords do not match")
    # return {"message": "Login successful", "user_id": user.id}
    return {"message": "Login successful", "user_name": user.username,  "user_id": user.id}




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

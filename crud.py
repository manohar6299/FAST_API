from models import User, Subscription
from sqlalchemy.orm import Session
import uuid

def create_user(db: Session, user_data):
    referral_code = f"{user_data.username}_ref"
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        referred_by=user_data.referred_by,
        referral_code=referral_code
    )
    db.add(new_user)

    # Update referral count if referred_by exists
    # if user_data.referred_by:
    #     referrer = db.query(User).filter_by(referral_code=user_data.referred_by).first()
    #     if referrer:
    #         referrer.total_referrals += 1
    #         referrer.total_earned += 10.0

    db.commit()
    db.refresh(new_user)
    return new_user

# def create_subscription(db: Session, sub_data):
#     user = db.query(User).filter_by(id=sub_data.user_id).first()
#     if not user:
#         return None
#     new_sub = Subscription(
#         user_id=sub_data.user_id,
#         amount=sub_data.amount,
#         name=sub_data.name
#     )
#     db.add(new_sub)
#     db.commit()
#     db.refresh(new_sub)
#     return new_sub
def create_subscription(db: Session, sub_data):
    user = db.query(User).filter_by(id=sub_data.user_id).first()
    if not user:
        return None

    # Add the subscription
    new_sub = Subscription(
        user_id=sub_data.user_id,
        amount=sub_data.amount,
        name=sub_data.name
    )
    db.add(new_sub)

    # Give 10% commission to referrer if exists
    if user.referred_by:
        referrer = db.query(User).filter_by(referral_code=user.referred_by).first()
        if referrer:
            commission = sub_data.amount * 0.10
            referrer.total_earned += commission
            db.add(referrer)  # optional but good practice

    db.commit()
    db.refresh(new_sub)
    return new_sub

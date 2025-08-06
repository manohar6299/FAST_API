from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    referral_code = Column(String, unique=True)
    referred_by = Column(String, ForeignKey('users.referral_code'), nullable=True)
    level = Column(String, default='Basic')
    total_referrals = Column(Integer, default=0)
    total_earned = Column(Float, default=0.0)

    referrals = relationship('User', backref='referrer', remote_side=[referral_code])


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

from pydantic import BaseModel
from typing import Optional , List


class UserCreate(BaseModel):
    username: str
    email: str
    referred_by: Optional[str] = None


class SubscriptionCreate(BaseModel):
    user_id: int
    amount: float
    name: str
    
class ReferredUser(BaseModel):
    id: int
    username: str
    email: str
    subscription_amount: Optional[float] = 0.0

    class Config:
        orm_mode = True

class ReferralStats(BaseModel):
    referrer_username: str
    total_referrals: int
    total_earned: float
    referrals: List[ReferredUser]
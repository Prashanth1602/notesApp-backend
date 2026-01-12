from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from db_config import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from models.users import Users

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("Users", backref="refresh_tokens")
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
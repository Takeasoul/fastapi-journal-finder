from sqlalchemy import Column, Integer, String
from app.core.base import Base

class IPWhitelist(Base):
    __tablename__ = "ip_whitelist"
    id = Column(Integer, primary_key=True, index=True)
    ip_network = Column(String(50), unique=True, nullable=False)
    organization_name = Column(String(255), nullable=True)

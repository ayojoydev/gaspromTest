from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Integer, unique=True, index=True, nullable=False)  # User ID
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")


class Device(Base):
    """Device model"""
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True, nullable=False)  # Unique device identifier
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="devices")
    readings = relationship("Reading", back_populates="device", cascade="all, delete-orphan")
    
    __table_args__ = (Index("idx_device_user", "device_id", "user_id"),)


class Reading(Base):
    """Device reading/statistic model"""
    __tablename__ = "readings"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, index=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    
    # Relationships
    device = relationship("Device", back_populates="readings")
    
    __table_args__ = (Index("idx_reading_device_time", "device_id", "timestamp"),)


class AnalysisResult(Base):
    """Cached analysis results"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    start_date = Column(DateTime, nullable=True, index=True)
    end_date = Column(DateTime, nullable=True, index=True)
    
    # Analysis fields for each axis
    x_min = Column(Float)
    x_max = Column(Float)
    x_sum = Column(Float)
    x_count = Column(Integer)
    x_median = Column(Float)
    
    y_min = Column(Float)
    y_max = Column(Float)
    y_sum = Column(Float)
    y_count = Column(Integer)
    y_median = Column(Float)
    
    z_min = Column(Float)
    z_max = Column(Float)
    z_sum = Column(Float)
    z_count = Column(Integer)
    z_median = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

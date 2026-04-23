from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ReadingCreate(BaseModel):
    """Reading creation model"""
    x: float = Field(..., description="X axis value")
    y: float = Field(..., description="Y axis value")
    z: float = Field(..., description="Z axis value")


class Reading(ReadingCreate):
    """Reading model"""
    id: int
    device_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class DeviceCreate(BaseModel):
    """Device creation model"""
    device_id: int = Field(..., description="Unique device identifier")
    user_id: int = Field(..., description="User ID")


class Device(DeviceCreate):
    """Device model"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """User creation model"""
    user_id: int = Field(..., description="User identifier")


class User(UserCreate):
    """User model"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalysisMetrics(BaseModel):
    """Analysis metrics for a single axis"""
    min: Optional[float] = None
    max: Optional[float] = None
    sum: Optional[float] = None
    count: Optional[int] = None
    median: Optional[float] = None


class ReadingAnalysis(BaseModel):
    """Reading analysis result"""
    x: AnalysisMetrics
    y: AnalysisMetrics
    z: AnalysisMetrics


class DeviceAnalysis(BaseModel):
    """Device analysis result"""
    device_id: int
    analysis: ReadingAnalysis
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None


class UserAnalysis(BaseModel):
    """User analysis result"""
    user_id: int
    aggregated_analysis: ReadingAnalysis
    devices: List[DeviceAnalysis]


class AnalysisRequest(BaseModel):
    """Analysis request model"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class StatusResponse(BaseModel):
    """Status response model"""
    status: str
    message: str

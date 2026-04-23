from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas import (
    ReadingCreate,
    DeviceCreate,
    UserCreate,
    AnalysisRequest,
    StatusResponse,
    ReadingAnalysis,
    DeviceAnalysis,
    UserAnalysis,
    AnalysisMetrics,
)
from app.services.data_service import UserService, DeviceService, ReadingService
from app.tasks.analytics import analyze_device_readings, analyze_user_devices

router = APIRouter(prefix="/api", tags=["API"])


# User endpoints
@router.post("/users", response_model=StatusResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    try:
        UserService.create_user(db, user.user_id)
        return StatusResponse(status="success", message=f"User {user.user_id} created")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Device endpoints
@router.post("/devices", response_model=StatusResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """Create a new device for user"""
    try:
        DeviceService.create_device(db, device.device_id, device.user_id)
        return StatusResponse(
            status="success",
            message=f"Device {device.device_id} created for user {device.user_id}",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Reading endpoints
@router.post("/readings", response_model=StatusResponse)
def add_reading(
    device_id: int,
    user_id: int,
    reading: ReadingCreate,
    db: Session = Depends(get_db),
):
    """Add a new reading for a device"""
    try:
        ReadingService.add_reading(
            db, device_id, user_id, reading.x, reading.y, reading.z
        )
        return StatusResponse(status="success", message="Reading added")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/readings/batch", response_model=StatusResponse)
def add_readings_batch(
    device_id: int,
    user_id: int,
    readings: list[ReadingCreate],
    db: Session = Depends(get_db),
):
    """Add multiple readings at once"""
    try:
        for reading in readings:
            ReadingService.add_reading(
                db, device_id, user_id, reading.x, reading.y, reading.z
            )
        return StatusResponse(
            status="success",
            message=f"Added {len(readings)} readings",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Analysis endpoints
@router.post("/analysis/device/{device_id}")
def analyze_device(
    device_id: int,
    user_id: int,
    analysis_req: AnalysisRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze device readings for a specific period.
    This triggers an async Celery task.
    """
    try:
        # Check if device exists
        device = DeviceService.get_device(db, device_id, user_id)
        if not device:
            raise HTTPException(
                status_code=404, detail="Device not found for this user"
            )
        
        # Trigger async analysis task
        task = analyze_device_readings.delay(
            device.id,
            analysis_req.start_date,
            analysis_req.end_date,
        )
        
        return {
            "status": "processing",
            "task_id": task.id,
            "message": "Analysis task started",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/analysis/device/{device_id}/result/{task_id}")
def get_device_analysis(device_id: int, user_id: int, task_id: str):
    """Get analysis result for a device"""
    try:
        task = analyze_device_readings.AsyncResult(task_id)
        
        if task.state == "PENDING":
            return {
                "status": "pending",
                "task_id": task_id,
            }
        elif task.state == "SUCCESS":
            return {
                "status": "success",
                "task_id": task_id,
                "result": task.result,
            }
        elif task.state == "FAILURE":
            return {
                "status": "failed",
                "task_id": task_id,
                "error": str(task.info),
            }
        else:
            return {
                "status": task.state.lower(),
                "task_id": task_id,
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analysis/user/{user_id}")
def analyze_user(
    user_id: int,
    analysis_req: AnalysisRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze all devices for a user.
    This triggers an async Celery task.
    """
    try:
        # Check if user exists
        user = UserService.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Trigger async analysis task
        task = analyze_user_devices.delay(
            user.id,
            analysis_req.start_date,
            analysis_req.end_date,
        )
        
        return {
            "status": "processing",
            "task_id": task.id,
            "message": "Analysis task started",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/analysis/user/{user_id}/result/{task_id}")
def get_user_analysis(user_id: int, task_id: str):
    """Get analysis result for a user"""
    try:
        task = analyze_user_devices.AsyncResult(task_id)
        
        if task.state == "PENDING":
            return {
                "status": "pending",
                "task_id": task_id,
            }
        elif task.state == "SUCCESS":
            return {
                "status": "success",
                "task_id": task_id,
                "result": task.result,
            }
        elif task.state == "FAILURE":
            return {
                "status": "failed",
                "task_id": task_id,
                "error": str(task.info),
            }
        else:
            return {
                "status": task.state.lower(),
                "task_id": task_id,
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Health check
@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Service is running"}

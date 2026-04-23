from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from numpy import median as np_median
from app.tasks.celery_app import celery_app
from app.db.models import Reading, Device, AnalysisResult
from app.db.database import SessionLocal


def calculate_statistics(values: list) -> Dict[str, Any]:
    """Calculate statistics for a list of values"""
    if not values:
        return {
            "min": None,
            "max": None,
            "sum": None,
            "count": 0,
            "median": None,
        }
    
    return {
        "min": float(min(values)),
        "max": float(max(values)),
        "sum": float(sum(values)),
        "count": len(values),
        "median": float(np_median(values)),
    }


@celery_app.task(bind=True, max_retries=3)
def analyze_device_readings(
    self,
    device_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    Analyze device readings for a specific period
    This task runs asynchronously using Celery
    """
    try:
        db = SessionLocal()
        
        # Query readings
        query = db.query(Reading).filter(Reading.device_id == device_id)
        
        if start_date:
            query = query.filter(Reading.timestamp >= start_date)
        if end_date:
            query = query.filter(Reading.timestamp <= end_date)
        
        readings = query.all()
        
        # Calculate statistics for each axis
        x_values = [r.x for r in readings]
        y_values = [r.y for r in readings]
        z_values = [r.z for r in readings]
        
        analysis = {
            "device_id": device_id,
            "x": calculate_statistics(x_values),
            "y": calculate_statistics(y_values),
            "z": calculate_statistics(z_values),
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        }
        
        # Save results to cache
        try:
            result = AnalysisResult(
                device_id=device_id,
                start_date=start_date,
                end_date=end_date,
                x_min=analysis["x"]["min"],
                x_max=analysis["x"]["max"],
                x_sum=analysis["x"]["sum"],
                x_count=analysis["x"]["count"],
                x_median=analysis["x"]["median"],
                y_min=analysis["y"]["min"],
                y_max=analysis["y"]["max"],
                y_sum=analysis["y"]["sum"],
                y_count=analysis["y"]["count"],
                y_median=analysis["y"]["median"],
                z_min=analysis["z"]["min"],
                z_max=analysis["z"]["max"],
                z_sum=analysis["z"]["sum"],
                z_count=analysis["z"]["count"],
                z_median=analysis["z"]["median"],
            )
            db.add(result)
            db.commit()
        except Exception:
            db.rollback()
        
        db.close()
        return analysis
        
    except Exception as exc:
        db.close()
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@celery_app.task(bind=True, max_retries=3)
def analyze_user_devices(
    self,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    Analyze all devices for a specific user
    """
    try:
        db = SessionLocal()
        
        # Get all devices for user
        devices = db.query(Device).filter(Device.user_id == user_id).all()
        device_ids = [d.id for d in devices]
        
        if not device_ids:
            db.close()
            return {
                "user_id": user_id,
                "devices": [],
                "aggregated_analysis": {
                    "x": {"min": None, "max": None, "sum": None, "count": 0, "median": None},
                    "y": {"min": None, "max": None, "sum": None, "count": 0, "median": None},
                    "z": {"min": None, "max": None, "sum": None, "count": 0, "median": None},
                },
            }
        
        # Get all readings for user's devices
        query = db.query(Reading).filter(Reading.device_id.in_(device_ids))
        
        if start_date:
            query = query.filter(Reading.timestamp >= start_date)
        if end_date:
            query = query.filter(Reading.timestamp <= end_date)
        
        readings = query.all()
        
        # Aggregate statistics
        x_values = [r.x for r in readings]
        y_values = [r.y for r in readings]
        z_values = [r.z for r in readings]
        
        aggregated_analysis = {
            "x": calculate_statistics(x_values),
            "y": calculate_statistics(y_values),
            "z": calculate_statistics(z_values),
        }
        
        # Save aggregated result
        try:
            result = AnalysisResult(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                x_min=aggregated_analysis["x"]["min"],
                x_max=aggregated_analysis["x"]["max"],
                x_sum=aggregated_analysis["x"]["sum"],
                x_count=aggregated_analysis["x"]["count"],
                x_median=aggregated_analysis["x"]["median"],
                y_min=aggregated_analysis["y"]["min"],
                y_max=aggregated_analysis["y"]["max"],
                y_sum=aggregated_analysis["y"]["sum"],
                y_count=aggregated_analysis["y"]["count"],
                y_median=aggregated_analysis["y"]["median"],
                z_min=aggregated_analysis["z"]["min"],
                z_max=aggregated_analysis["z"]["max"],
                z_sum=aggregated_analysis["z"]["sum"],
                z_count=aggregated_analysis["z"]["count"],
                z_median=aggregated_analysis["z"]["median"],
            )
            db.add(result)
            db.commit()
        except Exception:
            db.rollback()
        
        db.close()
        
        return {
            "user_id": user_id,
            "devices": device_ids,
            "aggregated_analysis": aggregated_analysis,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        }
        
    except Exception as exc:
        db.close()
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

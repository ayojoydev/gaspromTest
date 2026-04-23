from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.models import User, Device, Reading
from app.models.schemas import (
    UserCreate,
    DeviceCreate,
    ReadingCreate,
)


class UserService:
    """Service for user operations"""
    
    @staticmethod
    def create_user(db: Session, user_id: int) -> User:
        """Create a new user"""
        db_user = db.query(User).filter(User.username == user_id).first()
        if db_user:
            return db_user
        
        db_user = User(username=user_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.username == user_id).first()
    
    @staticmethod
    def get_or_create_user(db: Session, user_id: int) -> User:
        """Get or create user"""
        user = UserService.get_user(db, user_id)
        if not user:
            user = UserService.create_user(db, user_id)
        return user


class DeviceService:
    """Service for device operations"""
    
    @staticmethod
    def create_device(db: Session, device_id: int, user_id: int) -> Device:
        """Create a new device for user"""
        # Ensure user exists
        user = UserService.get_or_create_user(db, user_id)
        
        # Check if device already exists
        db_device = db.query(Device).filter(
            and_(Device.device_id == device_id, Device.user_id == user.id)
        ).first()
        if db_device:
            return db_device
        
        db_device = Device(device_id=device_id, user_id=user.id)
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    
    @staticmethod
    def get_device(db: Session, device_id: int, user_id: int) -> Optional[Device]:
        """Get device by device_id and user_id"""
        user = UserService.get_user(db, user_id)
        if not user:
            return None
        
        return db.query(Device).filter(
            and_(Device.device_id == device_id, Device.user_id == user.id)
        ).first()
    
    @staticmethod
    def get_or_create_device(db: Session, device_id: int, user_id: int) -> Device:
        """Get or create device"""
        device = DeviceService.get_device(db, device_id, user_id)
        if not device:
            device = DeviceService.create_device(db, device_id, user_id)
        return device
    
    @staticmethod
    def list_user_devices(db: Session, user_id: int) -> List[Device]:
        """List all devices for user"""
        user = UserService.get_user(db, user_id)
        if not user:
            return []
        
        return db.query(Device).filter(Device.user_id == user.id).all()


class ReadingService:
    """Service for reading operations"""
    
    @staticmethod
    def add_reading(
        db: Session,
        device_id: int,
        user_id: int,
        x: float,
        y: float,
        z: float,
    ) -> Reading:
        """Add a new reading"""
        # Ensure device exists
        device = DeviceService.get_or_create_device(db, device_id, user_id)
        
        reading = Reading(device_id=device.id, x=x, y=y, z=z)
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return reading
    
    @staticmethod
    def get_device_readings(
        db: Session,
        device_id: int,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Reading]:
        """Get readings for a specific device"""
        device = DeviceService.get_device(db, device_id, user_id)
        if not device:
            return []
        
        query = db.query(Reading).filter(Reading.device_id == device.id)
        
        if start_date:
            query = query.filter(Reading.timestamp >= start_date)
        if end_date:
            query = query.filter(Reading.timestamp <= end_date)
        
        return query.order_by(Reading.timestamp.desc()).all()
    
    @staticmethod
    def get_user_readings(
        db: Session,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Reading]:
        """Get all readings for a user's devices"""
        devices = DeviceService.list_user_devices(db, user_id)
        device_ids = [d.id for d in devices]
        
        if not device_ids:
            return []
        
        query = db.query(Reading).filter(Reading.device_id.in_(device_ids))
        
        if start_date:
            query = query.filter(Reading.timestamp >= start_date)
        if end_date:
            query = query.filter(Reading.timestamp <= end_date)
        
        return query.order_by(Reading.timestamp.desc()).all()

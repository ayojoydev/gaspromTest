#!/usr/bin/env python
"""
Initialization script for Device Analytics Service
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def init_database():
    """Initialize the database"""
    print("Initializing database...")
    from app.db.database import init_db
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return False
    return True

def create_test_data():
    """Create test data"""
    print("\nCreating test data...")
    from app.db.database import SessionLocal
    from app.services.data_service import UserService, DeviceService, ReadingService
    import random
    
    db = SessionLocal()
    try:
        # Create test users
        for user_id in [1001, 1002, 1003]:
            UserService.create_user(db, user_id)
            print(f"✓ Created user {user_id}")
        
        # Create test devices
        devices_config = [
            (1001, [101, 102, 103]),
            (1002, [201, 202]),
            (1003, [301]),
        ]
        
        for user_id, device_ids in devices_config:
            for device_id in device_ids:
                DeviceService.create_device(db, device_id, user_id)
                print(f"✓ Created device {device_id} for user {user_id}")
        
        # Add test readings
        print("\nAdding test readings...")
        for user_id, device_ids in devices_config:
            for device_id in device_ids:
                for i in range(100):
                    x = random.uniform(-100, 100)
                    y = random.uniform(-100, 100)
                    z = random.uniform(-100, 100)
                    ReadingService.add_reading(db, device_id, user_id, x, y, z)
                print(f"✓ Added 100 readings for device {device_id}")
        
        print("\n✓ Test data created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error creating test data: {e}")
        return False
    finally:
        db.close()

def print_info():
    """Print information about the service"""
    print("\n" + "=" * 60)
    print("Device Analytics Service - Initialization Complete")
    print("=" * 60)
    print("\nAccess the service:")
    print("  - API:        http://localhost:8000")
    print("  - Swagger:    http://localhost:8000/docs")
    print("  - ReDoc:      http://localhost:8000/redoc")
    print("  - Flower:     http://localhost:5555")
    print("\nUseful commands:")
    print("  - Run tests:  locust -f tests/locustfile.py --host=http://localhost:8000")
    print("  - View logs:  docker-compose logs -f")
    print("  - Health:     curl http://localhost:8000/api/health")
    print("\nRun examples:")
    print("  - python examples.py")
    print("=" * 60 + "\n")

def main():
    """Main initialization function"""
    print("\n" + "=" * 60)
    print("Device Analytics Service - Initialization")
    print("=" * 60 + "\n")
    
    # Initialize database
    if not init_database():
        print("\nInitialization failed!")
        return 1
    
    # Create test data
    if not create_test_data():
        print("\nInitialization completed with warnings")
        return 1
    
    # Print info
    print_info()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

"""
API Usage Examples for Device Analytics Service
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL
BASE_URL = "http://localhost:8000/api"

# Example user and device IDs
USER_ID = 1001
DEVICE_ID = 101


def example_1_create_user():
    """Example 1: Create a user"""
    print("=" * 50)
    print("Example 1: Create User")
    print("=" * 50)
    
    url = f"{BASE_URL}/users"
    payload = {"user_id": USER_ID}
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def example_2_create_device():
    """Example 2: Create a device"""
    print("=" * 50)
    print("Example 2: Create Device")
    print("=" * 50)
    
    url = f"{BASE_URL}/devices"
    payload = {
        "device_id": DEVICE_ID,
        "user_id": USER_ID
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def example_3_add_single_reading():
    """Example 3: Add a single reading"""
    print("=" * 50)
    print("Example 3: Add Single Reading")
    print("=" * 50)
    
    url = f"{BASE_URL}/readings?device_id={DEVICE_ID}&user_id={USER_ID}"
    payload = {
        "x": 45.5,
        "y": -23.1,
        "z": 78.9
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def example_4_add_batch_readings():
    """Example 4: Add batch of readings"""
    print("=" * 50)
    print("Example 4: Add Batch Readings")
    print("=" * 50)
    
    url = f"{BASE_URL}/readings/batch?device_id={DEVICE_ID}&user_id={USER_ID}"
    
    # Generate 50 random readings
    readings = []
    for i in range(50):
        readings.append({
            "x": 45.5 + i * 0.1,
            "y": -23.1 + i * 0.2,
            "z": 78.9 - i * 0.15
        })
    
    response = requests.post(url, json=readings)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def example_5_analyze_device():
    """Example 5: Analyze device readings"""
    print("=" * 50)
    print("Example 5: Analyze Device Readings")
    print("=" * 50)
    
    url = f"{BASE_URL}/analysis/device/{DEVICE_ID}?user_id={USER_ID}"
    
    # Analysis for last 7 days
    now = datetime.utcnow()
    start_date = (now - timedelta(days=7)).isoformat()
    end_date = now.isoformat()
    
    payload = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Get task ID for polling results
    if "task_id" in result:
        task_id = result["task_id"]
        
        print("\nPolling results (waiting for async task)...")
        import time
        for i in range(10):
            time.sleep(1)
            
            result_url = f"{BASE_URL}/analysis/device/{DEVICE_ID}/result/{task_id}"
            result_response = requests.get(result_url)
            status = result_response.json().get("status")
            
            print(f"  Attempt {i+1}: Status = {status}")
            
            if status == "success":
                print(f"\nAnalysis Result: {json.dumps(result_response.json(), indent=2)}")
                break
    print()


def example_6_analyze_user():
    """Example 6: Analyze all user devices"""
    print("=" * 50)
    print("Example 6: Analyze User (All Devices)")
    print("=" * 50)
    
    url = f"{BASE_URL}/analysis/user/{USER_ID}"
    
    payload = {
        "start_date": None,
        "end_date": None
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Get task ID for polling results
    if "task_id" in result:
        task_id = result["task_id"]
        
        print("\nPolling results (waiting for async task)...")
        import time
        for i in range(10):
            time.sleep(1)
            
            result_url = f"{BASE_URL}/analysis/user/{USER_ID}/result/{task_id}"
            result_response = requests.get(result_url)
            status = result_response.json().get("status")
            
            print(f"  Attempt {i+1}: Status = {status}")
            
            if status == "success":
                print(f"\nAnalysis Result: {json.dumps(result_response.json(), indent=2)}")
                break
    print()


def example_7_health_check():
    """Example 7: Health check"""
    print("=" * 50)
    print("Example 7: Health Check")
    print("=" * 50)
    
    url = f"{BASE_URL}/health"
    
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def run_all_examples():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║  Device Analytics Service - API Examples   ║")
    print("╚" + "=" * 48 + "╝")
    print()
    
    try:
        example_1_create_user()
        example_2_create_device()
        example_3_add_single_reading()
        example_4_add_batch_readings()
        example_5_analyze_device()
        example_6_analyze_user()
        example_7_health_check()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API at", BASE_URL)
        print("Make sure the service is running with: docker-compose up -d")
    except Exception as e:
        print(f"ERROR: {str(e)}")


if __name__ == "__main__":
    run_all_examples()

from locust import HttpUser, task, between, events
import json
import random
from datetime import datetime


class DeviceAnalyticsUser(HttpUser):
    """Load testing for Device Analytics Service"""
    
    wait_time = between(1, 5)
    
    def on_start(self):
        """Setup - create test user and device"""
        self.user_id = random.randint(1000, 9999)
        self.device_id = random.randint(100, 999)
        
        # Create user
        self.client.post(
            "/api/users",
            json={"user_id": self.user_id},
        )
        
        # Create device
        self.client.post(
            "/api/devices",
            json={
                "device_id": self.device_id,
                "user_id": self.user_id,
            },
        )
    
    @task(10)
    def add_single_reading(self):
        """Add single reading"""
        reading = {
            "x": random.uniform(-100, 100),
            "y": random.uniform(-100, 100),
            "z": random.uniform(-100, 100),
        }
        
        self.client.post(
            f"/api/readings?device_id={self.device_id}&user_id={self.user_id}",
            json=reading,
        )
    
    @task(5)
    def add_batch_readings(self):
        """Add batch of readings"""
        readings = [
            {
                "x": random.uniform(-100, 100),
                "y": random.uniform(-100, 100),
                "z": random.uniform(-100, 100),
            }
            for _ in range(10)
        ]
        
        self.client.post(
            f"/api/readings/batch?device_id={self.device_id}&user_id={self.user_id}",
            json=readings,
        )
    
    @task(3)
    def analyze_device(self):
        """Trigger device analysis"""
        analysis_req = {}
        
        response = self.client.post(
            f"/api/analysis/device/{self.device_id}?user_id={self.user_id}",
            json=analysis_req,
        )
        
        if response.status_code == 200:
            task_id = response.json().get("task_id")
            # Poll result
            self.client.get(
                f"/api/analysis/device/{self.device_id}/result/{task_id}"
            )
    
    @task(2)
    def analyze_user(self):
        """Trigger user analysis"""
        analysis_req = {}
        
        response = self.client.post(
            f"/api/analysis/user/{self.user_id}",
            json=analysis_req,
        )
        
        if response.status_code == 200:
            task_id = response.json().get("task_id")
            # Poll result
            self.client.get(
                f"/api/analysis/user/{self.user_id}/result/{task_id}"
            )
    
    @task(1)
    def health_check(self):
        """Health check"""
        self.client.get("/api/health")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when load test starts"""
    print("\n========== Load Test Started ==========")
    print(f"Timestamp: {datetime.now()}")
    print("======================================\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when load test stops"""
    print("\n========== Load Test Stopped ==========")
    print(f"Timestamp: {datetime.now()}")
    print("======================================\n")

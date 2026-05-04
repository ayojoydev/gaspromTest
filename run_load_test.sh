#!/bin/bash
# Load testing script using Locust

echo "=========================================="
echo "Device Analytics Service - Load Testing"
echo "=========================================="
echo ""

# Check if locust is installed
if ! command -v locust &> /dev/null; then
    echo "Locust is not installed."
    echo "Installing Locust..."
    pip install locust
fi

echo "Starting load test..."
echo "Test configuration:"
echo "  - Host: http://localhost:8000"
echo "  - Test file: tests/locustfile.py"
echo ""
echo "Note: Access Locust UI at http://localhost:8089"
echo ""

locust -f tests/locustfile.py --host=http://localhost:8000

echo ""
echo "Load test completed."

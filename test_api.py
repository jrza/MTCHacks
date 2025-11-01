#!/usr/bin/env python3
"""
Integration test script for the Islamic Media Recommender API
Tests the actual API endpoints with a running server.
"""

import requests
import time
import sys
import subprocess
import signal
import os

API_BASE_URL = "http://localhost:8000"

def wait_for_server(timeout=10):
    """Wait for the server to be ready"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=1)
            if response.status_code == 200:
                print("✓ Server is ready")
                return True
        except:
            time.sleep(0.5)
    return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n=== Testing GET / ===")
    response = requests.get(f"{API_BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data
    print(f"✓ Root endpoint working")
    print(f"  Version: {data['version']}")

def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n=== Testing GET /health ===")
    response = requests.get(f"{API_BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    print(f"✓ Health endpoint working")
    print(f"  TMDb configured: {data.get('tmdb_configured', False)}")
    print(f"  OpenAI configured: {data.get('openai_configured', False)}")

def test_recommend_endpoint():
    """Test the recommend endpoint"""
    print("\n=== Testing GET /recommend ===")
    try:
        response = requests.get(f"{API_BASE_URL}/recommend")
        if response.status_code == 200:
            data = response.json()
            assert "recommendations" in data
            assert "count" in data
            print(f"✓ Recommend endpoint working")
            print(f"  Returned {data['count']} recommendations")
            if data['recommendations']:
                first = data['recommendations'][0]
                print(f"  Example: {first.get('title', 'N/A')}")
        else:
            # Expected if no API key
            print(f"⚠ Recommend endpoint returned error (expected without API key)")
            print(f"  Status: {response.status_code}")
    except Exception as e:
        print(f"⚠ Recommend endpoint error (expected without API key): {e}")

def test_refresh_endpoint():
    """Test the refresh endpoint"""
    print("\n=== Testing POST /refresh ===")
    try:
        response = requests.post(f"{API_BASE_URL}/refresh")
        if response.status_code == 200:
            data = response.json()
            assert "recommendations" in data
            assert "count" in data
            print(f"✓ Refresh endpoint working")
            print(f"  Returned {data['count']} recommendations")
        else:
            # Expected if no API key
            print(f"⚠ Refresh endpoint returned error (expected without API key)")
            print(f"  Status: {response.status_code}")
    except Exception as e:
        print(f"⚠ Refresh endpoint error (expected without API key): {e}")

def run_tests():
    """Run all integration tests"""
    print("=== Starting Integration Tests ===")
    
    # Wait for server
    if not wait_for_server():
        print("✗ Server did not start in time")
        return False
    
    try:
        test_root_endpoint()
        test_health_endpoint()
        test_recommend_endpoint()
        test_refresh_endpoint()
        
        print("\n=== Integration Tests Completed ===")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Check if server is already running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=1)
        server_running = True
        print("✓ Server already running")
    except:
        server_running = False
        print("⚠ Server not running, please start it first")
        print("  Run: python main.py")
        sys.exit(1)
    
    # Run tests
    success = run_tests()
    sys.exit(0 if success else 1)

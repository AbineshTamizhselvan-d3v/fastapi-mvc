#!/usr/bin/env python3
"""
Test script for FastAPI JWT Authentication System
"""
import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000/api/v1"

async def test_auth_system():
    """Test the authentication system endpoints"""
    
    async with httpx.AsyncClient() as client:
        print("🚀 Testing FastAPI JWT Authentication System\n")
        
        # Test user registration
        print("1. Testing User Registration...")
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        try:
            response = await client.post(f"{BASE_URL}/auth/register", json=register_data)
            if response.status_code == 201:
                print("✅ User registration successful")
                user_data = response.json()
                print(f"   User ID: {user_data['id']}")
                print(f"   Username: {user_data['username']}")
                print(f"   Email: {user_data['email']}")
            else:
                print(f"❌ Registration failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Registration error: {e}")
        
        print()
        
        # Test user login
        print("2. Testing User Login...")
        login_data = {
            "identifier": "testuser",
            "password": "TestPassword123"
        }
        
        try:
            response = await client.post(f"{BASE_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                print("✅ User login successful")
                token_data = response.json()
                access_token = token_data["access_token"]
                print(f"   Token Type: {token_data['token_type']}")
                print(f"   Expires In: {token_data['expires_in']} seconds")
                print(f"   Access Token: {access_token[:20]}...")
            else:
                print(f"❌ Login failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return
        except Exception as e:
            print(f"❌ Login error: {e}")
            return
        
        print()
        
        # Test protected endpoint
        print("3. Testing Protected Endpoint...")
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            response = await client.get(f"{BASE_URL}/auth/me", headers=headers)
            if response.status_code == 200:
                print("✅ Protected endpoint access successful")
                user_profile = response.json()
                print(f"   Username: {user_profile['username']}")
                print(f"   Email: {user_profile['email']}")
                print(f"   Is Active: {user_profile['is_active']}")
            else:
                print(f"❌ Protected endpoint failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Protected endpoint error: {e}")
        
        print()
        
        # Test token verification
        print("4. Testing Token Verification...")
        try:
            response = await client.get(f"{BASE_URL}/auth/verify-token", headers=headers)
            if response.status_code == 200:
                print("✅ Token verification successful")
                token_info = response.json()
                print(f"   Valid: {token_info['valid']}")
                print(f"   User ID: {token_info['user_id']}")
            else:
                print(f"❌ Token verification failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Token verification error: {e}")
        
        print("\n🎉 Authentication system test completed!")

if __name__ == "__main__":
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("Run: uvicorn app.main:app --reload\n")
    
    try:
        asyncio.run(test_auth_system())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")

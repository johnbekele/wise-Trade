#!/usr/bin/env python3
"""
Test script for wise-Trade API
Run this to test the user creation endpoint
"""

import requests
import json


url="http://localhost:8000/api"

def auth_test():
    print("=====================================")
    print("Auth test please chose test ")
    
    try:
        response = requests.get(f"{url}/auth/register")



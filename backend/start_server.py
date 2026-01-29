#!/usr/bin/env python3
"""
LIFELINE AI - Backend Startup Script
Ensures backend runs with correct configuration
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    print("🚀 Starting LIFELINE AI Backend...")
    print(f"📁 Backend directory: {backend_dir}")
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Start server with proper configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Allow external connections
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )

if __name__ == "__main__":
    main()
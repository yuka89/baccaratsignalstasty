#!/usr/bin/env python3
"""
AI Trading Assistant Launch Script
Starts the FastAPI application with proper configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import openai
        import yfinance
        import pandas
        import numpy
        import plotly
        import requests
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if environment variables are set"""
    required_vars = ["OPENAI_API_KEY"]
    optional_vars = ["ALPHA_VANTAGE_API_KEY", "POLYGON_API_KEY"]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("Please set these in your .env file")
        return False
    
    if missing_optional:
        print(f"⚠️  Optional environment variables not set: {', '.join(missing_optional)}")
        print("Some features may be limited")
    
    print("✅ Environment variables check passed")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["static/css", "static/js", "static/images", "templates"]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        if Path(".env.example").exists():
            print("⚠️  .env file not found, but .env.example exists")
            print("Please copy .env.example to .env and configure your API keys")
            return False
        else:
            print("❌ Neither .env nor .env.example file found")
            return False
    
    print("✅ .env file found")
    return True

def main():
    """Main function to launch the application"""
    print("🚀 AI Trading Assistant Launch Script")
    print("=" * 40)
    
    # Check if .env file exists
    if not check_env_file():
        print("\n❌ Environment setup incomplete")
        sys.exit(1)
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("❌ python-dotenv not installed. Please run: pip install python-dotenv")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment variables
    if not check_environment():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Launch application
    print("\n🌟 Starting AI Trading Assistant...")
    print("📱 Application will be available at: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the application")
    print("=" * 40)
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
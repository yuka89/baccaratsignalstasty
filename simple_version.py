#!/usr/bin/env python3
"""
Minimal AI Trading Assistant - Easy to run version
Just run: python simple_version.py
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import os

# Simple FastAPI app
app = FastAPI(title="AI Trading Assistant - Simple Version")

# Minimal HTML interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Trading Assistant</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            padding: 50px 0;
        }
        .container { max-width: 800px; }
        .card { border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .hero { text-align: center; color: white; margin-bottom: 30px; }
        .hero h1 { font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>🤖 AI Trading Assistant</h1>
            <p>Minimal Python Version - Working!</p>
        </div>
        
        <div class="card">
            <div class="card-body p-4">
                <h3>✅ Success! Your Python App is Running</h3>
                <div class="alert alert-success">
                    <strong>Congratulations!</strong> Your AI Trading Assistant is successfully running on Python.
                </div>
                
                <h5>Next Steps:</h5>
                <ol>
                    <li>Get API keys (OpenAI, Alpha Vantage)</li>
                    <li>Add them to your .env file</li>
                    <li>Use the full version with all features</li>
                </ol>
                
                <h5>What's Working:</h5>
                <ul>
                    <li>✅ Python FastAPI server</li>
                    <li>✅ Web interface</li>
                    <li>✅ Bootstrap styling</li>
                    <li>✅ Responsive design</li>
                </ul>
                
                <div class="mt-4">
                    <button class="btn btn-primary" onclick="testFeature()">Test Button</button>
                    <button class="btn btn-success" onclick="showAlert()">Show Alert</button>
                </div>
                
                <div id="output" class="mt-3"></div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function testFeature() {
            document.getElementById('output').innerHTML = 
                '<div class="alert alert-info">✅ JavaScript is working! You can now add API integrations.</div>';
        }
        
        function showAlert() {
            alert('🎉 Everything is working perfectly! You can now build the full trading assistant.');
        }
        
        console.log('🚀 AI Trading Assistant loaded successfully!');
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    """Main page - shows the minimal interface"""
    return HTML_TEMPLATE

@app.get("/test")
async def test():
    """Test endpoint to verify the API is working"""
    return {"status": "success", "message": "API is working!", "app": "AI Trading Assistant"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "python_version": "working"}

if __name__ == "__main__":
    print("🚀 Starting AI Trading Assistant...")
    print("📱 Open your browser to: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
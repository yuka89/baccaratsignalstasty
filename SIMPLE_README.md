# AI Trading Assistant - Minimal Version

## Super Simple Setup (3 Steps)

### 1. Install Python Dependencies
```bash
pip install fastapi uvicorn
```

### 2. Download the File
Save the `simple_version.py` file to your computer.

### 3. Run the App
```bash
python simple_version.py
```

### 4. Open Your Browser
Go to: `http://localhost:8000`

## That's It! 🎉

If you see the webpage with "Success! Your Python App is Running", you're all set!

## Next Steps

Once this works, you can:
1. Get API keys (OpenAI, Alpha Vantage)
2. Use the full version with all features
3. Add real trading data and AI analysis

## Troubleshooting

### "Python not found"
- Install Python from [python.org](https://python.org)
- Make sure to check "Add Python to PATH"

### "Module not found"
```bash
pip install fastapi uvicorn
```

### "Port already in use"
Change the port in the last line of `simple_version.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change 8000 to 8001
```

## Commands to Copy-Paste

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the app
python simple_version.py

# Alternative (if python doesn't work)
python3 simple_version.py
```

That's all you need! 🚀
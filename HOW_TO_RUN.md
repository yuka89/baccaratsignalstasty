# How to Run AI Trading Assistant in Python 🐍

## 🚀 EASIEST WAY (Recommended for beginners)

### 1. Install Python
- Go to [python.org](https://python.org) and download Python 3.8+
- ✅ Make sure to check "Add Python to PATH" during installation

### 2. Install Dependencies
```bash
pip install fastapi uvicorn
```

### 3. Run the Minimal Version
```bash
python simple_version.py
```

### 4. Open Browser
Go to: `http://localhost:8000`

**✅ If you see "Success! Your Python App is Running" - you're done!**

---

## 🔧 FULL VERSION (With all features)

### 1. Install All Dependencies
```bash
pip install fastapi uvicorn python-multipart jinja2 python-dotenv openai requests pandas numpy plotly yfinance alpha-vantage pillow
```

### 2. Get API Keys
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Alpha Vantage**: [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

### 3. Create .env File
```bash
# Create .env file with your API keys
OPENAI_API_KEY=your_openai_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

### 4. Run Full Version
```bash
python main.py
```

---

## 📁 Files You Need

**For Minimal Version:**
- `simple_version.py` (I created this for you)
- `SIMPLE_README.md` (Instructions)

**For Full Version:**
- `main.py` (Complete application)
- `requirements.txt` (All dependencies)
- `run.py` (Launcher script)
- `.env` (Your API keys)
- `templates/index.html` (Web interface)
- `static/css/style.css` (Styling)
- `static/js/app.js` (JavaScript)

---

## 🎯 Quick Start Scripts

### Windows Users
Double-click: `run_simple.bat`

### Linux/Mac Users
```bash
bash run_simple.sh
```

---

## 🛠️ Common Issues

### "Python not found"
- Install Python from [python.org](https://python.org)
- Restart your terminal/command prompt

### "Module not found"
```bash
pip install fastapi uvicorn
```

### "Port already in use"
- Change port in the code from 8000 to 8001
- Or kill the process using the port

### "API key errors"
- Check `.env` file exists
- Verify API keys are correct
- No extra spaces in the keys

---

## 📝 Step-by-Step Video Guide

1. **Install Python** (2 minutes)
2. **Open terminal/command prompt** (30 seconds)
3. **Type: `pip install fastapi uvicorn`** (1 minute)
4. **Type: `python simple_version.py`** (30 seconds)
5. **Open browser to localhost:8000** (30 seconds)

**Total time: 5 minutes** ⏱️

---

## 🎉 What You'll Get

**Minimal Version:**
- ✅ Working Python web app
- ✅ Beautiful interface
- ✅ Ready for API integration

**Full Version:**
- ✅ AI chart analysis
- ✅ Market data (NASDAQ, S&P 500)
- ✅ Trading signals
- ✅ Real-time prices
- ✅ Interactive charts

---

## 📞 Need Help?

1. **First**: Try the minimal version
2. **If that works**: Upgrade to full version
3. **If stuck**: Check common issues above

**Remember**: Start with the minimal version first! 🚀
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import json
import base64
import io
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import openai
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import requests
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Trading Assistant",
    description="Advanced AI-powered trading analysis platform with chart upload and market insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize API clients
openai.api_key = os.getenv("OPENAI_API_KEY")
alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
polygon_key = os.getenv("POLYGON_API_KEY")

# Global variables for market data
nasdaq_100_symbols = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "AVGO", "ASML", "COST",
    "NFLX", "TMUS", "CSCO", "ADBE", "PEP", "LIN", "TXN", "QCOM", "CMCSA", "INTU",
    "AMGN", "HON", "AMAT", "BKNG", "ADP", "VRTX", "SBUX", "GILD", "ADI", "MELI",
    "LRCX", "MDLZ", "REGN", "ISRG", "PYPL", "KLAC", "SNPS", "CDNS", "CRWD", "MAR",
    "MRVL", "ORLY", "FTNT", "CSX", "DASH", "ADSK", "ABNB", "CHTR", "WDAY", "NXPI"
]

sp500_symbols = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK.B", "UNH", "JNJ",
    "V", "PG", "JPM", "MA", "HD", "CVX", "LLY", "ABBV", "AVGO", "PFE", "KO", "MRK",
    "COST", "PEP", "TMO", "WMT", "BAC", "ASML", "NFLX", "CRM", "ACN", "LIN", "CSCO",
    "ABT", "ADBE", "NKE", "MCD", "DIS", "TXN", "VZ", "CMCSA", "QCOM", "PM", "DHR",
    "INTC", "T", "UPS", "AMGN", "HON", "COP", "LOW", "SPGI", "RTX", "INTU", "NOW"
]

# Data models
class MarketQuestion(BaseModel):
    question: str
    context: Optional[str] = None
    symbol: Optional[str] = None

class ChartAnalysis(BaseModel):
    symbol: str
    timeframe: str
    analysis_type: str

class TradingSignal(BaseModel):
    symbol: str
    signal_type: str
    confidence: float
    reasoning: str
    entry_price: float
    stop_loss: float
    take_profit: float

# Market data functions
def get_market_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """Get market data using yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

def get_alpha_vantage_data(symbol: str, function: str = "TIME_SERIES_DAILY"):
    """Get data from Alpha Vantage API"""
    try:
        if not alpha_vantage_key:
            return None
        
        ts = TimeSeries(key=alpha_vantage_key, output_format='pandas')
        
        if function == "TIME_SERIES_DAILY":
            data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        elif function == "TIME_SERIES_INTRADAY":
            data, meta_data = ts.get_intraday(symbol=symbol, interval='5min', outputsize='full')
        
        return data
    except Exception as e:
        print(f"Error fetching Alpha Vantage data: {e}")
        return None

def get_polygon_data(symbol: str):
    """Get data from Polygon.io API"""
    try:
        if not polygon_key:
            return None
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
        params = {"apikey": polygon_key}
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') == 'OK':
            return data['results']
        return None
    except Exception as e:
        print(f"Error fetching Polygon data: {e}")
        return None

def analyze_chart_with_ai(image_data: bytes, symbol: str, question: str) -> str:
    """Analyze uploaded chart image using OpenAI Vision API"""
    try:
        # Encode image to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Get current market data for context
        market_data = get_market_data(symbol)
        current_price = market_data['Close'].iloc[-1] if not market_data.empty else "N/A"
        
        # Create prompt for AI analysis
        prompt = f"""
        You are a professional trading analyst with expertise in technical analysis, futures trading, 
        and market analysis. You have deep knowledge of NASDAQ 100 and S&P 500 stocks.
        
        Analyze this chart image for {symbol} and answer the following question: {question}
        
        Current market context:
        - Symbol: {symbol}
        - Current price: {current_price}
        - Chart uploaded by user for analysis
        
        Please provide:
        1. Technical analysis of the chart patterns
        2. Support and resistance levels if visible
        3. Trend analysis
        4. Trading signals and recommendations
        5. Risk assessment
        6. Future price predictions based on the chart
        
        Be specific and actionable in your response.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing chart: {str(e)}"

def answer_market_question(question: str, context: str = None, symbol: str = None) -> str:
    """Answer market questions using OpenAI with extensive trading knowledge"""
    try:
        # Get market data if symbol provided
        market_context = ""
        if symbol:
            data = get_market_data(symbol)
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
                percent_change = (price_change / data['Close'].iloc[-2]) * 100
                volume = data['Volume'].iloc[-1]
                
                market_context = f"""
                Current market data for {symbol}:
                - Current price: ${current_price:.2f}
                - Price change: ${price_change:.2f} ({percent_change:.2f}%)
                - Volume: {volume:,}
                - 52-week high: ${data['High'].max():.2f}
                - 52-week low: ${data['Low'].min():.2f}
                """
        
        # Create comprehensive prompt
        prompt = f"""
        You are an expert trading analyst with comprehensive knowledge of:
        - Technical analysis and chart patterns
        - Fundamental analysis
        - Futures trading (commodities, indices, currencies)
        - Options trading strategies
        - Risk management
        - Market psychology and sentiment
        - NASDAQ 100 companies and sectors
        - S&P 500 components and analysis
        - Global markets and economic indicators
        - Trading strategies (day trading, swing trading, position trading)
        - Market microstructure and liquidity
        
        Question: {question}
        
        {market_context}
        
        Additional context: {context if context else "None provided"}
        
        Please provide a comprehensive, professional response that includes:
        1. Direct answer to the question
        2. Relevant market analysis
        3. Trading implications
        4. Risk considerations
        5. Actionable insights
        
        Be specific, accurate, and provide practical trading advice.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a world-class trading expert with deep knowledge of financial markets, 
                    technical analysis, futures trading, and comprehensive understanding of NASDAQ 100 and S&P 500. 
                    You provide accurate, actionable trading advice and market insights."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error processing question: {str(e)}"

def generate_trading_signals(symbol: str) -> List[TradingSignal]:
    """Generate AI-powered trading signals"""
    try:
        data = get_market_data(symbol, period="3mo")
        if data.empty:
            return []
        
        # Calculate technical indicators
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['RSI'] = calculate_rsi(data['Close'])
        data['MACD'] = calculate_macd(data['Close'])
        
        # Generate signals using AI
        current_price = data['Close'].iloc[-1]
        sma_20 = data['SMA_20'].iloc[-1]
        sma_50 = data['SMA_50'].iloc[-1]
        rsi = data['RSI'].iloc[-1]
        
        # Create analysis prompt
        prompt = f"""
        Analyze the following technical data for {symbol} and generate trading signals:
        
        Current Price: ${current_price:.2f}
        20-day SMA: ${sma_20:.2f}
        50-day SMA: ${sma_50:.2f}
        RSI: {rsi:.2f}
        
        Volume trend: {"Increasing" if data['Volume'].iloc[-1] > data['Volume'].iloc[-5:].mean() else "Decreasing"}
        
        Generate 2-3 specific trading signals with entry points, stop losses, and take profits.
        Consider both bullish and bearish scenarios.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional trading signal generator. Provide specific, actionable trading signals with precise entry/exit points."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000
        )
        
        # Parse response and create signals (simplified)
        signals = []
        signal_text = response.choices[0].message.content
        
        # Create sample signals (in real implementation, parse AI response)
        if rsi < 30:
            signals.append(TradingSignal(
                symbol=symbol,
                signal_type="BUY",
                confidence=0.75,
                reasoning="RSI oversold, potential reversal",
                entry_price=current_price,
                stop_loss=current_price * 0.95,
                take_profit=current_price * 1.1
            ))
        
        if rsi > 70:
            signals.append(TradingSignal(
                symbol=symbol,
                signal_type="SELL",
                confidence=0.8,
                reasoning="RSI overbought, potential correction",
                entry_price=current_price,
                stop_loss=current_price * 1.05,
                take_profit=current_price * 0.9
            ))
        
        return signals
        
    except Exception as e:
        print(f"Error generating signals: {e}")
        return []

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
    """Calculate MACD indicator"""
    exp1 = prices.ewm(span=fast).mean()
    exp2 = prices.ewm(span=slow).mean()
    macd = exp1 - exp2
    return macd

def create_interactive_chart(symbol: str, data: pd.DataFrame) -> str:
    """Create interactive chart using Plotly"""
    try:
        fig = go.Figure()
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=symbol
        ))
        
        # Add volume
        fig.add_trace(go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            yaxis='y2',
            opacity=0.3
        ))
        
        # Add moving averages
        if len(data) >= 20:
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA_20'],
                name='20-day SMA',
                line=dict(color='orange', width=2)
            ))
        
        if len(data) >= 50:
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA_50'],
                name='50-day SMA',
                line=dict(color='blue', width=2)
            ))
        
        fig.update_layout(
            title=f'{symbol} Stock Chart',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            yaxis2=dict(
                title='Volume',
                overlaying='y',
                side='right',
                range=[0, data['Volume'].max() * 4]
            ),
            height=600,
            showlegend=True,
            xaxis_rangeslider_visible=False
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
        
    except Exception as e:
        print(f"Error creating chart: {e}")
        return "{}"

# API Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-chart")
async def upload_chart(
    file: UploadFile = File(...),
    symbol: str = Form(...),
    question: str = Form(...)
):
    """Upload and analyze chart image"""
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        
        # Analyze with AI
        analysis = analyze_chart_with_ai(image_data, symbol, question)
        
        return JSONResponse({
            "success": True,
            "analysis": analysis,
            "symbol": symbol,
            "question": question
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask-question")
async def ask_question(question: MarketQuestion):
    """Ask market-related questions"""
    try:
        answer = answer_market_question(
            question.question,
            question.context,
            question.symbol
        )
        
        return JSONResponse({
            "success": True,
            "answer": answer,
            "question": question.question
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-data/{symbol}")
async def get_market_data_api(symbol: str, period: str = "1y"):
    """Get market data for a symbol"""
    try:
        data = get_market_data(symbol, period)
        
        if data.empty:
            raise HTTPException(status_code=404, detail="No data found for symbol")
        
        # Convert to JSON-serializable format
        result = {
            "symbol": symbol,
            "period": period,
            "data": data.reset_index().to_dict(orient='records'),
            "current_price": float(data['Close'].iloc[-1]),
            "price_change": float(data['Close'].iloc[-1] - data['Close'].iloc[-2]),
            "percent_change": float(((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100)
        }
        
        return JSONResponse(result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chart/{symbol}")
async def get_chart(symbol: str, period: str = "1y"):
    """Get interactive chart for a symbol"""
    try:
        data = get_market_data(symbol, period)
        
        if data.empty:
            raise HTTPException(status_code=404, detail="No data found for symbol")
        
        chart_json = create_interactive_chart(symbol, data)
        
        return JSONResponse({
            "success": True,
            "chart": chart_json,
            "symbol": symbol
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trading-signals/{symbol}")
async def get_trading_signals(symbol: str):
    """Get AI-generated trading signals"""
    try:
        signals = generate_trading_signals(symbol)
        
        return JSONResponse({
            "success": True,
            "signals": [signal.dict() for signal in signals],
            "symbol": symbol
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nasdaq100")
async def get_nasdaq100():
    """Get NASDAQ 100 symbols and data"""
    try:
        results = []
        for symbol in nasdaq_100_symbols[:10]:  # Limit to first 10 for demo
            data = get_market_data(symbol, period="1d")
            if not data.empty:
                results.append({
                    "symbol": symbol,
                    "price": float(data['Close'].iloc[-1]),
                    "change": float(data['Close'].iloc[-1] - data['Close'].iloc[-2]) if len(data) > 1 else 0,
                    "volume": int(data['Volume'].iloc[-1])
                })
        
        return JSONResponse({
            "success": True,
            "data": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sp500")
async def get_sp500():
    """Get S&P 500 symbols and data"""
    try:
        results = []
        for symbol in sp500_symbols[:10]:  # Limit to first 10 for demo
            data = get_market_data(symbol, period="1d")
            if not data.empty:
                results.append({
                    "symbol": symbol,
                    "price": float(data['Close'].iloc[-1]),
                    "change": float(data['Close'].iloc[-1] - data['Close'].iloc[-2]) if len(data) > 1 else 0,
                    "volume": int(data['Volume'].iloc[-1])
                })
        
        return JSONResponse({
            "success": True,
            "data": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
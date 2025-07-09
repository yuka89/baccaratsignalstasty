# AI Trading Assistant 🤖📈

A comprehensive AI-powered trading analysis platform that allows users to upload charts, ask market questions, and get intelligent insights about trading markets, futures, NASDAQ 100, and S&P 500 stocks.

## Features 🚀

### Core Functionality
- **Chart Upload & Analysis**: Upload stock charts and get AI-powered technical analysis
- **Market Q&A**: Ask questions about trading, futures, market sentiment, and get expert-level responses
- **Real-time Data**: Live market data for NASDAQ 100 and S&P 500 stocks
- **Interactive Charts**: Dynamic, interactive stock charts with technical indicators
- **Trading Signals**: AI-generated trading signals with entry/exit points
- **Comprehensive Knowledge Base**: Deep understanding of trading strategies, market dynamics, and financial instruments

### AI Capabilities
- **Advanced Vision Analysis**: Analyzes uploaded chart images using OpenAI's GPT-4 Vision
- **Expert Market Knowledge**: Comprehensive understanding of:
  - Technical analysis and chart patterns
  - Futures trading (commodities, indices, currencies)
  - NASDAQ 100 and S&P 500 analysis
  - Market sentiment and psychology
  - Risk management strategies
  - Options trading
  - Market microstructure

### Market Data Integration
- **Multiple Data Sources**: Alpha Vantage, Polygon.io, Yahoo Finance
- **Real-time Updates**: Live price feeds and market data
- **Historical Analysis**: Access to historical price data and trends
- **Technical Indicators**: RSI, MACD, Moving Averages, and more

## Quick Start 🏃‍♂️

### Prerequisites
- Python 3.8+
- Modern web browser
- API keys for market data and AI services

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-trading-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8000`

## API Keys Setup 🔑

### Required API Keys

#### OpenAI API Key
- **Purpose**: AI chart analysis and market questions
- **How to get**: 
  1. Go to [OpenAI API](https://openai.com/api/)
  2. Create account and get API key
  3. Add to `.env` as `OPENAI_API_KEY`

#### Alpha Vantage API Key
- **Purpose**: Stock market data and indicators
- **How to get**:
  1. Visit [Alpha Vantage](https://www.alphavantage.co/)
  2. Sign up for free API key
  3. Add to `.env` as `ALPHA_VANTAGE_API_KEY`

#### Polygon.io API Key (Optional)
- **Purpose**: Real-time market data
- **How to get**:
  1. Go to [Polygon.io](https://polygon.io/)
  2. Create account and get API key
  3. Add to `.env` as `POLYGON_API_KEY`

## Usage Guide 📖

### 1. Chart Analysis
- Upload any stock chart image (PNG, JPG, JPEG)
- Enter the stock symbol
- Ask specific questions about the chart
- Get detailed AI analysis including:
  - Technical patterns
  - Support/resistance levels
  - Trend analysis
  - Trading recommendations

### 2. Market Questions
Ask questions like:
- "What are the best S&P 500 sectors to watch right now?"
- "Explain futures trading basics and key strategies"
- "How do I analyze market sentiment and volatility?"
- "What are the top performing NASDAQ 100 stocks this week?"

### 3. Live Market Data
- View real-time prices for NASDAQ 100 and S&P 500
- Monitor price changes and volume
- Track market movements

### 4. Interactive Charts
- Select from major stocks (AAPL, MSFT, GOOGL, etc.)
- Choose time periods (1 month to 2 years)
- View candlestick charts with technical indicators
- Zoom, pan, and explore data

### 5. Trading Signals
- Enter any stock symbol
- Get AI-generated trading signals
- View entry points, stop losses, and take profits
- See confidence levels and reasoning

## Technical Architecture 🏗️

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **AI Integration**: OpenAI GPT-4 Vision and Chat APIs
- **Data Sources**: Multiple market data providers
- **Real-time Processing**: WebSocket support for live updates
- **Technical Analysis**: Custom indicators and signal generation

### Frontend (HTML/CSS/JavaScript)
- **Design**: Modern, responsive UI with Bootstrap 5
- **Charts**: Interactive charts with Plotly.js
- **Real-time Updates**: Live market data feeds
- **File Upload**: Drag & drop chart upload
- **Chat Interface**: AI-powered Q&A system

### Data Flow
1. **Chart Upload**: Image → OpenAI Vision API → AI Analysis
2. **Market Questions**: User Query → OpenAI Chat API → Expert Response
3. **Market Data**: API Calls → Data Processing → Real-time Display
4. **Trading Signals**: Technical Analysis → AI Evaluation → Signal Generation

## API Endpoints 📊

### Core Endpoints
- `GET /` - Main application page
- `POST /upload-chart` - Analyze uploaded chart
- `POST /ask-question` - Ask market questions
- `GET /market-data/{symbol}` - Get market data
- `GET /chart/{symbol}` - Get interactive chart
- `GET /trading-signals/{symbol}` - Get trading signals

### Market Data Endpoints
- `GET /nasdaq100` - NASDAQ 100 data
- `GET /sp500` - S&P 500 data
- `GET /health` - Health check

## Configuration Options ⚙️

### Environment Variables
```env
# Required
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key

# Optional
POLYGON_API_KEY=your_polygon_key
TWELVE_DATA_API_KEY=your_twelve_data_key
FMP_API_KEY=your_fmp_key

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT=100
```

### Feature Flags
- `ENABLE_CHART_ANALYSIS` - Enable/disable chart upload
- `ENABLE_TRADING_SIGNALS` - Enable/disable signal generation
- `ENABLE_MARKET_DATA` - Enable/disable live data
- `ENABLE_AI_CHAT` - Enable/disable AI chat

## Security & Best Practices 🔒

### API Key Security
- Never commit API keys to version control
- Use environment variables for all sensitive data
- Implement rate limiting to prevent abuse
- Monitor API usage and costs

### Data Privacy
- No user data is permanently stored
- Images are processed in memory only
- Chat conversations are not logged
- All API calls are encrypted

### Performance
- Caching for frequently requested data
- Async processing for better performance
- Rate limiting to prevent overload
- Error handling and graceful degradation

## Troubleshooting 🔧

### Common Issues

1. **API Key Errors**
   - Check if API keys are correctly set in `.env`
   - Verify API key validity and quotas
   - Ensure proper environment variable loading

2. **Market Data Issues**
   - Verify internet connection
   - Check API quotas and limits
   - Try different data sources

3. **Chart Upload Problems**
   - Ensure image file is supported format
   - Check file size limits
   - Verify OpenAI API key is valid

4. **Performance Issues**
   - Check network connectivity
   - Monitor API response times
   - Consider upgrading API plans

### Debug Mode
Enable debug mode for detailed error information:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📝

This project is for educational purposes only. Please consult with a financial advisor before making investment decisions.

## Disclaimer ⚠️

This application is for educational and informational purposes only. It does not constitute financial advice. Always do your own research and consult with qualified financial professionals before making investment decisions.

## Support 💬

For issues, questions, or contributions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

## Roadmap 🗺️

### Upcoming Features
- [ ] Portfolio tracking
- [ ] Alert system
- [ ] Mobile app
- [ ] Advanced charting tools
- [ ] Backtesting capabilities
- [ ] Social features
- [ ] News sentiment analysis
- [ ] Crypto support

### Version History
- **v1.0.0** - Initial release with core features
- **v1.1.0** - Enhanced AI capabilities (planned)
- **v1.2.0** - Portfolio management (planned)

---

**Built with ❤️ for traders and investors**

*Powered by OpenAI, Alpha Vantage, and modern web technologies*
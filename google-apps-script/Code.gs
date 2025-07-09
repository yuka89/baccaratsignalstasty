// AI Trading Assistant - Google Apps Script Version
// Limited functionality due to platform constraints

// Configuration
const OPENAI_API_KEY = 'your_openai_api_key_here';
const ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key_here';

// Main function to serve the web app
function doGet() {
  return HtmlService.createTemplateFromFile('index')
    .evaluate()
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .setTitle('AI Trading Assistant');
}

// Include HTML templates
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

// Market data functions
function getStockPrice(symbol) {
  try {
    const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${ALPHA_VANTAGE_API_KEY}`;
    const response = UrlFetchApp.fetch(url);
    const data = JSON.parse(response.getContentText());
    
    if (data['Global Quote']) {
      const quote = data['Global Quote'];
      return {
        symbol: quote['01. symbol'],
        price: parseFloat(quote['05. price']),
        change: parseFloat(quote['09. change']),
        changePercent: quote['10. change percent'],
        volume: parseInt(quote['06. volume']),
        timestamp: new Date().toISOString()
      };
    }
    
    return { error: 'No data found for symbol' };
  } catch (error) {
    console.error('Error fetching stock price:', error);
    return { error: error.toString() };
  }
}

// Get multiple stock prices
function getMultipleStocks(symbols) {
  const results = [];
  
  // Due to API rate limits, we'll limit to 5 stocks
  const limitedSymbols = symbols.slice(0, 5);
  
  for (const symbol of limitedSymbols) {
    const data = getStockPrice(symbol);
    if (!data.error) {
      results.push(data);
    }
    // Add delay to respect API rate limits
    Utilities.sleep(1000);
  }
  
  return results;
}

// NASDAQ 100 top stocks (limited list)
function getNasdaq100Data() {
  const nasdaq100Symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'];
  return getMultipleStocks(nasdaq100Symbols);
}

// S&P 500 top stocks (limited list)
function getSP500Data() {
  const sp500Symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'];
  return getMultipleStocks(sp500Symbols);
}

// AI-powered market question answering
function askMarketQuestion(question, symbol = null) {
  try {
    let context = '';
    
    // Get market data context if symbol provided
    if (symbol) {
      const stockData = getStockPrice(symbol);
      if (!stockData.error) {
        context = `Current market data for ${symbol}:
- Price: $${stockData.price}
- Change: ${stockData.change} (${stockData.changePercent})
- Volume: ${stockData.volume}`;
      }
    }
    
    const prompt = `You are an expert trading analyst with comprehensive knowledge of:
- Technical analysis and chart patterns
- Fundamental analysis
- Futures trading (commodities, indices, currencies)
- Options trading strategies
- Risk management
- Market psychology and sentiment
- NASDAQ 100 companies and sectors
- S&P 500 components and analysis
- Global markets and economic indicators

Question: ${question}

${context}

Please provide a comprehensive, professional response that includes:
1. Direct answer to the question
2. Relevant market analysis
3. Trading implications
4. Risk considerations
5. Actionable insights

Be specific, accurate, and provide practical trading advice.`;

    const response = callOpenAI(prompt);
    return response;
    
  } catch (error) {
    console.error('Error answering market question:', error);
    return 'Error processing your question. Please try again.';
  }
}

// OpenAI API call
function callOpenAI(prompt) {
  try {
    const url = 'https://api.openai.com/v1/chat/completions';
    
    const payload = {
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are a world-class trading expert with deep knowledge of financial markets, technical analysis, futures trading, and comprehensive understanding of NASDAQ 100 and S&P 500. You provide accurate, actionable trading advice and market insights.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      max_tokens: 1500,
      temperature: 0.7
    };
    
    const options = {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(payload)
    };
    
    const response = UrlFetchApp.fetch(url, options);
    const data = JSON.parse(response.getContentText());
    
    if (data.choices && data.choices[0]) {
      return data.choices[0].message.content;
    }
    
    return 'Unable to get response from AI assistant.';
    
  } catch (error) {
    console.error('Error calling OpenAI:', error);
    return 'Error connecting to AI assistant. Please check your API key.';
  }
}

// Generate basic trading signals
function getTradingSignals(symbol) {
  try {
    const stockData = getStockPrice(symbol);
    
    if (stockData.error) {
      return { error: stockData.error };
    }
    
    // Simple signal generation based on price change
    const signals = [];
    const changePercent = parseFloat(stockData.changePercent.replace('%', ''));
    
    if (changePercent < -3) {
      signals.push({
        type: 'BUY',
        confidence: 0.7,
        reasoning: 'Stock down significantly, potential oversold condition',
        entryPrice: stockData.price,
        stopLoss: stockData.price * 0.95,
        takeProfit: stockData.price * 1.1
      });
    } else if (changePercent > 3) {
      signals.push({
        type: 'SELL',
        confidence: 0.65,
        reasoning: 'Stock up significantly, potential overbought condition',
        entryPrice: stockData.price,
        stopLoss: stockData.price * 1.05,
        takeProfit: stockData.price * 0.9
      });
    } else {
      signals.push({
        type: 'HOLD',
        confidence: 0.5,
        reasoning: 'No strong signals detected, monitor for changes',
        entryPrice: stockData.price,
        stopLoss: stockData.price * 0.95,
        takeProfit: stockData.price * 1.05
      });
    }
    
    return {
      symbol: symbol,
      signals: signals,
      marketData: stockData
    };
    
  } catch (error) {
    console.error('Error generating trading signals:', error);
    return { error: error.toString() };
  }
}

// Utility function to format currency
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}

// Test function
function testApp() {
  console.log('Testing AI Trading Assistant...');
  
  // Test stock price
  const appleData = getStockPrice('AAPL');
  console.log('Apple stock data:', appleData);
  
  // Test AI question
  const aiResponse = askMarketQuestion('What are the key factors to consider when trading NASDAQ 100 stocks?');
  console.log('AI Response:', aiResponse);
  
  // Test trading signals
  const signals = getTradingSignals('AAPL');
  console.log('Trading signals:', signals);
}
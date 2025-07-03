/**
 * Trading Emotion Control App
 * Google Apps Script application to help traders manage emotions
 */

// Global configuration
const SHEET_NAME_EMOTIONS = 'TradingEmotions';
const SHEET_NAME_TRADES = 'TradeResults';
const SPREADSHEET_ID = ''; // Set this to your Google Sheets ID

/**
 * Initialize the web app
 */
function doGet() {
  return HtmlService.createTemplateFromFile('index')
    .evaluate()
    .setTitle('Trading Emotion Control')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Include HTML partials
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

/**
 * Initialize spreadsheet for data storage
 */
function initializeSpreadsheet() {
  try {
    let ss;
    if (SPREADSHEET_ID) {
      ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    } else {
      ss = SpreadsheetApp.create('Trading Emotions & Performance Data');
      Logger.log('Created new spreadsheet: ' + ss.getId());
    }
    
    // Initialize Emotions sheet
    let emotionsSheet = ss.getSheetByName(SHEET_NAME_EMOTIONS);
    if (!emotionsSheet) {
      emotionsSheet = ss.insertSheet(SHEET_NAME_EMOTIONS);
    }
    
    // Check if sheet has any data, handle empty sheet case
    const lastCol = emotionsSheet.getLastColumn();
    let emotionsHeaders = [];
    if (lastCol > 0) {
      emotionsHeaders = emotionsSheet.getRange(1, 1, 1, lastCol).getValues()[0];
    }
    
    if (emotionsHeaders.length === 0 || emotionsHeaders[0] === '') {
      emotionsSheet.getRange(1, 1, 1, 8).setValues([[
        'Timestamp', 'Emotion Score', 'Market Action', 'Confidence Level', 
        'Fear Level', 'Greed Level', 'Notes', 'Reflection'
      ]]);
    }
    
    // Initialize Trades sheet
    let tradesSheet = ss.getSheetByName(SHEET_NAME_TRADES);
    if (!tradesSheet) {
      tradesSheet = ss.insertSheet(SHEET_NAME_TRADES);
    }
    
    // Check if sheet has any data, handle empty sheet case
    const tradesLastCol = tradesSheet.getLastColumn();
    let tradesHeaders = [];
    if (tradesLastCol > 0) {
      tradesHeaders = tradesSheet.getRange(1, 1, 1, tradesLastCol).getValues()[0];
    }
    
    if (tradesHeaders.length === 0 || tradesHeaders[0] === '') {
      tradesSheet.getRange(1, 1, 1, 13).setValues([[
        'Timestamp', 'Symbol', 'Trade Type', 'Entry Price', 'Exit Price', 
        'Contracts', 'Result', 'Profit/Loss', 'Current Balance', 'Trade Notes', 
        'Chart Image ID', 'Emotion Score', 'Confidence Level'
      ]]);
    }
    
    return { emotions: emotionsSheet, trades: tradesSheet };
  } catch (error) {
    Logger.log('Error initializing spreadsheet: ' + error.toString());
    throw error;
  }
}

/**
 * Get emotions sheet only (for backward compatibility)
 */
function getEmotionsSheet() {
  const sheets = initializeSpreadsheet();
  return sheets.emotions;
}

/**
 * Record emotional state and trading decision
 */
function recordEmotionalState(data) {
  try {
    Logger.log('Recording emotional state: ' + JSON.stringify(data));
    
    const sheet = getEmotionsSheet();
    const timestamp = new Date();
    
    const rowData = [
      timestamp,
      data.emotionScore || 5,
      data.marketAction || 'Hold',
      data.confidenceLevel || 5,
      data.fearLevel || 5,
      data.greedLevel || 5,
      data.notes || '',
      data.reflection || ''
    ];
    
    Logger.log('Appending row data: ' + JSON.stringify(rowData));
    
    sheet.appendRow(rowData);
    
    Logger.log('Emotional state recorded successfully');
    
    return { success: true, message: 'Emotional state recorded successfully' };
  } catch (error) {
    Logger.log('Error recording emotional state: ' + error.toString());
    Logger.log('Error stack: ' + error.stack);
    return { success: false, message: error.toString() };
  }
}

/**
 * Record trade result with performance data
 */
function recordTrade(tradeData) {
  try {
    Logger.log('Recording trade data: ' + JSON.stringify(tradeData));
    
    const sheets = initializeSpreadsheet();
    const sheet = sheets.trades;
    
    // Calculate profit/loss based on futures contract specifications
    let profitLoss = 0;
    if (tradeData.entryPrice && tradeData.exitPrice && tradeData.quantity) {
      const entryPrice = parseFloat(tradeData.entryPrice);
      const exitPrice = parseFloat(tradeData.exitPrice);
      const quantity = parseFloat(tradeData.quantity);
      
      // Get point value for different futures contracts
      const pointValue = getContractPointValue(tradeData.symbol);
      
      if (tradeData.tradeType === 'Long') {
        profitLoss = (exitPrice - entryPrice) * quantity * pointValue;
      } else {
        profitLoss = (entryPrice - exitPrice) * quantity * pointValue;
      }
    }
    
    sheet.appendRow([
      new Date(),
      tradeData.symbol || '',
      tradeData.tradeType || 'Long',
      tradeData.entryPrice || '',
      tradeData.exitPrice || '',
      tradeData.quantity || 1,
      tradeData.result || 'Win',
      profitLoss.toFixed(2),
      tradeData.currentBalance || '',
      tradeData.tradeNotes || '',
      '', // Chart Image ID - removed
      tradeData.emotionScore || 5,
      tradeData.confidenceLevel || 5
    ]);
    
    Logger.log('Trade recorded successfully');
    
    return { 
      success: true, 
      message: 'Trade recorded successfully', 
      profitLoss: profitLoss.toFixed(2)
    };
  } catch (error) {
    Logger.log('Error recording trade: ' + error.toString());
    return { success: false, message: error.toString() };
  }
}

/**
 * Get point value for different futures contracts
 */
function getContractPointValue(symbol) {
  const pointValues = {
    // Stock Index Futures
    'ES': 50,      // E-mini S&P 500
    'MES': 5,      // Micro E-mini S&P 500
    'NQ': 20,      // E-mini NASDAQ 100
    'MNQ': 2,      // Micro E-mini NASDAQ 100
    'YM': 5,       // E-mini Dow Jones
    'MYM': 0.5,    // Micro E-mini Dow Jones
    'RTY': 50,     // E-mini Russell 2000
    'M2K': 5,      // Micro E-mini Russell 2000
    
    // Energy Futures
    'CL': 1000,    // Crude Oil (1000 barrels)
    'MCL': 100,    // Micro Crude Oil
    'NG': 10000,   // Natural Gas (10,000 MMBtu)
    'RB': 42000,   // Gasoline (42,000 gallons)
    'HO': 42000,   // Heating Oil (42,000 gallons)
    
    // Metal Futures
    'GC': 100,     // Gold (100 troy ounces)
    'MGC': 10,     // Micro Gold
    'SI': 5000,    // Silver (5,000 troy ounces)
    'SIL': 1000,   // Micro Silver
    'HG': 25000,   // Copper (25,000 pounds)
    'PA': 100,     // Palladium
    'PL': 50,      // Platinum
    
    // Currency Futures
    '6E': 125000,  // Euro FX
    'M6E': 12500,  // Micro Euro FX
    '6B': 62500,   // British Pound
    'M6B': 6250,   // Micro British Pound
    '6J': 12500000, // Japanese Yen
    '6A': 100000,  // Australian Dollar
    '6C': 100000,  // Canadian Dollar
    '6S': 125000,  // Swiss Franc
    
    // Agricultural Futures
    'ZC': 50,      // Corn (5,000 bushels, $0.01 = $50)
    'ZS': 50,      // Soybeans (5,000 bushels, $0.01 = $50)
    'ZW': 50,      // Wheat (5,000 bushels, $0.01 = $50)
    'LE': 400,     // Live Cattle (40,000 pounds, $0.01 = $400)
    'HE': 400,     // Lean Hogs (40,000 pounds, $0.01 = $400)
    'CC': 10,      // Cocoa
    'KC': 375,     // Coffee
    'SB': 1120,    // Sugar
    'CT': 500,     // Cotton
    
    // Bond Futures
    'ZB': 1000,    // 30-Year T-Bond
    'ZN': 1000,    // 10-Year T-Note
    'ZF': 1000,    // 5-Year T-Note
    'ZT': 2000     // 2-Year T-Note
  };
  
  return pointValues[symbol] || 1; // Default to 1 if symbol not found
}

/**
 * Get trade performance data
 */
function getTradePerformance(days) {
  try {
    days = days || 30;  // Default to 30 days if not provided
    Logger.log('Getting trade performance data for last ' + days + ' days');
    
    const sheets = initializeSpreadsheet();
    const sheet = sheets.trades;
    
    // Check if sheet has data
    const lastRow = sheet.getLastRow();
    const lastCol = sheet.getLastColumn();
    if (lastRow <= 1 || lastCol <= 0) {
      Logger.log('No trade data found');
      return { trades: [], performance: null };
    }
    
    const data = sheet.getDataRange().getValues();
    
    if (data.length <= 1) {
      Logger.log('No trade data rows found');
      return { trades: [], performance: null };
    }
    
    const headers = data[0];
    const rows = data.slice(1);
    
    Logger.log('Found ' + rows.length + ' trade rows');
    Logger.log('Headers: ' + JSON.stringify(headers));
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    const recentTrades = rows
      .filter(row => {
        const tradeDate = new Date(row[0]);
        return tradeDate >= cutoffDate;
      })
      .map(row => {
        const obj = {};
        headers.forEach((header, index) => {
          obj[header] = row[index];
        });
        return obj;
      });
    
    Logger.log('Found ' + recentTrades.length + ' recent trades');
    
    // Calculate performance metrics
    const wins = recentTrades.filter(trade => trade.Result === 'Win').length;
    const losses = recentTrades.filter(trade => trade.Result === 'Loss').length;
    const totalTrades = recentTrades.length;
    const winRate = totalTrades > 0 ? (wins / totalTrades * 100).toFixed(1) : 0;
    
    const totalPnL = recentTrades.reduce((sum, trade) => {
      const pnl = parseFloat(trade['Profit/Loss']) || 0;
      return sum + pnl;
    }, 0);
    
    const avgEmotionScore = recentTrades.length > 0 ? 
      recentTrades.reduce((sum, trade) => sum + (parseFloat(trade['Emotion Score']) || 5), 0) / recentTrades.length : 5;
    
    const performance = {
      totalTrades,
      wins,
      losses,
      winRate,
      totalPnL: totalPnL.toFixed(2),
      avgEmotionScore: avgEmotionScore.toFixed(1)
    };
    
    Logger.log('Performance calculated: ' + JSON.stringify(performance));
    
    return {
      trades: recentTrades,
      performance: performance
    };
  } catch (error) {
    Logger.log('Error getting trade performance: ' + error.toString());
    Logger.log('Error stack: ' + error.stack);
    return { trades: [], performance: null, error: error.toString() };
  }
}

/**
 * Get recent emotional data for analysis
 */
function getRecentEmotionalData(days) {
  try {
    days = days || 30;  // Default to 30 days if not provided
    Logger.log('Getting recent emotional data for last ' + days + ' days');
    
    const sheet = getEmotionsSheet();
    
    // Check if sheet has data
    const lastRow = sheet.getLastRow();
    const lastCol = sheet.getLastColumn();
    if (lastRow <= 1 || lastCol <= 0) {
      Logger.log('No emotional data found in sheet');
      return [];
    }
    
    const data = sheet.getDataRange().getValues();
    
    if (data.length <= 1) {
      Logger.log('No emotional data rows found');
      return [];
    }
    
    const headers = data[0];
    const rows = data.slice(1);
    
    Logger.log('Found ' + rows.length + ' emotional data rows');
    Logger.log('Emotional headers: ' + JSON.stringify(headers));
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    const recentData = rows
      .filter(row => {
        const dataDate = new Date(row[0]);
        return dataDate >= cutoffDate;
      })
      .map(row => {
        const obj = {};
        headers.forEach((header, index) => {
          obj[header] = row[index];
        });
        return obj;
      });
    
    Logger.log('Found ' + recentData.length + ' recent emotional entries');
    
    return recentData;
  } catch (error) {
    Logger.log('Error getting emotional data: ' + error.toString());
    Logger.log('Error stack: ' + error.stack);
    return [];
  }
}

/**
 * Analyze emotional patterns
 */
function analyzeEmotionalPatterns() {
  try {
    Logger.log('Starting emotional pattern analysis');
    
    const data = getRecentEmotionalData(30);
    
    Logger.log('Got ' + data.length + ' emotional data points');
    
    if (data.length === 0) {
      Logger.log('No emotional data found, returning default values');
      return {
        avgEmotionScore: 5,
        avgFearLevel: 5,
        avgGreedLevel: 5,
        avgConfidence: 5,
        totalEntries: 0,
        recommendations: ['Start recording your emotional states to get personalized insights.']
      };
    }
    
    const analysis = {
      avgEmotionScore: data.reduce((sum, item) => sum + (parseFloat(item['Emotion Score']) || 5), 0) / data.length,
      avgFearLevel: data.reduce((sum, item) => sum + (parseFloat(item['Fear Level']) || 5), 0) / data.length,
      avgGreedLevel: data.reduce((sum, item) => sum + (parseFloat(item['Greed Level']) || 5), 0) / data.length,
      avgConfidence: data.reduce((sum, item) => sum + (parseFloat(item['Confidence Level']) || 5), 0) / data.length,
      totalEntries: data.length,
      recommendations: []
    };
    
    Logger.log('Calculated analysis averages: ' + JSON.stringify(analysis));
    
    // Generate recommendations based on patterns
    if (analysis.avgFearLevel > 7) {
      analysis.recommendations.push('Your fear levels are elevated. Consider implementing risk management strategies and meditation.');
    }
    
    if (analysis.avgGreedLevel > 7) {
      analysis.recommendations.push('High greed levels detected. Focus on profit-taking strategies and position sizing.');
    }
    
    if (analysis.avgConfidence < 4) {
      analysis.recommendations.push('Low confidence levels. Consider backtesting your strategies and building confidence through education.');
    }
    
    if (analysis.avgEmotionScore < 4) {
      analysis.recommendations.push('Overall emotional state needs attention. Consider taking breaks and practicing stress management.');
    }
    
    if (analysis.recommendations.length === 0) {
      analysis.recommendations.push('Your emotional control appears balanced. Keep up the good work!');
    }
    
    Logger.log('Final analysis with recommendations: ' + JSON.stringify(analysis));
    
    return analysis;
  } catch (error) {
    Logger.log('Error analyzing patterns: ' + error.toString());
    Logger.log('Error stack: ' + error.stack);
    return { error: error.toString() };
  }
}

/**
 * Get trading psychology tips
 */
function getTradingPsychologyTips() {
  const tips = [
    {
      category: 'Fear Management',
      title: 'Position Sizing',
      content: 'Never risk more than 1-2% of your capital on a single trade. This helps reduce fear and emotional stress.',
      severity: 'high'
    },
    {
      category: 'Greed Control',
      title: 'Take Partial Profits',
      content: 'Scale out of winning positions. Take 50% profit at your first target, then let the rest run with a trailing stop.',
      severity: 'medium'
    },
    {
      category: 'Discipline',
      title: 'Stick to Your Plan',
      content: 'Write down your trading plan before the market opens. Stick to it regardless of market noise.',
      severity: 'high'
    },
    {
      category: 'Mindfulness',
      title: 'Breathing Exercise',
      content: 'Before entering any trade, take 3 deep breaths. Count to 4 on inhale, hold for 4, exhale for 4.',
      severity: 'low'
    },
    {
      category: 'Risk Management',
      title: 'Stop Losses Are Sacred',
      content: 'Always set stop losses before entering a trade. Never move them against you.',
      severity: 'high'
    },
    {
      category: 'Mental State',
      title: 'Trading Journal',
      content: 'Keep a detailed journal of not just what you traded, but how you felt and why you made each decision.',
      severity: 'medium'
    },
    {
      category: 'FOMO Prevention',
      title: 'Patience is Profitable',
      content: 'The market will always provide new opportunities. Missing one trade is better than forcing a bad one.',
      severity: 'medium'
    },
    {
      category: 'Overconfidence',
      title: 'Stay Humble',
      content: 'A few winning trades don\'t make you invincible. The market humbles everyone eventually.',
      severity: 'high'
    }
  ];
  
  return tips;
}

/**
 * Get a random motivational quote for traders
 */
function getMotivationalQuote() {
  const quotes = [
    "Risk comes from not knowing what you're doing. - Warren Buffett",
    "The goal of a successful trader is to make the best trades. Money is secondary. - Alexander Elder",
    "It's not whether you're right or wrong that's important, but how much money you make when you're right and how much you lose when you're wrong. - George Soros",
    "The market is a device for transferring money from the impatient to the patient. - Warren Buffett",
    "Rule No. 1: Never lose money. Rule No. 2: Never forget rule No. 1. - Warren Buffett",
    "In trading, what seems too good to be true usually is. - Larry Williams",
    "The key to trading success is emotional discipline. - Victor Sperandeo",
    "Markets are constantly in a state of uncertainty and flux, and money is made by discounting the obvious and betting on the unexpected. - George Soros"
  ];
  
  return quotes[Math.floor(Math.random() * quotes.length)];
}

/**
 * Emergency emotional reset function
 */
function emergencyEmotionalReset() {
  return {
    message: "STOP TRADING IMMEDIATELY",
    instructions: [
      "Step away from your trading platform",
      "Take 10 deep breaths",
      "Drink a glass of water",
      "Go for a 5-minute walk",
      "Review your trading plan",
      "Ask yourself: 'Am I trading with emotion or logic?'",
      "Only return to trading when you feel centered and calm"
    ],
    quote: "The market will be here tomorrow. Your capital might not be if you trade emotionally."
  };
}

/**
 * Set up time-based triggers for emotional check-ins
 */
function setupDailyTrigger() {
  ScriptApp.newTrigger('dailyEmotionalCheckIn')
    .timeBased()
    .everyDays(1)
    .atHour(9) // 9 AM
    .create();
}

/**
 * Daily emotional check-in function
 */
function dailyEmotionalCheckIn() {
  // This could send emails or notifications
  // For now, it just logs
  Logger.log('Daily emotional check-in triggered at: ' + new Date());
}

/**
 * Test function for development
 */
function testApp() {
  Logger.log('Testing Trading Emotion Control App');
  
  // Test spreadsheet initialization
  const sheet = initializeSpreadsheet();
  Logger.log('Spreadsheet initialized: ' + sheet.getName());
  
  // Test data recording
  const testData = {
    emotionScore: 6,
    marketAction: 'Buy',
    confidenceLevel: 7,
    fearLevel: 4,
    greedLevel: 3,
    notes: 'Test entry',
    reflection: 'Feeling good about this setup'
  };
  
  const result = recordEmotionalState(testData);
  Logger.log('Data recording result: ' + JSON.stringify(result));
  
  // Test analysis
  const analysis = analyzeEmotionalPatterns();
  Logger.log('Analysis result: ' + JSON.stringify(analysis));
}
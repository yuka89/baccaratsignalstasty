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
    
    const emotionsHeaders = emotionsSheet.getRange(1, 1, 1, emotionsSheet.getLastColumn()).getValues()[0];
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
    
    const tradesHeaders = tradesSheet.getRange(1, 1, 1, tradesSheet.getLastColumn()).getValues()[0];
    if (tradesHeaders.length === 0 || tradesHeaders[0] === '') {
      tradesSheet.getRange(1, 1, 1, 12).setValues([[
        'Timestamp', 'Symbol', 'Trade Type', 'Entry Price', 'Exit Price', 
        'Quantity', 'Result', 'Profit/Loss', 'Trade Notes', 'Chart Image ID', 
        'Emotion Score', 'Confidence Level'
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
    const sheet = getEmotionsSheet();
    const timestamp = new Date();
    
    sheet.appendRow([
      timestamp,
      data.emotionScore || 5,
      data.marketAction || 'Hold',
      data.confidenceLevel || 5,
      data.fearLevel || 5,
      data.greedLevel || 5,
      data.notes || '',
      data.reflection || ''
    ]);
    
    return { success: true, message: 'Emotional state recorded successfully' };
  } catch (error) {
    Logger.log('Error recording emotional state: ' + error.toString());
    return { success: false, message: error.toString() };
  }
}

/**
 * Record trade result with performance data
 */
function recordTrade(tradeData) {
  try {
    const sheets = initializeSpreadsheet();
    const sheet = sheets.trades;
    
    // Calculate profit/loss
    let profitLoss = 0;
    if (tradeData.entryPrice && tradeData.exitPrice && tradeData.quantity) {
      const entryPrice = parseFloat(tradeData.entryPrice);
      const exitPrice = parseFloat(tradeData.exitPrice);
      const quantity = parseFloat(tradeData.quantity);
      
      if (tradeData.tradeType === 'Long') {
        profitLoss = (exitPrice - entryPrice) * quantity;
      } else {
        profitLoss = (entryPrice - exitPrice) * quantity;
      }
    }
    
    sheet.appendRow([
      new Date(),
      tradeData.symbol || '',
      tradeData.tradeType || 'Long',
      tradeData.entryPrice || '',
      tradeData.exitPrice || '',
      tradeData.quantity || '',
      tradeData.result || 'Win',
      profitLoss.toFixed(2),
      tradeData.tradeNotes || '',
      '', // Chart Image ID - removed
      tradeData.emotionScore || 5,
      tradeData.confidenceLevel || 5
    ]);
    
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
 * Upload trade chart image
 */
function uploadTradeChart(imageData, fileName) {
  try {
    // Create a folder for trade charts if it doesn't exist
    const folders = DriveApp.getFoldersByName('Trading Charts');
    let folder;
    if (folders.hasNext()) {
      folder = folders.next();
    } else {
      folder = DriveApp.createFolder('Trading Charts');
    }
    
    // Convert base64 to blob and create file
    const contentType = imageData.split(';')[0].split(':')[1];
    const base64Data = imageData.split(',')[1];
    const blob = Utilities.newBlob(Utilities.base64Decode(base64Data), contentType, fileName);
    const file = folder.createFile(blob);
    
    // Make file viewable
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    
    return { 
      success: true, 
      fileId: file.getId(), 
      url: file.getUrl(),
      message: 'Chart uploaded successfully' 
    };
  } catch (error) {
    Logger.log('Error uploading chart: ' + error.toString());
    return { success: false, message: error.toString() };
  }
}

/**
 * Get trade performance data
 */
function getTradePerformance(days = 30) {
  try {
    const sheets = initializeSpreadsheet();
    const sheet = sheets.trades;
    const data = sheet.getDataRange().getValues();
    
    if (data.length <= 1) return { trades: [], performance: null };
    
    const headers = data[0];
    const rows = data.slice(1);
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    const recentTrades = rows
      .filter(row => new Date(row[0]) >= cutoffDate)
      .map(row => {
        const obj = {};
        headers.forEach((header, index) => {
          obj[header] = row[index];
        });
        return obj;
      });
    
    // Calculate performance metrics
    const wins = recentTrades.filter(trade => trade.Result === 'Win').length;
    const losses = recentTrades.filter(trade => trade.Result === 'Loss').length;
    const totalTrades = recentTrades.length;
    const winRate = totalTrades > 0 ? (wins / totalTrades * 100).toFixed(1) : 0;
    
    const totalPnL = recentTrades.reduce((sum, trade) => {
      return sum + (parseFloat(trade['Profit/Loss']) || 0);
    }, 0);
    
    const avgEmotionScore = recentTrades.length > 0 ? 
      recentTrades.reduce((sum, trade) => sum + (trade['Emotion Score'] || 5), 0) / recentTrades.length : 5;
    
    return {
      trades: recentTrades,
      performance: {
        totalTrades,
        wins,
        losses,
        winRate,
        totalPnL: totalPnL.toFixed(2),
        avgEmotionScore: avgEmotionScore.toFixed(1)
      }
    };
  } catch (error) {
    Logger.log('Error getting trade performance: ' + error.toString());
    return { trades: [], performance: null };
  }
}

/**
 * Get recent emotional data for analysis
 */
function getRecentEmotionalData(days = 30) {
  try {
    const sheet = getEmotionsSheet();
    const data = sheet.getDataRange().getValues();
    
    if (data.length <= 1) return [];
    
    const headers = data[0];
    const rows = data.slice(1);
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    const recentData = rows
      .filter(row => new Date(row[0]) >= cutoffDate)
      .map(row => {
        const obj = {};
        headers.forEach((header, index) => {
          obj[header] = row[index];
        });
        return obj;
      });
    
    return recentData;
  } catch (error) {
    Logger.log('Error getting emotional data: ' + error.toString());
    return [];
  }
}

/**
 * Analyze emotional patterns
 */
function analyzeEmotionalPatterns() {
  try {
    const data = getRecentEmotionalData(30);
    
    if (data.length === 0) {
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
      avgEmotionScore: data.reduce((sum, item) => sum + (item['Emotion Score'] || 5), 0) / data.length,
      avgFearLevel: data.reduce((sum, item) => sum + (item['Fear Level'] || 5), 0) / data.length,
      avgGreedLevel: data.reduce((sum, item) => sum + (item['Greed Level'] || 5), 0) / data.length,
      avgConfidence: data.reduce((sum, item) => sum + (item['Confidence Level'] || 5), 0) / data.length,
      totalEntries: data.length,
      recommendations: []
    };
    
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
    
    return analysis;
  } catch (error) {
    Logger.log('Error analyzing patterns: ' + error.toString());
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
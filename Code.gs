/**
 * Trading Emotion Control App
 * Google Apps Script application to help traders manage emotions
 */

// Global configuration
const SHEET_NAME = 'TradingEmotions';
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
    let sheet;
    if (SPREADSHEET_ID) {
      const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
      sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    } else {
      const ss = SpreadsheetApp.create('Trading Emotions Data');
      sheet = ss.getActiveSheet();
      sheet.setName(SHEET_NAME);
      Logger.log('Created new spreadsheet: ' + ss.getId());
    }
    
    // Set up headers if not exists
    const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    if (headers.length === 0 || headers[0] === '') {
      sheet.getRange(1, 1, 1, 8).setValues([[
        'Timestamp', 'Emotion Score', 'Market Action', 'Confidence Level', 
        'Fear Level', 'Greed Level', 'Notes', 'Reflection'
      ]]);
    }
    
    return sheet;
  } catch (error) {
    Logger.log('Error initializing spreadsheet: ' + error.toString());
    throw error;
  }
}

/**
 * Record emotional state and trading decision
 */
function recordEmotionalState(data) {
  try {
    const sheet = initializeSpreadsheet();
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
 * Get recent emotional data for analysis
 */
function getRecentEmotionalData(days = 30) {
  try {
    const sheet = initializeSpreadsheet();
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
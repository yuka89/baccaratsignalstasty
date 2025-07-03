# 🚀 Quick Deployment Guide

## Step-by-Step Setup (5 minutes)

### 1. Create Google Apps Script Project
1. Go to [script.google.com](https://script.google.com)
2. Click **"+ New project"**
3. Rename from "Untitled project" to **"Trading Emotion Control"**

### 2. Upload Files
1. **Replace Code.gs**: 
   - Delete default content
   - Copy and paste content from `Code.gs`

2. **Add HTML file**:
   - Click **"+"** → **"HTML file"**
   - Name it **"index"**
   - Copy and paste content from `index.html`

3. **Add Configuration**:
   - Click **"+"** → **"JSON file"** 
   - Name it **"appsscript"**
   - Copy and paste content from `appsscript.json`

### 3. Deploy Web App
1. Click **"Deploy"** → **"New deployment"**
2. Click gear icon ⚙️ → Select **"Web app"**
3. Set **Execute as**: "Me"
4. Set **Who has access**: "Anyone" 
5. Click **"Deploy"**
6. Click **"Authorize access"** and grant permissions
7. **Copy the Web app URL** 📋

### 4. Test Your App
1. Open the Web app URL in new browser tab
2. Fill out the emotion tracking form
3. Click "Record Emotional State"
4. Check that data appears in the auto-created Google Sheet

## ✅ You're Done!

Your Trading Emotion Control app is now live and ready to use.

## 📱 Bookmark the URL
- Add the web app URL to your bookmarks
- Create a home screen shortcut on mobile
- Share with other traders (if desired)

## 🔧 Optional Customizations

### Use Your Own Google Sheet
1. Create a new Google Sheet
2. Copy the Sheet ID from the URL: `docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
3. In Code.gs, update: `const SPREADSHEET_ID = 'your_sheet_id_here';`
4. Deploy new version

### Set Up Daily Reminders
1. In Apps Script editor, run the `setupDailyTrigger` function
2. This will send you daily emotional check-in reminders at 9 AM

### Change Time Zone
1. In `appsscript.json`, update `timeZone` to your preferred timezone
2. Common options: "America/New_York", "Europe/London", "Asia/Tokyo"

## 🆘 Troubleshooting

**App won't load?**
- Check that all three files (Code.gs, index.html, appsscript.json) are uploaded
- Try deploying a new version
- Verify you authorized all permissions

**Data not saving?**
- Check execution logs in Apps Script editor
- Run the `testApp()` function manually
- Verify Google Sheets permissions are granted

**Need help?**
- Check the execution transcript in Apps Script
- Look at browser console (F12) for JavaScript errors
- Review the detailed README.md for troubleshooting steps

---

🎯 **Pro Tip**: Use this app daily for maximum benefit. Emotional awareness is the key to trading success!
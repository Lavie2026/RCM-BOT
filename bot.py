import yfinance as yf
import requests
import os
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def get_data(ticker, name):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="2d")
        if len(df) < 2: return f"{name}: נתון חסר"
        change = ((df['Close'].iloc[-1] / df['Close'].iloc[-2]) - 1) * 100
        icon = "🟢" if change >= 0 else "🔴"
        return f"{icon} {name}: {change:+.2f}%"
    except: return f"⚠️ {name}: שגיאה"

def run():
    msg = f"📊 *סיכום יום מסחר - RCM הדרכה פיננסית*\n"
    msg += f"📅 {datetime.now().strftime('%d/%m/%Y')}\n\n"
    msg += f"🇮🇱 *תל אביב:*\n{get_data('^TA125.TA', 'תא 125')}\n{get_data('^TA35.TA', 'תא 35')}\n\n"
    msg += f"🇺🇸 *ארה\"ב:*\n{get_data('^GSPC', 'S&P 500')}\n{get_data('^IXIC', 'Nasdaq')}\n\n"
    msg += "📈 *בהצלחה, צוות RCM*"
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run()
  

"""
================================================================
MARKET UPDATER v1.0 - Hourly Market Data Refresh
================================================================
Runs every hour to update market data in news.json
Does NOT send emails - just updates the JSON file
================================================================
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

# 🇮🇳 INDIAN MARKETS
INDIAN_INDICES = [
    ("Nifty 50", "^NSEI"),
    ("Sensex", "^BSESN"),
    ("Bank Nifty", "^NSEBANK"),
    ("Nifty IT", "^CNXIT"),
    ("Nifty Pharma", "^CNXPHARMA")
]

INDIAN_STOCKS = [
    ("TCS", "TCS.NS"),
    ("Reliance", "RELIANCE.NS"),
    ("HDFC Bank", "HDFCBANK.NS"),
    ("Infosys", "INFY.NS"),
    ("ICICI Bank", "ICICIBANK.NS"),
    ("L&T", "LT.NS"),
    ("Wipro", "WIPRO.NS"),
    ("Maruti", "MARUTI.NS"),
    ("Sun Pharma", "SUNPHARMA.NS"),
    ("Bharti Airtel", "BHARTIARTL.NS"),
    ("Bajaj Finance", "BAJFINANCE.NS"),
    ("Tata Motors", "TATAMOTORS.NS")
]

# 🇺🇸 US MARKETS
US_INDICES = [
    ("S&P 500", "^GSPC"),
    ("NASDAQ", "^IXIC"),
    ("Dow Jones", "^DJI")
]

US_STOCKS = [
    ("Apple", "AAPL"),
    ("Microsoft", "MSFT"),
    ("Google", "GOOGL"),
    ("Nvidia", "NVDA"),
    ("Tesla", "TSLA"),
    ("Amazon", "AMZN"),
    ("Meta", "META")
]

# ₿ CRYPTO
CRYPTO = [
    ("Bitcoin", "BTC-USD"),
    ("Ethereum", "ETH-USD"),
    ("Solana", "SOL-USD"),
    ("Cardano", "ADA-USD")
]

# 💵 CURRENCY & COMMODITY
CURRENCY = [
    ("USD/INR", "INR=X"),
    ("EUR/USD", "EURUSD=X")
]

COMMODITY = [
    ("Gold (₹/10g)", "GC=F"),
    ("Silver", "SI=F"),
    ("Crude Oil", "CL=F")
]


# =====================================================
# FETCH STOCK DATA (Yahoo Finance)
# =====================================================

def fetch_stock_data(symbol):
    """Fetch current price and change for a symbol via Yahoo Finance"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}"
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
        
        result = data['chart']['result'][0]
        meta = result['meta']
        
        current = meta.get('regularMarketPrice', 0)
        previous = meta.get('chartPreviousClose', meta.get('previousClose', current))
        change = current - previous
        change_pct = (change / previous * 100) if previous else 0
        
        return {
            'price': current,
            'change': change,
            'change_pct': change_pct,
            'is_up': change >= 0
        }
    except Exception as e:
        print(f"  [STOCK] Failed {symbol}: {e}")
        return None


def fetch_all_stocks(stocks_list):
    """Fetch multiple stocks and return list of valid results"""
    results = []
    for name, symbol in stocks_list:
        data = fetch_stock_data(symbol)
        if data:
            results.append({'name': name, **data})
    return results


# =====================================================
# MAIN
# =====================================================

def main():
    print("=" * 60)
    print(f"MARKET UPDATER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Build market object
    market = {
        "last_updated": datetime.now().strftime("%I:%M %p IST"),
        "last_updated_iso": datetime.now().isoformat(),
        "indian": {},
        "us": {},
        "crypto": [],
        "currency": [],
        "commodity": []
    }
    
    # 🇮🇳 INDIAN MARKETS
    print("\n[🇮🇳 INDIAN MARKETS]")
    market['indian']['indices'] = fetch_all_stocks(INDIAN_INDICES)
    print(f"  Indices: {len(market['indian']['indices'])} fetched")
    
    indian_stocks = fetch_all_stocks(INDIAN_STOCKS)
    indian_stocks.sort(key=lambda x: x['change_pct'], reverse=True)
    market['indian']['gainers'] = indian_stocks[:3]
    market['indian']['losers'] = indian_stocks[-3:][::-1]
    print(f"  Gainers/Losers: {len(indian_stocks)} stocks tracked")
    
    # 🇺🇸 US MARKETS
    print("\n[🇺🇸 US MARKETS]")
    market['us']['indices'] = fetch_all_stocks(US_INDICES)
    print(f"  Indices: {len(market['us']['indices'])} fetched")
    
    us_stocks = fetch_all_stocks(US_STOCKS)
    us_stocks.sort(key=lambda x: x['change_pct'], reverse=True)
    market['us']['gainers'] = us_stocks[:3]
    market['us']['losers'] = us_stocks[-3:][::-1]
    print(f"  Stocks: {len(us_stocks)} tracked")
    
    # ₿ CRYPTO
    print("\n[₿ CRYPTO]")
    market['crypto'] = fetch_all_stocks(CRYPTO)
    print(f"  Crypto: {len(market['crypto'])} fetched")
    
    # 💵 CURRENCY
    print("\n[💵 CURRENCY]")
    market['currency'] = fetch_all_stocks(CURRENCY)
    print(f"  Currency: {len(market['currency'])} fetched")
    
    # 🪙 COMMODITY
    print("\n[🪙 COMMODITY]")
    market['commodity'] = fetch_all_stocks(COMMODITY)
    print(f"  Commodity: {len(market['commodity'])} fetched")
    
    # Read existing news.json (so we don't lose news data)
    existing_data = {}
    try:
        with open('news.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print("\n[FILE] Loaded existing news.json")
    except:
        print("\n[FILE] No existing news.json, creating new")
    
    # Update only the market section
    existing_data['market'] = market
    existing_data['market_last_updated'] = datetime.now().strftime("%I:%M %p IST")
    
    # Save back
    try:
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Market data saved to news.json")
        print(f"   Updated at: {datetime.now().strftime('%I:%M %p IST')}")
    except Exception as e:
        print(f"\n❌ Failed to save: {e}")


if __name__ == "__main__":
    main()

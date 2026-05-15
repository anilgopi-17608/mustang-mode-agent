"""
================================================================
TECH PIT STOP - DAILY DIGEST v2.0
================================================================
Built for: ANIL GOPI GUDAPATI
Layout: 2-column (News + Stocks)

LEFT COLUMN (70%): News
  🤖 AI / Tech (TechCrunch, The Verge, MIT Tech)
  🏥 Medical Devices (MassDevice, Medical Design)
  🇮🇳 India Tech (YourStory, Inc42)
  🛠️ Engineering (Engineering.com)
  📺 Tech Videos (MKBHD, Two Minute Papers)

RIGHT COLUMN (30%): Indian Stock Market
  📈 Nifty 50, Sensex, Bank Nifty
  🏆 Top Gainers / Losers
  💵 USD/INR, Gold price

Runs at 7:00 AM IST daily via GitHub Actions.
================================================================
"""

import os
import re
import json
import time
import smtplib
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from xml.etree import ElementTree as ET

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# =====================================================
# CONFIGURATION
# =====================================================

GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

DIGEST_RECIPIENT = "anilgopi731@gmail.com"
SENDER_EMAIL = "anilgopi731@gmail.com"
USER_NAME = "Anil"

USE_AI_SUMMARIES = bool(GEMINI_API_KEY) and GEMINI_AVAILABLE

# News sources organized by category
NEWS_CATEGORIES = {
    "🤖 AI & TECH": {
        "color": "#dc2626",
        "max_items": 5,
        "feeds": [
            ("TechCrunch", "https://techcrunch.com/feed/"),
            ("The Verge", "https://www.theverge.com/rss/index.xml"),
            ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
            ("MIT Technology Review", "https://www.technologyreview.com/feed/")
        ]
    },
    "💼 MARKET INTELLIGENCE": {
        "color": "#7c3aed",
        "max_items": 5,
        "feeds": [
            ("Economic Times Markets", "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"),
            ("Moneycontrol Business", "https://www.moneycontrol.com/rss/business.xml"),
            ("Business Standard Markets", "https://www.business-standard.com/rss/markets-106.rss"),
            ("Livemint Companies", "https://www.livemint.com/rss/companies"),
            ("Reuters Business", "https://www.reuters.com/business/feed/")
        ]
    },
    "🏥 MEDICAL DEVICES": {
        "color": "#16a34a",
        "max_items": 3,
        "feeds": [
            ("MassDevice", "https://www.massdevice.com/feed/"),
            ("Medical Design & Outsourcing", "https://www.medicaldesignandoutsourcing.com/feed/"),
            ("Medical Device Network", "https://www.medicaldevice-network.com/feed/")
        ]
    },
    "🇮🇳 INDIA TECH": {
        "color": "#ff6b00",
        "max_items": 3,
        "feeds": [
            ("YourStory", "https://yourstory.com/feed"),
            ("Inc42", "https://inc42.com/feed/"),
            ("Entrackr", "https://entrackr.com/feed/")
        ]
    },
    "🛠️ ENGINEERING": {
        "color": "#0891b2",
        "max_items": 2,
        "feeds": [
            ("Design World", "https://www.designworldonline.com/feed/"),
            ("Engineering.com", "https://www.engineering.com/rss")
        ]
    }
}

# YouTube channels
YOUTUBE_CHANNELS = [
    {
        "name": "MKBHD",
        "channel_id": "UCBJycsmduvYEL83R_U4JriQ",
        "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ"
    },
    {
        "name": "Two Minute Papers (AI)",
        "channel_id": "UCbfYPyITQ-7l4upoX8nvctg",
        "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg"
    }
]

# Stock symbols to track
STOCK_SYMBOLS = {
    "indices": [
        ("Nifty 50", "^NSEI"),
        ("Sensex", "^BSESN"),
        ("Bank Nifty", "^NSEBANK")
    ],
    "currency": [
        ("USD/INR", "INR=X")
    ],
    "commodity": [
        ("Gold (₹/10g)", "GC=F")
    ]
}

# Top stocks for gainers/losers tracking
TOP_STOCKS = [
    ("TCS", "TCS.NS"),
    ("Reliance", "RELIANCE.NS"),
    ("HDFC Bank", "HDFCBANK.NS"),
    ("Infosys", "INFY.NS"),
    ("ICICI Bank", "ICICIBANK.NS"),
    ("L&T", "LT.NS"),
    ("Wipro", "WIPRO.NS"),
    ("Maruti", "MARUTI.NS"),
    ("Sun Pharma", "SUNPHARMA.NS"),
    ("Bharti Airtel", "BHARTIARTL.NS")
]

# =====================================================
# GEMINI AI FOR SUMMARIES
# =====================================================

def init_gemini():
    if not USE_AI_SUMMARIES:
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("[OK] Gemini AI activated")
        return model
    except Exception as e:
        print(f"[WARN] Gemini init failed: {e}")
        return None


def ai_summarize(model, title, content, category=""):
    if not model:
        return content[:180] + "..." if content else ""
    
    # Special prompt for market intelligence to highlight deals/acquisitions
    if "MARKET" in category.upper() or "BUSINESS" in category.upper():
        prompt = f"""Summarize this business news in ONE punchy English sentence (max 30 words). 
Focus on:
- Deal value (₹, $)
- Companies involved
- Action (acquired, merged, raised, listed)
- Impact

Title: {title}
Content: {content[:500]}

Reply with ONLY the summary."""
    else:
        prompt = f"""Summarize this news in ONE simple English sentence (max 25 words). Be direct.

Title: {title}
Content: {content[:400]}

Reply with ONLY the summary."""
    
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        summary = re.sub(r'^"|"$', '', summary)
        return summary[:220]
    except Exception as e:
        return content[:180] + "..." if content else ""


# =====================================================
# RSS FEED PARSING
# =====================================================

def fetch_rss(url, max_items=5):
    """Fetch and parse RSS feed (RSS 2.0 or Atom)"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
        
        root = ET.fromstring(data)
        items = []
        
        # RSS 2.0 format
        for item in root.iter('item'):
            if len(items) >= max_items:
                break
            title = (item.findtext('title') or '').strip()
            link = (item.findtext('link') or '').strip()
            description = (item.findtext('description') or '').strip()
            description = re.sub(r'<[^>]+>', ' ', description)
            description = re.sub(r'\s+', ' ', description).strip()
            
            if title and link:
                items.append({
                    'title': title,
                    'link': link,
                    'description': description[:400]
                })
        
        # Atom format (YouTube)
        if not items:
            atom_ns = '{http://www.w3.org/2005/Atom}'
            media_ns = '{http://search.yahoo.com/mrss/}'
            
            for entry in root.iter(f'{atom_ns}entry'):
                if len(items) >= max_items:
                    break
                
                title = (entry.findtext(f'{atom_ns}title') or '').strip()
                link_elem = entry.find(f'{atom_ns}link')
                link = link_elem.get('href', '') if link_elem is not None else ''
                
                desc = ""
                thumb = ""
                
                media_group = entry.find(f'{media_ns}group')
                if media_group is not None:
                    desc_elem = media_group.find(f'{media_ns}description')
                    if desc_elem is not None and desc_elem.text:
                        desc = desc_elem.text[:400]
                    
                    thumb_elem = media_group.find(f'{media_ns}thumbnail')
                    if thumb_elem is not None:
                        thumb = thumb_elem.get('url', '')
                
                if title and link:
                    items.append({
                        'title': title,
                        'link': link,
                        'description': desc,
                        'thumbnail': thumb
                    })
        
        return items
    except Exception as e:
        print(f"  [ERROR] {url}: {e}")
        return []


# =====================================================
# STOCK MARKET DATA (Yahoo Finance)
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


def get_market_data():
    """Get all market data: indices, top movers, currency, gold"""
    print("\n[STOCKS] Fetching market data...")
    market = {
        'indices': [],
        'gainers': [],
        'losers': [],
        'currency': [],
        'commodity': []
    }
    
    # Indices
    for name, symbol in STOCK_SYMBOLS['indices']:
        data = fetch_stock_data(symbol)
        if data:
            market['indices'].append({'name': name, **data})
            print(f"  {name}: {data['price']:.2f} ({data['change_pct']:+.2f}%)")
    
    # Currency
    for name, symbol in STOCK_SYMBOLS['currency']:
        data = fetch_stock_data(symbol)
        if data:
            market['currency'].append({'name': name, **data})
    
    # Commodity
    for name, symbol in STOCK_SYMBOLS['commodity']:
        data = fetch_stock_data(symbol)
        if data:
            market['commodity'].append({'name': name, **data})
    
    # Top stocks for gainers/losers
    stock_data = []
    for name, symbol in TOP_STOCKS:
        data = fetch_stock_data(symbol)
        if data:
            stock_data.append({'name': name, **data})
    
    # Sort by change_pct
    stock_data.sort(key=lambda x: x['change_pct'], reverse=True)
    market['gainers'] = stock_data[:3]
    market['losers'] = stock_data[-3:][::-1]  # Reverse to show worst first
    
    return market


# =====================================================
# BUILD HTML DIGEST
# =====================================================

def build_news_column_html(all_news, all_videos):
    """Build the LEFT column with all news + videos"""
    html = ""
    
    # News categories
    for cat_name, cat_info in all_news.items():
        items = cat_info['items']
        if not items:
            continue
        
        color = cat_info['color']
        cards_html = ""
        for i, item in enumerate(items, 1):
            summary = item.get('summary', item.get('description', ''))[:200]
            cards_html += f"""
            <div style='background:#ffffff; border:1px solid #e5e7eb; border-left:3px solid {color}; border-radius:8px; padding:14px; margin-bottom:10px;'>
                <div style='font-size:9px; color:#9ca3af; letter-spacing:2px; font-weight:bold; margin-bottom:4px;'>#{i}</div>
                <div style='color:#111827; font-size:14px; font-weight:bold; line-height:1.4; margin-bottom:6px;'>
                    {item['title']}
                </div>
                <div style='color:#4b5563; font-size:12px; line-height:1.5; margin:6px 0;'>
                    💡 {summary}
                </div>
                <a href='{item['link']}' style='display:inline-block; color:{color}; font-size:11px; font-weight:bold; text-decoration:none; margin-top:4px;'>
                    📖 Read →
                </a>
            </div>
            """
        
        html += f"""
        <div style='margin-bottom:20px;'>
            <div style='background:linear-gradient(135deg, {color}, #000); color:#fff; padding:10px 14px; border-radius:8px; margin-bottom:10px;'>
                <div style='font-size:13px; font-weight:bold; letter-spacing:2px;'>{cat_name}</div>
            </div>
            {cards_html}
        </div>
        """
    
    # YouTube videos
    if all_videos:
        html += """
        <div style='margin-bottom:20px;'>
            <div style='background:linear-gradient(135deg, #ff0000, #000); color:#fff; padding:10px 14px; border-radius:8px; margin-bottom:10px;'>
                <div style='font-size:13px; font-weight:bold; letter-spacing:2px;'>📺 TOP TECH VIDEOS</div>
            </div>
        """
        for vid in all_videos:
            thumb = vid.get('thumbnail', '')
            channel = vid.get('channel', '')
            summary = vid.get('summary', vid.get('description', 'New video uploaded'))[:180]
            
            thumb_html = ""
            if thumb:
                thumb_html = f"""
                <a href='{vid['link']}'>
                    <img src='{thumb}' style='width:100%; border-radius:6px; margin-bottom:8px; border:1px solid #e5e7eb;' alt='Video'>
                </a>
                """
            
            html += f"""
            <div style='background:#ffffff; border:1px solid #e5e7eb; border-left:3px solid #ff0000; border-radius:8px; padding:14px; margin-bottom:10px;'>
                <div style='font-size:9px; color:#9ca3af; letter-spacing:2px; font-weight:bold; margin-bottom:6px;'>🎬 {channel.upper()}</div>
                <div style='color:#111827; font-size:14px; font-weight:bold; margin-bottom:8px; line-height:1.4;'>
                    {vid['title']}
                </div>
                {thumb_html}
                <div style='color:#4b5563; font-size:12px; line-height:1.5; margin:6px 0;'>
                    💡 {summary}
                </div>
                <a href='{vid['link']}' style='display:inline-block; background:#ff0000; color:#fff; padding:6px 14px; border-radius:4px; font-size:11px; font-weight:bold; text-decoration:none;'>
                    ▶️ Watch
                </a>
            </div>
            """
        html += "</div>"
    
    return html


def build_stock_column_html(market):
    """Build the RIGHT column with stock market data"""
    
    def stock_card(item, prefix=""):
        if not item:
            return ""
        arrow = "▲" if item['is_up'] else "▼"
        color = "#16a34a" if item['is_up'] else "#dc2626"
        sign = "+" if item['is_up'] else ""
        return f"""
        <div style='background:#ffffff; padding:10px 12px; margin-bottom:6px; border-radius:6px; border:1px solid #e5e7eb;'>
            <div style='color:#374151; font-size:11px; font-weight:bold; margin-bottom:2px;'>{prefix}{item['name']}</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div style='color:#111827; font-size:14px; font-weight:bold;'>₹{item['price']:,.2f}</div>
                <div style='color:{color}; font-size:11px; font-weight:bold;'>{arrow} {sign}{item['change_pct']:.2f}%</div>
            </div>
        </div>
        """
    
    indices_html = "".join(stock_card(idx) for idx in market.get('indices', []))
    gainers_html = "".join(stock_card(stk) for stk in market.get('gainers', []))
    losers_html = "".join(stock_card(stk) for stk in market.get('losers', []))
    currency_html = "".join(stock_card(c) for c in market.get('currency', []))
    commodity_html = "".join(stock_card(c) for c in market.get('commodity', []))
    
    return f"""
    <!-- Indices -->
    <div style='background:linear-gradient(135deg, #1f1f1f, #0a0a0a); color:#fff; padding:10px 14px; border-radius:8px; margin-bottom:10px;'>
        <div style='font-size:11px; font-weight:bold; letter-spacing:2px;'>📈 MARKET INDICES</div>
    </div>
    {indices_html}
    
    <!-- Gainers -->
    <div style='background:linear-gradient(135deg, #16a34a, #0a4d1e); color:#fff; padding:10px 14px; border-radius:8px; margin:14px 0 10px;'>
        <div style='font-size:11px; font-weight:bold; letter-spacing:2px;'>🏆 TOP GAINERS</div>
    </div>
    {gainers_html}
    
    <!-- Losers -->
    <div style='background:linear-gradient(135deg, #dc2626, #4d0a0a); color:#fff; padding:10px 14px; border-radius:8px; margin:14px 0 10px;'>
        <div style='font-size:11px; font-weight:bold; letter-spacing:2px;'>📉 TOP LOSERS</div>
    </div>
    {losers_html}
    
    <!-- Currency & Gold -->
    <div style='background:linear-gradient(135deg, #f59e0b, #92400e); color:#fff; padding:10px 14px; border-radius:8px; margin:14px 0 10px;'>
        <div style='font-size:11px; font-weight:bold; letter-spacing:2px;'>💵 FOREX & GOLD</div>
    </div>
    {currency_html}
    {commodity_html}
    """


def build_digest_html(all_news, all_videos, market):
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    news_column = build_news_column_html(all_news, all_videos)
    stock_column = build_stock_column_html(market)
    
    total_stories = sum(len(s['items']) for s in all_news.values())
    total_videos = len(all_videos)
    
    html = f"""
    <html>
    <body style='margin:0; padding:0; background:#f3f4f6; font-family:Verdana, Arial, sans-serif;'>
        <div style='max-width:900px; margin:0 auto; padding:24px 16px;'>
            
            <!-- Header -->
            <div style='text-align:center; padding:28px 20px; background:linear-gradient(135deg, #1f1f1f 0%, #0a0a0a 100%); border-radius:14px; margin-bottom:18px;'>
                <div style='font-size:32px; margin-bottom:4px;'>🌅</div>
                <h1 style='color:#ffffff; letter-spacing:4px; margin:6px 0 0 0; font-size:22px; font-weight:bold;'>TECH PIT STOP</h1>
                <div style='color:#fbbf24; font-size:12px; letter-spacing:3px; margin-top:6px; font-weight:bold;'>MORNING DIGEST</div>
                <div style='color:#9ca3af; font-size:11px; letter-spacing:2px; margin-top:8px;'>{today.upper()}</div>
            </div>
            
            <!-- Greeting -->
            <div style='background:#ffffff; border-radius:10px; padding:16px 20px; margin-bottom:16px; border:1px solid #e5e7eb;'>
                <div style='color:#111827; font-size:14px; line-height:1.7;'>
                    Good morning <span style='color:#dc2626; font-weight:bold;'>{USER_NAME}</span>! ☕<br>
                    <span style='color:#16a34a; font-weight:bold;'>{total_stories} stories</span> + 
                    <span style='color:#ff0000; font-weight:bold;'>{total_videos} videos</span> + 
                    <span style='color:#f59e0b; font-weight:bold;'>live market data</span> waiting for you.
                </div>
            </div>
            
            <!-- 2-Column Layout -->
            <table cellpadding="0" cellspacing="0" border="0" style='width:100%; border-collapse:separate; border-spacing:10px 0;'>
                <tr>
                    <!-- LEFT: News (~70%) -->
                    <td style='width:65%; vertical-align:top;'>
                        {news_column}
                    </td>
                    
                    <!-- RIGHT: Stocks (~30%) -->
                    <td style='width:35%; vertical-align:top;'>
                        {stock_column}
                    </td>
                </tr>
            </table>
            
            <!-- Footer -->
            <div style='text-align:center; padding:20px; margin-top:18px; background:#1f1f1f; border-radius:10px;'>
                <div style='color:#fbbf24; font-size:11px; letter-spacing:3px; font-weight:bold;'>🌅 STAY CURIOUS · LEARN DAILY 🚀</div>
                <div style='margin-top:8px; color:#6b7280; font-size:10px; letter-spacing:1px;'>☕ Tech Pit Stop · Sent every morning at 7 AM IST</div>
            </div>
            
        </div>
    </body>
    </html>
    """
    return html


# =====================================================
# SEND EMAIL
# =====================================================

def send_digest(html_content, total_stories, total_videos):
    if not GMAIL_APP_PASSWORD:
        print("ERROR: No GMAIL_APP_PASSWORD!")
        return False
    
    today = datetime.now().strftime("%b %d")
    subject = f"🌅 Tech Pit Stop | {total_stories} stories + market update ({today})"
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"Tech Pit Stop AI <{SENDER_EMAIL}>"
    msg['To'] = DIGEST_RECIPIENT
    msg.attach(MIMEText(html_content, 'html'))
    
    print(f"\nSending to {DIGEST_RECIPIENT}...")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print("Sent successfully!")
        return True
    except Exception as e:
        print(f"Send failed: {e}")
        return False


# =====================================================
# MAIN
# =====================================================

def main():
    print("=" * 60)
    print("TECH PIT STOP v2.0 - MORNING DIGEST")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    model = init_gemini()
    
    # Fetch news by category
    all_news = {}
    for cat_name, cat_info in NEWS_CATEGORIES.items():
        print(f"\n[NEWS] {cat_name}")
        category_items = []
        max_per_cat = cat_info['max_items']
        
        for source_name, rss_url in cat_info['feeds']:
            if len(category_items) >= max_per_cat:
                break
            try:
                items = fetch_rss(rss_url, max_items=2)
                for item in items:
                    if len(category_items) >= max_per_cat:
                        break
                    item['source'] = source_name
                    
                    if model:
                        try:
                            item['summary'] = ai_summarize(model, item['title'], item['description'], cat_name)
                            time.sleep(0.3)
                        except:
                            item['summary'] = item.get('description', '')[:180]
                    
                    category_items.append(item)
                print(f"  ✓ {source_name}: {len(items)} items")
            except Exception as e:
                print(f"  ✗ {source_name} failed: {e}")
        
        all_news[cat_name] = {
            'items': category_items[:max_per_cat],
            'color': cat_info['color']
        }
    
    # Fetch YouTube videos
    print("\n[VIDEOS] Fetching top tech videos...")
    all_videos = []
    for channel in YOUTUBE_CHANNELS:
        try:
            items = fetch_rss(channel['rss'], max_items=1)
            for item in items:
                item['channel'] = channel['name']
                if model:
                    try:
                        item['summary'] = ai_summarize(model, item['title'], item['description'])
                        time.sleep(0.3)
                    except:
                        item['summary'] = "Click to watch this video"
                all_videos.append(item)
            print(f"  ✓ {channel['name']}: {len(items)} videos")
        except Exception as e:
            print(f"  ✗ {channel['name']} failed: {e}")
    
    # Fetch stock market data
    try:
        market = get_market_data()
    except Exception as e:
        print(f"[ERROR] Market data failed: {e}")
        market = {'indices': [], 'gainers': [], 'losers': [], 'currency': [], 'commodity': []}
    
    # Stats
    total_stories = sum(len(s['items']) for s in all_news.values())
    total_videos = len(all_videos)
    
    print(f"\n{'=' * 60}")
    print(f"DIGEST: {total_stories} stories + {total_videos} videos + market data")
    print(f"{'=' * 60}")
    
    if total_stories == 0 and total_videos == 0 and not market['indices']:
        print("[WARN] Everything empty - skipping send")
        return
    
    # ⭐ NEW: Save to news.json for the web page
    save_news_json(all_news, all_videos, market)
    
    html = build_digest_html(all_news, all_videos, market)
    send_digest(html, total_stories, total_videos)
    
    print("\nMorning digest complete! ☕")


def save_news_json(all_news, all_videos, market):
    """Save news data to news.json for the web page"""
    print("\n[JSON] Saving news.json for web page...")
    
    # Build the JSON structure
    news_json = {
        "last_updated": datetime.now().strftime("%A, %B %d, %Y at %I:%M %p IST"),
        "last_updated_iso": datetime.now().isoformat(),
        "market": market,
        "categories": {}
    }
    
    # Add news by category
    for cat_name, cat_info in all_news.items():
        items_clean = []
        for item in cat_info['items']:
            items_clean.append({
                "title": item.get('title', ''),
                "summary": item.get('summary', item.get('description', ''))[:250],
                "link": item.get('link', ''),
                "source": item.get('source', '')
            })
        news_json["categories"][cat_name] = {
            "color": cat_info.get('color', '#ff6b00'),
            "items": items_clean
        }
    
    # Add videos as their own category
    if all_videos:
        videos_clean = []
        for vid in all_videos:
            videos_clean.append({
                "title": vid.get('title', ''),
                "summary": vid.get('summary', '')[:250],
                "link": vid.get('link', ''),
                "source": vid.get('channel', 'YouTube'),
                "thumbnail": vid.get('thumbnail', '')
            })
        news_json["categories"]["📺 TOP TECH VIDEOS"] = {
            "color": "#ff0000",
            "items": videos_clean
        }
    
    # Write to file
    try:
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(news_json, f, indent=2, ensure_ascii=False)
        print(f"  ✓ news.json saved ({len(news_json['categories'])} categories)")
    except Exception as e:
        print(f"  ✗ Failed: {e}")


if __name__ == "__main__":
    main()

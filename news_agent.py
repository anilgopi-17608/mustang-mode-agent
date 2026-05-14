"""
================================================================
TECH PIT STOP - DAILY NEWS DIGEST AGENT v1.0
================================================================
Tuned for: ANIL GOPI GUDAPATI
Sources:
  📰 ABN Telugu (Andhra Jyothy)
  📰 ETV Telugu (Eenadu)
  📺 Prasad Tech in Telugu (YouTube)

Runs every morning at 7:00 AM IST via GitHub Actions.
Sends a beautifully formatted news digest to your Gmail.
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

# Optional: Gemini AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# =====================================================
# LOAD SECRETS
# =====================================================

GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# =====================================================
# CONFIGURATION
# =====================================================

DIGEST_RECIPIENT = "anilgopi731@gmail.com"
SENDER_EMAIL = "anilgopi731@gmail.com"
USER_NAME = "Anil"

# News sources (RSS feeds)
NEWS_SOURCES = {
    "ABN Andhra Jyothy": {
        "rss": "https://rss.andhrajyothy.com/news/AndhraPradesh?SupId=0&SubId=43",
        "icon": "📰",
        "color": "#dc2626"
    },
    "NTV Telugu": {
        "rss": "https://ntvtelugu.com/feed",
        "icon": "📺",
        "color": "#0077b5"
    },
    "Mana Telangana": {
        "rss": "https://manatelangana.news/feed",
        "icon": "🟠",
        "color": "#16a34a"
    }
}

# YouTube channels (using YouTube's built-in RSS - no API key needed!)
YOUTUBE_CHANNELS = {
    "Prasad Tech in Telugu": {
        "channel_id": "UCb-xXZ7ltTvrh9C6DgB9H-Q",
        "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCb-xXZ7ltTvrh9C6DgB9H-Q",
        "icon": "📺",
        "color": "#ff0000"
    }
}

MAX_NEWS_PER_SOURCE = 5
MAX_VIDEOS = 3
USE_AI_SUMMARIES = bool(GEMINI_API_KEY) and GEMINI_AVAILABLE

# =====================================================
# GEMINI AI FOR SUMMARIES
# =====================================================

def init_gemini():
    """Initialize Gemini API"""
    if not USE_AI_SUMMARIES:
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("[OK] Gemini AI activated for summaries")
        return model
    except Exception as e:
        print(f"[WARN] Gemini init failed: {e}")
        return None


def ai_summarize(model, title, content):
    """Get AI summary of a news article"""
    if not model:
        return content[:200] + "..."
    
    prompt = f"""Summarize this Telugu/English news article in ONE simple English sentence (max 25 words). Be direct and informative.

Title: {title}
Content: {content[:500]}

Respond with ONLY the summary, no preamble."""
    
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        # Clean up
        summary = re.sub(r'^"|"$', '', summary)
        return summary[:200]
    except Exception as e:
        print(f"  [AI] Summary failed: {e}")
        return content[:200] + "..."


# =====================================================
# RSS FEED PARSING
# =====================================================

def fetch_rss(url, max_items=5):
    """Fetch and parse RSS feed"""
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
        
        # Try standard RSS format
        for item in root.iter('item'):
            if len(items) >= max_items:
                break
            
            title_elem = item.find('title')
            link_elem = item.find('link')
            desc_elem = item.find('description')
            pub_elem = item.find('pubDate')
            
            title = title_elem.text if title_elem is not None else "No title"
            link = link_elem.text if link_elem is not None else ""
            description = desc_elem.text if desc_elem is not None else ""
            pub_date = pub_elem.text if pub_elem is not None else ""
            
            # Clean HTML from description
            description = re.sub(r'<[^>]+>', ' ', description or '')
            description = re.sub(r'\s+', ' ', description).strip()
            
            items.append({
                'title': title or '',
                'link': link or '',
                'description': description[:500],
                'pub_date': pub_date or ''
            })
        
        # Try Atom format if no items found (YouTube uses this)
        if not items:
            ns = {'atom': 'http://www.w3.org/2005/Atom',
                  'media': 'http://search.yahoo.com/mrss/'}
            for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):
                if len(items) >= max_items:
                    break
                
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                link_elem = entry.find('{http://www.w3.org/2005/Atom}link')
                pub_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                
                # Try to get description from media:description
                desc = ""
                media_desc = entry.find('{http://search.yahoo.com/mrss/}group/{http://search.yahoo.com/mrss/}description')
                if media_desc is not None and media_desc.text:
                    desc = media_desc.text[:500]
                
                # YouTube thumbnail
                thumbnail = ""
                media_thumb = entry.find('{http://search.yahoo.com/mrss/}group/{http://search.yahoo.com/mrss/}thumbnail')
                if media_thumb is not None:
                    thumbnail = media_thumb.get('url', '')
                
                title = title_elem.text if title_elem is not None else "No title"
                link = link_elem.get('href', '') if link_elem is not None else ""
                pub_date = pub_elem.text if pub_elem is not None else ""
                
                items.append({
                    'title': title or '',
                    'link': link or '',
                    'description': desc,
                    'pub_date': pub_date or '',
                    'thumbnail': thumbnail
                })
        
        return items
    except Exception as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return []


# =====================================================
# BUILD HTML DIGEST
# =====================================================

def build_news_digest(news_data, video_data):
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    # Build news sections
    news_html = ""
    for source_name, source_info in news_data.items():
        items = source_info['items']
        if not items:
            continue
        
        cards = ""
        for i, item in enumerate(items, 1):
            summary = item.get('summary', item.get('description', ''))[:250]
            cards += f"""
            <div style='background:#ffffff; border:1px solid #e5e7eb; border-left:4px solid {source_info['color']}; border-radius:10px; padding:18px; margin-bottom:12px;'>
                <div style='font-size:10px; color:#9ca3af; letter-spacing:2px; font-weight:bold; margin-bottom:6px;'>STORY #{i}</div>
                <div style='color:#111827; font-size:15px; font-weight:bold; margin-bottom:8px; line-height:1.4;'>
                    {item['title']}
                </div>
                <div style='color:#4b5563; font-size:13px; line-height:1.6; margin:8px 0; padding:10px; background:#f9fafb; border-radius:6px;'>
                    💡 {summary}
                </div>
                <a href='{item['link']}' style='display:inline-block; color:{source_info['color']}; font-size:12px; font-weight:bold; text-decoration:none; margin-top:4px;'>
                    📖 Read full article →
                </a>
            </div>
            """
        
        news_html += f"""
        <div style='margin-bottom:24px;'>
            <div style='background:linear-gradient(135deg, {source_info['color']}, #000); color:#fff; padding:14px 20px; border-radius:10px; margin-bottom:14px; text-align:center;'>
                <div style='font-size:11px; letter-spacing:3px; font-weight:bold;'>{source_info['icon']} {source_name.upper()}</div>
                <div style='font-size:18px; font-weight:bold; margin-top:4px;'>Top {len(items)} Stories</div>
            </div>
            {cards}
        </div>
        """
    
    # Build YouTube videos section
    video_html = ""
    for channel_name, channel_info in video_data.items():
        videos = channel_info['items']
        if not videos:
            continue
        
        cards = ""
        for i, vid in enumerate(videos, 1):
            thumb = vid.get('thumbnail', '')
            desc = vid.get('summary', vid.get('description', 'New video uploaded'))[:200]
            
            thumb_html = ""
            if thumb:
                thumb_html = f"""
                <a href='{vid['link']}' style='display:block; text-align:center; margin-bottom:10px;'>
                    <img src='{thumb}' style='max-width:100%; border-radius:8px; border:2px solid #e5e7eb;' alt='Video thumbnail'>
                </a>
                """
            
            cards += f"""
            <div style='background:#ffffff; border:1px solid #e5e7eb; border-left:4px solid {channel_info['color']}; border-radius:10px; padding:18px; margin-bottom:12px;'>
                <div style='font-size:10px; color:#9ca3af; letter-spacing:2px; font-weight:bold; margin-bottom:6px;'>VIDEO #{i}</div>
                <div style='color:#111827; font-size:15px; font-weight:bold; margin-bottom:10px; line-height:1.4;'>
                    🎬 {vid['title']}
                </div>
                {thumb_html}
                <div style='color:#4b5563; font-size:13px; line-height:1.6; margin:8px 0; padding:10px; background:#f9fafb; border-radius:6px;'>
                    💡 {desc}
                </div>
                <a href='{vid['link']}' style='display:inline-block; background:linear-gradient(135deg, {channel_info['color']}, #c00); color:#fff; padding:10px 20px; border-radius:6px; font-size:12px; font-weight:bold; text-decoration:none; margin-top:6px;'>
                    ▶️ Watch on YouTube
                </a>
            </div>
            """
        
        video_html += f"""
        <div style='margin-bottom:24px;'>
            <div style='background:linear-gradient(135deg, {channel_info['color']}, #000); color:#fff; padding:14px 20px; border-radius:10px; margin-bottom:14px; text-align:center;'>
                <div style='font-size:11px; letter-spacing:3px; font-weight:bold;'>{channel_info['icon']} {channel_name.upper()}</div>
                <div style='font-size:18px; font-weight:bold; margin-top:4px;'>Latest {len(videos)} Videos</div>
            </div>
            {cards}
        </div>
        """
    
    total_stories = sum(len(s['items']) for s in news_data.values())
    total_videos = sum(len(c['items']) for c in video_data.values())
    
    html = f"""
    <html>
    <body style='margin:0; padding:0; background:#f3f4f6; font-family:Verdana, Arial, sans-serif;'>
        <div style='max-width:700px; margin:0 auto; padding:24px 16px;'>
            
            <!-- Header -->
            <div style='text-align:center; padding:32px 20px; background:linear-gradient(135deg, #1f1f1f 0%, #0a0a0a 100%); border-radius:16px; margin-bottom:24px; box-shadow:0 4px 12px rgba(0,0,0,0.15);'>
                <div style='font-size:32px; margin-bottom:6px;'>🌅</div>
                <h1 style='color:#ffffff; font-family:Verdana, Arial, sans-serif; letter-spacing:4px; margin:8px 0 0 0; font-size:24px; font-weight:bold;'>TECH PIT STOP</h1>
                <div style='color:#fbbf24; font-size:14px; letter-spacing:3px; margin-top:8px; font-weight:bold;'>MORNING DIGEST</div>
                <div style='color:#9ca3af; font-size:11px; letter-spacing:2px; margin-top:10px;'>{today.upper()}</div>
            </div>
            
            <!-- Greeting -->
            <div style='background:#ffffff; border-radius:12px; padding:20px 24px; margin-bottom:18px; border:1px solid #e5e7eb;'>
                <div style='color:#111827; font-size:15px; line-height:1.7;'>
                    Good morning <span style='color:#dc2626; font-weight:bold;'>{USER_NAME}</span>! ☕<br>
                    Here's what happened while you were sleeping:<br>
                    <span style='color:#16a34a; font-weight:bold;'>{total_stories} news stories</span> + 
                    <span style='color:#dc2626; font-weight:bold;'>{total_videos} new videos</span> from your favorite channels.
                </div>
            </div>
            
            <!-- Stats -->
            <table style='width:100%; border-collapse:separate; border-spacing:8px 0; margin-bottom:20px;'>
                <tr>
                    <td style='width:33%; background:#ffffff; border:1px solid #e5e7eb; padding:16px 8px; border-radius:10px; text-align:center;'>
                        <div style='color:#dc2626; font-size:24px; font-weight:bold;'>📰</div>
                        <div style='color:#111827; font-size:22px; font-weight:bold;'>{total_stories}</div>
                        <div style='color:#6b7280; font-size:10px; letter-spacing:1px; font-weight:600;'>NEWS STORIES</div>
                    </td>
                    <td style='width:33%; background:#ffffff; border:1px solid #e5e7eb; padding:16px 8px; border-radius:10px; text-align:center;'>
                        <div style='color:#dc2626; font-size:24px; font-weight:bold;'>📺</div>
                        <div style='color:#111827; font-size:22px; font-weight:bold;'>{total_videos}</div>
                        <div style='color:#6b7280; font-size:10px; letter-spacing:1px; font-weight:600;'>NEW VIDEOS</div>
                    </td>
                    <td style='width:33%; background:#ffffff; border:1px solid #e5e7eb; padding:16px 8px; border-radius:10px; text-align:center;'>
                        <div style='color:#16a34a; font-size:24px; font-weight:bold;'>🧠</div>
                        <div style='color:#111827; font-size:13px; font-weight:bold; margin-top:8px;'>AI-Summarized</div>
                        <div style='color:#6b7280; font-size:10px; letter-spacing:1px; font-weight:600;'>BY GEMINI</div>
                    </td>
                </tr>
            </table>
            
            <!-- News Section -->
            {news_html}
            
            <!-- Videos Section -->
            {video_html}
            
            <!-- Footer -->
            <div style='text-align:center; padding:24px 20px; margin-top:20px; background:#1f1f1f; border-radius:12px;'>
                <div style='color:#fbbf24; font-size:11px; letter-spacing:3px; font-weight:bold;'>🌅 STAY CURIOUS · LEARN DAILY 🚀</div>
                <div style='margin-top:10px; color:#6b7280; font-size:10px; letter-spacing:1px;'>☕ Tech Pit Stop · Sent automatically every morning</div>
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
    subject = f"🌅 Tech Pit Stop | {total_stories} stories + {total_videos} videos ({today})"
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"Tech Pit Stop AI <{SENDER_EMAIL}>"
    msg['To'] = DIGEST_RECIPIENT
    msg.attach(MIMEText(html_content, 'html'))
    
    print(f"Sending digest to {DIGEST_RECIPIENT}...")
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
    print("TECH PIT STOP v1.0 - MORNING NEWS DIGEST")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Initialize Gemini (optional - script works without it)
    model = init_gemini()
    
    # Fetch news from all sources (each is independent - one failing is OK)
    news_data = {}
    for source_name, source_info in NEWS_SOURCES.items():
        print(f"\n[NEWS] Fetching {source_name}...")
        try:
            items = fetch_rss(source_info['rss'], MAX_NEWS_PER_SOURCE)
            print(f"  Found {len(items)} stories")
            
            # AI-summarize each item (only if Gemini is available)
            if model and items:
                for item in items:
                    try:
                        item['summary'] = ai_summarize(model, item['title'], item['description'])
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  [AI] Skip summary for one item: {e}")
                        item['summary'] = item.get('description', '')[:200]
            
            news_data[source_name] = {
                'items': items,
                **source_info
            }
        except Exception as e:
            print(f"  [ERROR] Source {source_name} failed: {e}")
            news_data[source_name] = {
                'items': [],
                **source_info
            }
    
    # Fetch YouTube videos
    video_data = {}
    for channel_name, channel_info in YOUTUBE_CHANNELS.items():
        print(f"\n[VIDEO] Fetching {channel_name}...")
        try:
            items = fetch_rss(channel_info['rss'], MAX_VIDEOS)
            print(f"  Found {len(items)} videos")
            
            # AI-summarize video descriptions
            if model and items:
                for item in items:
                    try:
                        item['summary'] = ai_summarize(model, item['title'], item['description'])
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  [AI] Skip summary for one video: {e}")
                        item['summary'] = "New video uploaded - click to watch!"
            
            video_data[channel_name] = {
                'items': items,
                **channel_info
            }
        except Exception as e:
            print(f"  [ERROR] Channel {channel_name} failed: {e}")
            video_data[channel_name] = {
                'items': [],
                **channel_info
            }
    
    # Build digest
    total_stories = sum(len(s['items']) for s in news_data.values())
    total_videos = sum(len(c['items']) for c in video_data.values())
    
    print(f"\n{'=' * 60}")
    print(f"DIGEST: {total_stories} stories + {total_videos} videos")
    print(f"{'=' * 60}")
    
    if total_stories == 0 and total_videos == 0:
        print("[WARN] Nothing to send - all sources empty!")
        print("Sending minimal digest anyway to confirm pipeline works...")
    
    html = build_news_digest(news_data, video_data)
    send_digest(html, total_stories, total_videos)
    
    print("\nMorning digest complete! ☕")


if __name__ == "__main__":
    main()

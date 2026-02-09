"""Content processor - URL metadata extraction and tagging"""
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from functools import lru_cache

# Domain to tag mappings
DOMAIN_TAGS = {
    "youtube.com": "#video", "youtu.be": "#video", "vimeo.com": "#video",
    "tiktok.com": "#video", "instagram.com": "#social", "twitter.com": "#social",
    "x.com": "#social", "medium.com": "#article", "dev.to": "#article",
    "github.com": "#code", "stackoverflow.com": "#qa", "reddit.com": "#discussion"
}

# Keyword to tag mappings
KEYWORD_TAGS = {
    "docker": "#docker", "kubernetes": "#k8s", "aws": "#cloud", "python": "#python",
    "javascript": "#javascript", "react": "#react", "ai": "#ai", "ml": "#ml",
    "database": "#database", "api": "#api", "security": "#security"
}

def process_url(url: str) -> dict:
    """Process URL and extract metadata"""
    try:
        response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text[:50000], 'html.parser')
            
            # Extract title
            title = ""
            og_title = soup.find('meta', property='og:title')
            if og_title:
                title = og_title.get('content', '')
            elif soup.title:
                title = soup.title.string
            
            # Extract description
            desc = ""
            og_desc = soup.find('meta', property='og:description')
            if og_desc:
                desc = og_desc.get('content', '')
            
            title = title.strip() if title else extract_title_from_url(url)
            
            # Generate filename and tags
            filename = generate_filename(title)
            tags = generate_tags(url, title, desc)
            
            return {
                'title': title,
                'description': desc,
                'filename': filename,
                'tags': tags,
                'url': url
            }
    except:
        pass
    
    # Fallback
    title = extract_title_from_url(url)
    return {
        'title': title,
        'description': '',
        'filename': generate_filename(title),
        'tags': generate_tags(url, title, ''),
        'url': url
    }

def process_text(text: str) -> dict:
    """Process plain text"""
    lines = text.split('\n', 1)
    title = lines[0][:100] if lines else "Note"
    desc = lines[1][:200] if len(lines) > 1 else ""
    
    return {
        'title': title,
        'description': desc,
        'filename': generate_filename(title),
        'tags': generate_tags('', title, text),
        'url': ''
    }

def extract_title_from_url(url: str) -> str:
    """Extract title from URL"""
    try:
        parsed = urlparse(url)
        path = unquote(parsed.path)
        segments = [s for s in path.split('/') if s]
        title = segments[-1] if segments else parsed.netloc
        title = re.sub(r'\.\w+$', '', title)
        title = title.replace('-', ' ').replace('_', ' ')
        return title.title() if title else "Untitled"
    except:
        return "Untitled"

@lru_cache(maxsize=256)
def extract_keywords(text: str) -> tuple:
    """Extract keywords from text"""
    if not text:
        return ("note",)
    
    text_lower = text.lower()
    text_clean = re.sub(r'[^\w\s]', ' ', text_lower)
    words = text_clean.split()
    
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'can', 'this', 'that'
    }
    
    keywords = []
    for word in words:
        if len(word) > 2 and word not in stop_words and word not in keywords:
            keywords.append(word)
            if len(keywords) >= 3:
                break
    
    return tuple(keywords) if keywords else ("note",)

def generate_filename(title: str) -> str:
    """Generate filename"""
    keywords = extract_keywords(title)
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    if len(keywords) >= 2:
        filename = f"{keywords[0]}-{keywords[1]}-{date_str}.md"
    else:
        filename = f"{keywords[0]}-{date_str}.md"
    
    filename = re.sub(r'[^\w\-\.]', '-', filename)
    filename = re.sub(r'-+', '-', filename).strip('-')
    
    return filename.lower()

def generate_tags(url: str, title: str, content: str) -> list:
    """Generate tags"""
    tags = set()
    text = f"{title} {content}".lower()
    
    # Domain tags
    if url:
        domain = urlparse(url).netloc.lower().replace('www.', '')
        for d, tag in DOMAIN_TAGS.items():
            if d in domain:
                tags.add(tag)
                break
    
    # Keyword tags
    for keyword, tag in KEYWORD_TAGS.items():
        if keyword in text:
            tags.add(tag)
    
    # Content type
    if not url:
        tags.add("#note")
    elif not tags:
        tags.add("#article")
    
    # Length tag
    if len(content) > 5000:
        tags.add("#long-read")
    
    # Year tag
    tags.add(f"#{datetime.now().year}")
    
    return sorted(list(tags))

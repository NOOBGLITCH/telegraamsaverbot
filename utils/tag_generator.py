"""
Advanced tag generation with intelligent keyword extraction
Uses NLP-inspired techniques for better, more relevant tags
"""

import re
from typing import List, Set, Optional, Dict, Tuple
from urllib.parse import urlparse
from collections import Counter
import config


# Enhanced stop words (expanded list)
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
    'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
    'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 'just', 'about', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'between',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'also',
    'available', 'description', 'content', 'title', 'link', 'url'
}

# Domain-based tag mapping with priority tags
DOMAIN_TAGS = {
    'youtube.com': ['Video', 'YT', 'YouTube'],
    'youtu.be': ['Video', 'YT', 'YouTube'],
    'github.com': ['Code', 'GitHub', 'Dev'],
    'stackoverflow.com': ['Programming', 'QA'],
    'medium.com': ['Article', 'Blog'],
    'twitter.com': ['Social', 'Twitter'],
    'x.com': ['Social', 'Twitter'],
    'reddit.com': ['Discussion', 'Reddit'],
    'wikipedia.org': ['Reference', 'Wiki'],
    'arxiv.org': ['Research', 'Paper', 'Academic'],
    'news.ycombinator.com': ['Tech', 'News'],
    'dev.to': ['Development', 'Blog'],
    'linkedin.com': ['Professional', 'Network'],
    'instagram.com': ['Social', 'Photo'],
    'tiktok.com': ['Video', 'Social'],
    'spotify.com': ['Music', 'Audio'],
    'soundcloud.com': ['Music', 'Audio'],
}

# High-value keywords (weighted higher in scoring)
PRIORITY_KEYWORDS = {
    # Programming languages
    'python': 'Python', 'javascript': 'JavaScript', 'java': 'Java', 
    'typescript': 'TypeScript', 'rust': 'Rust', 'go': 'Go', 'golang': 'Go',
    'cpp': 'CPP', 'csharp': 'CSharp', 'ruby': 'Ruby', 'php': 'PHP',
    'swift': 'Swift', 'kotlin': 'Kotlin', 'scala': 'Scala',
    
    # Frameworks & Libraries
    'react': 'React', 'vue': 'Vue', 'angular': 'Angular', 'svelte': 'Svelte',
    'nextjs': 'NextJS', 'django': 'Django', 'flask': 'Flask', 'fastapi': 'FastAPI',
    'express': 'Express', 'nestjs': 'NestJS', 'spring': 'Spring',
    
    # DevOps & Cloud
    'docker': 'Docker', 'kubernetes': 'K8s', 'aws': 'AWS', 'azure': 'Azure',
    'gcp': 'GCP', 'cloud': 'Cloud', 'devops': 'DevOps', 'cicd': 'CICD',
    'terraform': 'Terraform', 'ansible': 'Ansible',
    
    # AI/ML
    'ai': 'AI', 'ml': 'ML', 'machinelearning': 'MachineLearning',
    'deeplearning': 'DeepLearning', 'neuralnetwork': 'NeuralNetwork',
    'tensorflow': 'TensorFlow', 'pytorch': 'PyTorch', 'llm': 'LLM',
    'gpt': 'GPT', 'chatgpt': 'ChatGPT', 'openai': 'OpenAI',
    
    # Blockchain & Crypto
    'blockchain': 'Blockchain', 'crypto': 'Crypto', 'bitcoin': 'Bitcoin',
    'ethereum': 'Ethereum', 'web3': 'Web3', 'nft': 'NFT', 'defi': 'DeFi',
    
    # Databases
    'database': 'Database', 'sql': 'SQL', 'nosql': 'NoSQL', 'mongodb': 'MongoDB',
    'postgresql': 'PostgreSQL', 'mysql': 'MySQL', 'redis': 'Redis',
    
    # General Tech
    'api': 'API', 'rest': 'REST', 'graphql': 'GraphQL', 'websocket': 'WebSocket',
    'frontend': 'Frontend', 'backend': 'Backend', 'fullstack': 'FullStack',
    'mobile': 'Mobile', 'ios': 'iOS', 'android': 'Android',
    
    # Content types
    'tutorial': 'Tutorial', 'guide': 'Guide', 'course': 'Course',
    'documentation': 'Docs', 'review': 'Review', 'news': 'News',
    'interview': 'Interview', 'podcast': 'Podcast', 'webinar': 'Webinar',
}

# Category keywords for context
CATEGORY_KEYWORDS = {
    'gaming': ['game', 'gaming', 'gamer', 'gameplay', 'esports', 'streamer'],
    'music': ['music', 'song', 'album', 'artist', 'band', 'concert', 'audio'],
    'education': ['learn', 'tutorial', 'course', 'education', 'teaching', 'study'],
    'business': ['business', 'startup', 'entrepreneur', 'marketing', 'sales'],
    'health': ['health', 'fitness', 'workout', 'nutrition', 'wellness', 'medical'],
    'science': ['science', 'research', 'study', 'experiment', 'discovery'],
    'entertainment': ['movie', 'film', 'show', 'series', 'entertainment', 'comedy'],
    'news': ['news', 'breaking', 'update', 'report', 'announcement'],
    'sports': ['sports', 'football', 'basketball', 'soccer', 'cricket', 'athlete'],
}


def generate_tags(
    title: str = '',
    description: str = '',
    caption: str = '',
    media_type: Optional[str] = None,
    url: Optional[str] = None
) -> List[str]:
    """
    Generate intelligent, relevant tags using advanced keyword extraction
    
    Algorithm:
    1. Extract domain-specific tags (highest priority)
    2. Score keywords using TF-IDF-like approach
    3. Detect categories and add contextual tags
    4. Filter and rank by relevance
    5. Return top 5-6 most relevant tags
    
    Args:
        title: Content title (highest weight)
        description: Content description (medium weight)
        caption: User caption (medium weight)
        media_type: Type of media
        url: Original URL
        
    Returns:
        List of 5-6 most relevant hashtags
    """
    tags: Set[str] = set()
    max_tags = 6
    
    # Priority 1: Domain-based tags (always include for known domains)
    if url:
        domain_tags = _get_domain_tags(url)
        # Take first 3 domain tags max to leave room for content tags
        for tag in domain_tags[:3]:
            tags.add(tag)
    
    # Priority 2: Extract and score keywords from content
    keyword_scores = _extract_scored_keywords(title, description, caption)
    
    # Priority 3: Add high-value tech/topic keywords
    for keyword, score in keyword_scores:
        if len(tags) >= max_tags:
            break
        
        # Check if it's a priority keyword
        normalized_keyword = keyword.lower().replace(' ', '')
        if normalized_keyword in PRIORITY_KEYWORDS:
            tag = PRIORITY_KEYWORDS[normalized_keyword]
            if tag not in tags:
                tags.add(tag)
        else:
            # Regular keyword
            tag = _normalize_tag(keyword)
            if tag and tag not in tags and len(tag) >= 3:
                tags.add(tag)
    
    # Priority 4: Add category tag if detected
    if len(tags) < max_tags:
        category = _detect_category(f"{title} {description} {caption}".lower())
        if category:
            tag = category.capitalize()
            if tag not in tags:
                tags.add(tag)
    
    # Priority 5: Add media type if not covered
    if media_type and len(tags) < max_tags:
        media_tag = _get_media_tag(media_type)
        if media_tag and media_tag not in tags:
            tags.add(media_tag)
    
    # Convert to hashtag list
    tag_list = [f"#{tag}" for tag in list(tags)[:max_tags]]
    
    # Ensure at least one tag
    if not tag_list:
        tag_list = ['#Content']
    
    return tag_list


def _extract_scored_keywords(title: str, description: str, caption: str) -> List[Tuple[str, float]]:
    """
    Extract keywords with TF-IDF-like scoring
    Title words get 3x weight, description 1.5x, caption 1x
    """
    # Tokenize and weight
    title_words = _tokenize(title)
    desc_words = _tokenize(description)
    caption_words = _tokenize(caption)
    
    # Count with weights
    word_scores: Dict[str, float] = {}
    
    for word in title_words:
        word_scores[word] = word_scores.get(word, 0) + 3.0
    
    for word in desc_words:
        word_scores[word] = word_scores.get(word, 0) + 1.5
    
    for word in caption_words:
        word_scores[word] = word_scores.get(word, 0) + 1.0
    
    # Boost priority keywords
    for word in word_scores:
        normalized = word.lower().replace(' ', '')
        if normalized in PRIORITY_KEYWORDS:
            word_scores[word] *= 2.0
    
    # Sort by score
    sorted_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_keywords[:15]  # Top 15 candidates


def _tokenize(text: str) -> List[str]:
    """Extract meaningful words from text"""
    if not text:
        return []
    
    # Extract words (3+ chars, alphanumeric)
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]{2,}\b', text)
    
    # Filter stop words
    filtered = [w for w in words if w.lower() not in STOP_WORDS]
    
    return filtered


def _detect_category(text: str) -> Optional[str]:
    """Detect content category from keywords"""
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category
    return None


def _get_domain_tags(url: str) -> List[str]:
    """Get tags based on URL domain"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        if domain.startswith('www.'):
            domain = domain[4:]
        
        for domain_pattern, tags in DOMAIN_TAGS.items():
            if domain_pattern in domain:
                return tags if isinstance(tags, list) else [tags]
                
    except Exception:
        pass
    
    return []


def _get_media_tag(media_type: str) -> Optional[str]:
    """Get tag based on media type"""
    media_map = {
        'photo': 'Image',
        'video': 'Video',
        'audio': 'Audio',
        'voice': 'Voice',
        'document': 'Document',
        'animation': 'GIF',
        'sticker': 'Sticker'
    }
    return media_map.get(media_type.lower())


def _normalize_tag(tag: str) -> Optional[str]:
    """Normalize tag to proper hashtag format"""
    # Remove special characters
    normalized = re.sub(r'[^a-zA-Z0-9]', '', tag)
    
    # Capitalize properly (preserve camelCase if exists)
    if normalized and not normalized[0].isupper():
        normalized = normalized.capitalize()
    
    return normalized if len(normalized) >= 3 else None

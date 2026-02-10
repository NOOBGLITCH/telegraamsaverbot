"""
URL extraction and validation utilities
"""

import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Optional, List
from .. import config


def extract_urls(text: str) -> List[str]:
    """
    Extract all HTTP/HTTPS URLs from text
    
    Args:
        text: Input text containing potential URLs
        
    Returns:
        List of valid URLs found in text
    """
    if not text:
        return []
    
    # Regex pattern for HTTP/HTTPS URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    
    urls = re.findall(url_pattern, text)
    
    # Validate and clean URLs
    valid_urls = []
    for url in urls:
        if is_valid_url(url):
            cleaned = clean_url(url)
            if cleaned:
                valid_urls.append(cleaned)
    
    return valid_urls


def is_valid_url(url: str) -> bool:
    """
    Validate if URL is properly formed and not pointing to private IPs
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL is valid and safe
    """
    try:
        parsed = urlparse(url)
        
        # Must have scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # Only HTTP/HTTPS
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check for blocked IP patterns (security)
        hostname = parsed.hostname or parsed.netloc
        for pattern in config.BLOCKED_IP_PATTERNS:
            if re.match(pattern, hostname, re.IGNORECASE):
                return False
        
        return True
        
    except Exception:
        return False


def clean_url(url: str) -> Optional[str]:
    """
    Remove tracking parameters and clean URL
    
    Args:
        url: URL to clean
        
    Returns:
        Cleaned URL or None if invalid
    """
    try:
        parsed = urlparse(url)
        
        # Common tracking parameters to remove
        tracking_params = {
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
            'fbclid', 'gclid', 'msclkid', 'mc_cid', 'mc_eid',
            '_ga', '_gl', 'ref', 'source'
        }
        
        # Parse query parameters
        query_params = parse_qs(parsed.query)
        
        # Remove tracking parameters
        cleaned_params = {
            k: v for k, v in query_params.items() 
            if k.lower() not in tracking_params
        }
        
        # Rebuild query string
        new_query = urlencode(cleaned_params, doseq=True)
        
        # Reconstruct URL
        cleaned = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            ''  # Remove fragment
        ))
        
        return cleaned
        
    except Exception:
        return url  # Return original if cleaning fails


def get_first_valid_url(text: str) -> Optional[str]:
    """
    Get the first valid URL from text
    
    Args:
        text: Input text
        
    Returns:
        First valid URL or None
    """
    urls = extract_urls(text)
    return urls[0] if urls else None

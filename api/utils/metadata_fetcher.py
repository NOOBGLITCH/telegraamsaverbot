"""
Metadata fetching from URLs
Extracts title and description using Open Graph tags and HTML meta tags
"""

import httpx
from bs4 import BeautifulSoup
from typing import Dict, Optional
import config


async def fetch_metadata(url: str) -> Dict[str, str]:
    """
    Fetch metadata (title, description) from URL
    
    Priority order:
    1. Open Graph tags (og:title, og:description)
    2. HTML meta tags
    3. <title> element
    4. Fallback values
    
    Args:
        url: URL to fetch metadata from
        
    Returns:
        Dictionary with 'title' and 'description' keys
    """
    metadata = {
        'title': 'Untitled Content',
        'description': 'No description available'
    }
    
    try:
        async with httpx.AsyncClient(
            timeout=config.METADATA_TIMEOUT,
            follow_redirects=True,
            headers={'User-Agent': config.USER_AGENT}
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Only process HTML content
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                return metadata
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract title
            title = _extract_title(soup)
            if title:
                metadata['title'] = title
            
            # Extract description
            description = _extract_description(soup)
            if description:
                metadata['description'] = description
                
    except httpx.TimeoutException:
        # Timeout - use fallback
        pass
    except httpx.HTTPStatusError:
        # HTTP error - use fallback
        pass
    except Exception:
        # Any other error - use fallback
        pass
    
    return metadata


def _extract_title(soup: BeautifulSoup) -> Optional[str]:
    """
    Extract title from HTML with priority order
    
    Args:
        soup: BeautifulSoup object
        
    Returns:
        Extracted title or None
    """
    # 1. Try Open Graph title
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        return og_title['content'].strip()
    
    # 2. Try Twitter title
    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if twitter_title and twitter_title.get('content'):
        return twitter_title['content'].strip()
    
    # 3. Try regular meta title
    meta_title = soup.find('meta', attrs={'name': 'title'})
    if meta_title and meta_title.get('content'):
        return meta_title['content'].strip()
    
    # 4. Try <title> tag
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        return title_tag.string.strip()
    
    return None


def _extract_description(soup: BeautifulSoup) -> Optional[str]:
    """
    Extract description from HTML with priority order
    
    Args:
        soup: BeautifulSoup object
        
    Returns:
        Extracted description or None
    """
    # 1. Try Open Graph description
    og_desc = soup.find('meta', property='og:description')
    if og_desc and og_desc.get('content'):
        return og_desc['content'].strip()
    
    # 2. Try Twitter description
    twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
    if twitter_desc and twitter_desc.get('content'):
        return twitter_desc['content'].strip()
    
    # 3. Try regular meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        return meta_desc['content'].strip()
    
    return None

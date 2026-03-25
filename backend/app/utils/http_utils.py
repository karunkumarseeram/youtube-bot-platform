"""
HTTP Utilities
Python 3.14.3 Compatible
"""

import random
from typing import Optional, Dict
import requests
import logging

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]


def get_random_user_agent() -> str:
    """Get random user agent"""
    return random.choice(USER_AGENTS)


def get_headers(use_proxy: bool = False) -> Dict[str, str]:
    """Get HTTP headers with random user agent"""
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
    }


def make_request(
    url: str,
    method: str = "GET",
    use_proxy: bool = False,
    timeout: int = 10,
    **kwargs
) -> Optional[requests.Response]:
    """Make HTTP request with random headers"""
    headers = get_headers()
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        return response
    
    except requests.Timeout:
        logger.error(f"Request timeout: {url}")
        return None
    
    except requests.ConnectionError:
        logger.error(f"Connection error: {url}")
        return None
    
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        return None
"""
Proxy Management Utilities
Python 3.14.3 Compatible
"""

import requests
import random
from typing import List, Optional
import logging

from app.utils.logger import get_logger
from app.config import get_settings

logger = get_logger(__name__)
settings = get_settings()


class ProxyManager:
    """Manage proxy servers"""
    
    def __init__(self):
        self.proxies: List[str] = []
        self.current_index = 0
    
    def fetch_free_proxies(self, limit: int = 10) -> List[str]:
        """Fetch free proxies from public sources"""
        try:
            response = requests.get(
                settings.proxy_list_url,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                proxies = [
                    f"http://{item['ip']}:{item['port']}"
                    for item in data.get('LISTA', [])[:limit]
                ]
                self.proxies = proxies
                logger.info(f"✅ Fetched {len(proxies)} proxies")
                return proxies
        
        except Exception as e:
            logger.error(f"❌ Error fetching proxies: {str(e)}")
        
        return []
    
    def get_random_proxy(self) -> Optional[str]:
        """Get random proxy from list"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def get_next_proxy(self) -> Optional[str]:
        """Get next proxy in rotation"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy


# Global proxy manager instance
proxy_manager = ProxyManager()
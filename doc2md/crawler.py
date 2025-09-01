"""
Web Crawler Module

Handles crawling of web documents with configurable depth control
and domain restriction.
"""

import requests
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
from typing import Set, List, Dict, Optional
import time
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)


class WebCrawler:
    """Web crawler for discovering and crawling document pages."""
    
    def __init__(self, base_url: str, max_depth: int = 0, delay: float = 1.0, exclude_urls: List[str] = None):
        """
        Initialize the web crawler.
        
        Args:
            base_url: The root URL of the document site
            max_depth: Maximum depth to crawl (0 for unlimited)
            delay: Delay between requests in seconds
            exclude_urls: List of URLs or URL patterns to exclude from crawling
        """
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.base_path = urlparse(base_url).path
        self.max_depth = max_depth
        self.delay = delay
        self.exclude_urls = exclude_urls or []
        
        # Normalize exclude URLs
        self.exclude_patterns = [self.normalize_url(url) for url in self.exclude_urls]
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Doc2MD/1.0)'
        })
        
        # Track discovered URLs and their depths
        self.discovered_urls: Set[str] = set()
        self.url_depths: Dict[str, int] = {}
        self.url_titles: Dict[str, str] = {}
        self.url_links: Dict[str, List[str]] = {}
        
    def is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain and path scope."""
        parsed = urlparse(url)
        
        # Check domain first
        if parsed.netloc != self.domain:
            return False
        
        # Check if URL path starts with the base URL path
        # This ensures we only crawl URLs under the specified path
        if self.base_path and self.base_path != '/':
            if not parsed.path.startswith(self.base_path):
                return False
        
        return True
    
    def is_excluded(self, url: str) -> bool:
        """Check if URL should be excluded from crawling."""
        normalized_url = self.normalize_url(url)
        
        # Check if the URL matches any exclude pattern
        for exclude_pattern in self.exclude_patterns:
            # Check exact match
            if normalized_url == exclude_pattern:
                return True
            
            # Check if URL starts with exclude pattern (for path-based exclusion)
            if exclude_pattern.endswith('/') and normalized_url.startswith(exclude_pattern):
                return True
            
            # Check if exclude pattern ends with / and URL starts with it
            if not exclude_pattern.endswith('/') and normalized_url.startswith(exclude_pattern + '/'):
                return True
        
        return False
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragments and query parameters."""
        parsed = urlparse(url)
        # Remove fragment and query parameters for cleaner URLs
        clean_parsed = parsed._replace(fragment='', query='')
        return urlunparse(clean_parsed)
    
    def extract_links(self, html_content: str, base_url: str) -> List[str]:
        """Extract all links from HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            # Only include same-domain links that are not excluded
            if self.is_same_domain(absolute_url) and not self.is_excluded(absolute_url):
                normalized_url = self.normalize_url(absolute_url)
                links.append(normalized_url)
        
        return links
    
    def extract_title(self, html_content: str) -> str:
        """Extract page title from HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Try to get title from various sources
        title = soup.find('title')
        if title:
            return title.get_text().strip()
        
        # Fallback to first h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        # Fallback to first h2
        h2 = soup.find('h2')
        if h2:
            return h2.get_text().strip()
        
        return "Untitled"
    
    def crawl_page(self, url: str, depth: int) -> Optional[str]:
        """Crawl a single page and return its HTML content."""
        try:
            # Check if URL should be excluded
            if self.is_excluded(url):
                logger.info(f"Skipping excluded URL: {url}")
                return None
            
            logger.info(f"Crawling {url} at depth {depth}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Store page information
            self.discovered_urls.add(url)
            self.url_depths[url] = depth
            self.url_titles[url] = self.extract_title(response.text)
            
            # Extract links for further crawling
            links = self.extract_links(response.text, url)
            self.url_links[url] = links
            
            return response.text
            
        except requests.RequestException as e:
            logger.error(f"Failed to crawl {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error crawling {url}: {e}")
            return None
    
    def crawl(self) -> Dict[str, str]:
        """
        Crawl the entire document site.
        
        Returns:
            Dictionary mapping URLs to their HTML content
        """
        logger.info(f"Starting crawl of {self.base_url} with max depth {self.max_depth}")
        
        # Start with the base URL
        to_crawl = [(self.base_url, 0)]
        crawled_content = {}
        
        with tqdm(desc="Crawling pages", unit="page") as pbar:
            while to_crawl:
                current_url, current_depth = to_crawl.pop(0)
                
                # Skip if already crawled
                if current_url in self.discovered_urls:
                    continue
                
                # Check depth limit
                if self.max_depth > 0 and current_depth > self.max_depth:
                    continue
                
                # Crawl the page
                content = self.crawl_page(current_url, current_depth)
                if content:
                    crawled_content[current_url] = content
                    pbar.update(1)
                    
                    # Add discovered links to crawl queue
                    if current_url in self.url_links:
                        for link in self.url_links[current_url]:
                            if link not in self.discovered_urls:
                                to_crawl.append((link, current_depth + 1))
                
                # Respect delay between requests
                if self.delay > 0:
                    time.sleep(self.delay)
        
        logger.info(f"Crawling completed. Discovered {len(self.discovered_urls)} pages.")
        return crawled_content
    
    def get_site_structure(self) -> Dict[str, any]:
        """Get the complete site structure information."""
        return {
            'base_url': self.base_url,
            'domain': self.domain,
            'max_depth': self.max_depth,
            'total_pages': len(self.discovered_urls),
            'urls': list(self.discovered_urls),
            'url_depths': self.url_depths,
            'url_titles': self.url_titles,
            'url_links': self.url_links
        }

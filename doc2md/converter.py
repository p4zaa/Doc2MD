"""
Main Document Converter Module

Orchestrates the entire conversion process from web crawling to
markdown generation and folder structure creation.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

from .crawler import WebCrawler
from .markdown_generator import MarkdownGenerator
from .link_tree import LinkTreeGenerator

logger = logging.getLogger(__name__)


class DocumentConverter:
    """Main class for converting web documents to markdown format."""
    
    def __init__(self, base_url: str, output_dir: str = "docs", 
                 max_depth: int = 0, delay: float = 1.0, exclude_urls: List[str] = None,
                 force_triple_backticks: bool = True, debug: bool = False, 
                 generate_readme: bool = True, raw_output: bool = False,
                 ai_optimization_level: str = "standard", reduce_empty_lines: bool = True):
        """
        Initialize the document converter.
        
        Args:
            base_url: Root URL of the document site to convert
            output_dir: Output directory for generated markdown files
            max_depth: Maximum depth to crawl (0 for unlimited)
            delay: Delay between requests in seconds
            exclude_urls: List of URLs or URL patterns to exclude from crawling
            force_triple_backticks: Whether to force triple backticks (```) instead of [code] syntax
            debug: Whether to enable debug logging for troubleshooting
            generate_readme: Whether to generate README.md files for navigation
            raw_output: Whether to output raw markdown without any cleaning or fixing
            ai_optimization_level: Level of AI optimization ("minimal", "standard", "enhanced")
            reduce_empty_lines: Whether to reduce consecutive empty lines to single lines (default: True)
        """
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.max_depth = max_depth
        self.delay = delay
        self.exclude_urls = exclude_urls or []
        self.force_triple_backticks = force_triple_backticks
        self.debug = debug
        self.generate_readme = generate_readme
        self.raw_output = raw_output
        self.ai_optimization_level = ai_optimization_level
        self.reduce_empty_lines = reduce_empty_lines
        
        # Initialize components
        self.crawler = WebCrawler(base_url, max_depth, delay, self.exclude_urls)
        self.markdown_generator = MarkdownGenerator(base_url, optimize_for_ai=True, raw_output=self.raw_output, ai_optimization_level=self.ai_optimization_level, force_triple_backticks=self.force_triple_backticks, reduce_empty_lines=self.reduce_empty_lines)
        self.link_tree_generator = LinkTreeGenerator(base_url, output_dir)
        
        # Conversion results
        self.crawled_content: Dict[str, str] = {}
        self.url_mapping: Dict[str, str] = {}
        self.site_structure: Dict[str, any] = {}
        
        # Create output directory first
        self._create_output_directory()
        
        # Setup logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration."""
        log_level = logging.DEBUG if self.debug else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.output_dir / 'conversion.log')
            ]
        )
        

        
    def _create_output_directory(self):
        """Create the output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {self.output_dir.absolute()}")
        
    def _generate_file_paths(self) -> Dict[str, str]:
        """
        Generate local file paths for each crawled URL.
        
        Returns:
            Mapping of URLs to local file paths
        """
        url_mapping = {}
        
        for url in self.crawler.discovered_urls:
            # Generate filename from URL
            filename = self.markdown_generator.get_filename_from_url(url)
            
            # Determine folder structure based on URL path
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) > 1 and path_parts[-1]:
                # URL has a path, create nested folders
                folder_path = '/'.join(path_parts[:-1])
                folder_path = folder_path.replace('-', '_').replace(' ', '_')
                
                # Handle special characters in folder names
                folder_path = self._sanitize_path(folder_path)
                
                if folder_path:
                    local_path = f"{folder_path}/{filename}.md"
                else:
                    local_path = f"{filename}.md"
            else:
                # Root URL or URL ending with /
                local_path = f"{filename}.md"
            
            url_mapping[url] = local_path
            
        return url_mapping
    
    def _sanitize_path(self, path: str) -> str:
        """Sanitize path by removing/replacing invalid characters."""
        import re
        # Replace invalid characters with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9\-_/]', '_', path)
        # Remove multiple consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        return sanitized
    
    def _save_markdown_files(self):
        """Save all converted markdown files to disk."""
        logger.info("Saving markdown files...")
        
        for url, local_path in self.url_mapping.items():
            if url in self.crawled_content:
                # Convert HTML to markdown
                markdown_content = self.markdown_generator.generate_markdown(
                    self.crawled_content[url], 
                    url, 
                    self.url_mapping
                )
                
                # Create full file path
                file_path = self.output_dir / local_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the file
                file_path.write_text(markdown_content, encoding='utf-8')
                logger.info(f"Saved: {local_path}")
        
        logger.info(f"All markdown files saved successfully!")
    
    def convert(self) -> Dict[str, any]:
        """
        Perform the complete conversion process.
        
        Returns:
            Dictionary containing conversion results and statistics
        """
        logger.info(f"Starting conversion of {self.base_url}")
        logger.info(f"Max depth: {self.max_depth if self.max_depth > 0 else 'Unlimited'}")
        
        try:
            # Step 1: Create output directory
            self._create_output_directory()
            
            # Step 2: Crawl the website
            logger.info("Step 1: Crawling website...")
            self.crawled_content = self.crawler.crawl()
            
            if not self.crawled_content:
                raise RuntimeError("No content was crawled. Please check the URL and try again.")
            
            # Step 3: Get site structure information
            self.site_structure = self.crawler.get_site_structure()
            
            # Step 4: Generate file paths
            logger.info("Step 2: Generating file structure...")
            self.url_mapping = self._generate_file_paths()
            
            # Step 5: Convert and save markdown files
            logger.info("Step 3: Converting to markdown...")
            self._save_markdown_files()
            
            # Step 6: Generate navigation and README files (if enabled)
            if self.generate_readme:
                logger.info("Step 4: Generating navigation...")
                self.link_tree_generator.create_all_readmes(
                    self.url_mapping, 
                    self.site_structure
                )
            else:
                logger.info("Step 4: Skipping README generation (disabled)")
            
            # Step 7: Generate conversion summary
            summary = self._generate_summary()
            
            logger.info("Conversion completed successfully!")
            return summary
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise
    
    def _generate_summary(self) -> Dict[str, any]:
        """Generate a summary of the conversion process."""
        return {
            'status': 'success',
            'base_url': self.base_url,
            'output_directory': str(self.output_dir.absolute()),
            'total_pages_crawled': len(self.crawled_content),
            'total_files_generated': len(self.url_mapping),
            'crawl_depth': self.max_depth,
            'site_structure': self.site_structure,
            'url_mapping': self.url_mapping,
            'conversion_timestamp': self._get_current_timestamp()
        }
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_conversion_stats(self) -> Dict[str, any]:
        """Get statistics about the conversion process."""
        return {
            'base_url': self.base_url,
            'output_directory': str(self.output_dir.absolute()),
            'crawled_pages': len(self.crawled_content),
            'generated_files': len(self.url_mapping),
            'crawl_depth': self.max_depth,
            'site_domain': urlparse(self.base_url).netloc
        }
    
    def validate_url(self) -> bool:
        """Validate that the base URL is accessible."""
        try:
            response = self.crawler.session.get(self.base_url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"URL validation failed: {e}")
            return False
    
    def preview_conversion(self) -> Dict[str, any]:
        """
        Preview what the conversion would look like without actually converting.
        
        Returns:
            Preview information including estimated file count and structure
        """
        logger.info("Generating conversion preview...")
        
        # Test crawl a few pages to get an estimate
        test_crawler = WebCrawler(self.base_url, min(self.max_depth, 2), self.delay)
        test_content = test_crawler.crawl()
        
        if not test_content:
            return {'error': 'Could not access the website'}
        
        # Generate sample file paths
        sample_mapping = {}
        for url in test_crawler.discovered_urls:
            filename = self.markdown_generator.get_filename_from_url(url)
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) > 1 and path_parts[-1]:
                folder_path = '/'.join(path_parts[:-1])
                folder_path = self._sanitize_path(folder_path)
                if folder_path:
                    local_path = f"{folder_path}/{filename}.md"
                else:
                    local_path = f"{filename}.md"
            else:
                local_path = f"{filename}.md"
            
            sample_mapping[url] = local_path
        
        return {
            'base_url': self.base_url,
            'estimated_pages': len(test_crawler.discovered_urls),
            'sample_file_structure': sample_mapping,
            'domain': test_crawler.domain,
            'accessible': True
        }

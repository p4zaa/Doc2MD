#!/usr/bin/env python3
"""
Tests for DocumentConverter

Comprehensive test suite for the main converter functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import shutil
import os

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doc2md import DocumentConverter, WebCrawler, MarkdownGenerator, LinkTreeGenerator


class TestDocumentConverter(unittest.TestCase):
    """Test cases for DocumentConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "https://google.github.io/adk-docs/"
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test DocumentConverter initialization."""
        converter = DocumentConverter(
            base_url=self.test_url,
            output_dir=self.temp_dir,
            max_depth=3,
            delay=2.0
        )
        
        self.assertEqual(converter.base_url, self.test_url)
        self.assertEqual(converter.max_depth, 3)
        self.assertEqual(converter.delay, 2.0)
        self.assertIsInstance(converter.crawler, WebCrawler)
        self.assertIsInstance(converter.markdown_generator, MarkdownGenerator)
        self.assertIsInstance(converter.link_tree_generator, LinkTreeGenerator)
    
    def test_url_normalization(self):
        """Test URL normalization in initialization."""
        # Test with trailing slash
        converter = DocumentConverter(f"{self.test_url}/", output_dir=self.temp_dir)
        self.assertEqual(converter.base_url, self.test_url)
        
        # Test without trailing slash
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        self.assertEqual(converter.base_url, self.test_url)
    
    def test_output_directory_creation(self):
        """Test output directory creation."""
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        converter._create_output_directory()
        
        self.assertTrue(Path(self.temp_dir).exists())
        self.assertTrue(Path(self.temp_dir).is_dir())
    
    def test_path_sanitization(self):
        """Test path sanitization for folder names."""
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        
        # Test various path sanitization scenarios
        test_cases = [
            ("normal-path", "normal-path"),
            ("path with spaces", "path_with_spaces"),
            ("path@with#special$chars", "path_with_special_chars"),
            ("path/with/slashes", "path_with_slashes"),
            ("path_with_multiple___underscores", "path_with_multiple_underscores"),
            ("__path_with_leading_underscores__", "path_with_leading_underscores"),
        ]
        
        for input_path, expected in test_cases:
            result = converter._sanitize_path(input_path)
            self.assertEqual(result, expected)
    
    def test_file_path_generation(self):
        """Test file path generation from URLs."""
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        
        # Mock discovered URLs
        converter.crawler.discovered_urls = {
            "https://google.github.io/adk-docs/",
            "https://google.github.io/adk-docs/get-started",
            "https://google.github.io/adk-docs/get-started/installation",
            "https://google.github.io/adk-docs/deploy/agent-engine"
        }
        
        url_mapping = converter._generate_file_paths()
        
        # Check that all URLs have mappings
        self.assertEqual(len(url_mapping), 4)
        
        # Check specific mappings
        self.assertIn("https://google.github.io/adk-docs/", url_mapping)
        self.assertIn("https://google.github.io/adk-docs/get-started", url_mapping)
        self.assertIn("https://google.github.io/adk-docs/get-started/installation", url_mapping)
        self.assertIn("https://google.github.io/adk-docs/deploy/agent-engine", url_mapping)
    
    def test_url_validation(self):
        """Test URL validation functionality."""
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        
        # Mock successful response
        with patch.object(converter.crawler.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            result = converter.validate_url()
            self.assertTrue(result)
        
        # Mock failed response
        with patch.object(converter.crawler.session, 'get') as mock_get:
            mock_get.side_effect = Exception("Connection failed")
            
            result = converter.validate_url()
            self.assertFalse(result)
    
    def test_preview_conversion(self):
        """Test conversion preview functionality."""
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        
        # Mock successful preview
        with patch.object(WebCrawler, 'crawl') as mock_crawl:
            mock_crawl.return_value = {
                "https://google.github.io/adk-docs/": "<html>content</html>",
                "https://google.github.io/adk-docs/page1": "<html>page1</html>"
            }
            
            preview = converter.preview_conversion()
            
            self.assertNotIn('error', preview)
            self.assertEqual(preview['estimated_pages'], 2)
            self.assertEqual(preview['base_url'], self.test_url)
    
    def test_preview_conversion_failure(self):
        """Test conversion preview when crawling fails."""
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        
        # Mock failed preview
        with patch.object(WebCrawler, 'crawl') as mock_crawl:
            mock_crawl.return_value = {}
            
            preview = converter.preview_conversion()
            
            self.assertIn('error', preview)
            self.assertEqual(preview['error'], 'Could not access the website')
    
    def test_conversion_summary_generation(self):
        """Test conversion summary generation."""
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        
        # Mock conversion results
        converter.crawled_content = {"url1": "content1", "url2": "content2"}
        converter.url_mapping = {"url1": "file1.md", "url2": "file2.md"}
        converter.site_structure = {"total_pages": 2}
        
        summary = converter._generate_summary()
        
        self.assertEqual(summary['status'], 'success')
        self.assertEqual(summary['total_pages_crawled'], 2)
        self.assertEqual(summary['total_files_generated'], 2)
        self.assertEqual(summary['base_url'], self.test_url)
        self.assertIn('conversion_timestamp', summary)
    
    def test_conversion_stats(self):
        """Test conversion statistics retrieval."""
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        
        # Mock conversion results
        converter.crawled_content = {"url1": "content1"}
        converter.url_mapping = {"url1": "file1.md"}
        
        stats = converter.get_conversion_stats()
        
        self.assertEqual(stats['base_url'], self.test_url)
        self.assertEqual(stats['crawled_pages'], 1)
        self.assertEqual(stats['generated_files'], 1)
        self.assertEqual(stats['crawl_depth'], 0)
        self.assertEqual(stats['site_domain'], 'google.github.io')
    
    @patch('doc2md.converter.WebCrawler')
    @patch('doc2md.converter.MarkdownGenerator')
    @patch('doc2md.converter.LinkTreeGenerator')
    def test_full_conversion_process(self, mock_link_tree, mock_md_gen, mock_crawler):
        """Test the complete conversion process."""
        # Mock all components
        mock_crawler_instance = Mock()
        mock_crawler_instance.crawl.return_value = {"url1": "html1", "url2": "html2"}
        mock_crawler_instance.get_site_structure.return_value = {"total_pages": 2}
        mock_crawler_instance.discovered_urls = {"url1", "url2"}
        mock_crawler.return_value = mock_crawler_instance
        
        mock_md_gen_instance = Mock()
        mock_md_gen_instance.get_filename_from_url.return_value = "page"
        mock_md_gen_instance.generate_markdown.return_value = "# Markdown Content"
        mock_md_gen.return_value = mock_md_gen_instance
        
        mock_link_tree_instance = Mock()
        mock_link_tree.return_value = mock_link_tree_instance
        
        # Create converter and run conversion
        converter = DocumentConverter(self.test_url, output_dir=self.temp_dir)
        
        # Mock the file path generation
        converter._generate_file_paths = Mock(return_value={"url1": "page.md", "url2": "page.md"})
        
        # Run conversion
        result = converter.convert()
        
        # Verify all steps were called
        mock_crawler_instance.crawl.assert_called_once()
        mock_crawler_instance.get_site_structure.assert_called_once()
        mock_link_tree_instance.create_all_readmes.assert_called_once()
        
        # Verify result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['total_pages_crawled'], 2)
        self.assertEqual(result['total_files_generated'], 2)


class TestWebCrawler(unittest.TestCase):
    """Test cases for WebCrawler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "https://google.github.io/adk-docs/"
    
    def test_initialization(self):
        """Test WebCrawler initialization."""
        crawler = WebCrawler(self.test_url, max_depth=3, delay=2.0)
        
        self.assertEqual(crawler.base_url, self.test_url)
        self.assertEqual(crawler.max_depth, 3)
        self.assertEqual(crawler.delay, 2.0)
        self.assertEqual(crawler.domain, "google.github.io")
        self.assertEqual(crawler.base_path, "/adk-docs")
    
    def test_domain_validation(self):
        """Test same domain validation."""
        crawler = WebCrawler(self.test_url)
        
        # Same domain and path scope
        self.assertTrue(crawler.is_same_domain("https://google.github.io/adk-docs/page1"))
        self.assertTrue(crawler.is_same_domain("https://google.github.io/adk-docs/subdir/page"))
        
        # Different domain
        self.assertFalse(crawler.is_same_domain("https://other-site.com"))
        
        # Same domain but different path (should be excluded)
        self.assertFalse(crawler.is_same_domain("https://google.github.io/other-docs"))
        self.assertFalse(crawler.is_same_domain("https://google.github.io/"))
    
    def test_url_normalization(self):
        """Test URL normalization."""
        crawler = WebCrawler(self.test_url)
        
        # Test with query parameters and fragments
        normalized = crawler.normalize_url("https://google.github.io/adk-docs/page?param=value#section")
        self.assertEqual(normalized, "https://google.github.io/adk-docs/page")
        
        # Test without query parameters
        normalized = crawler.normalize_url("https://google.github.io/adk-docs/page")
        self.assertEqual(normalized, "https://google.github.io/adk-docs/page")


class TestMarkdownGenerator(unittest.TestCase):
    """Test cases for MarkdownGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "https://google.github.io/adk-docs/"
        self.generator = MarkdownGenerator(self.test_url)
    
    def test_initialization(self):
        """Test MarkdownGenerator initialization."""
        self.assertEqual(self.generator.base_url, self.test_url)
        self.assertIsNotNone(self.generator.h2t)
    
    def test_html_cleaning(self):
        """Test HTML cleaning functionality."""
        test_html = """
        <html>
        <head><title>Test</title></head>
        <body>
            <script>alert('test');</script>
            <style>body { color: red; }</style>
            <nav>Navigation</nav>
            <div class="advertisement">Ad</div>
            <h1>Main Content</h1>
            <p>This is content.</p>
        </body>
        </html>
        """
        
        cleaned = self.generator.clean_html(test_html)
        
        # Script, style, nav, and advertisement should be removed
        self.assertNotIn("alert('test')", cleaned)
        self.assertNotIn("color: red", cleaned)
        self.assertNotIn("Navigation", cleaned)
        self.assertNotIn("Ad", cleaned)
        
        # Content should remain
        self.assertIn("Main Content", cleaned)
        self.assertIn("This is content", cleaned)
    
    def test_filename_generation(self):
        """Test filename generation from URLs."""
        test_cases = [
            ("https://google.github.io/adk-docs/", "index"),
            ("https://google.github.io/adk-docs/", "index"),
            ("https://google.github.io/adk-docs/page", "page"),
            ("https://google.github.io/adk-docs/getting-started", "getting_started"),
            ("https://google.github.io/adk-docs/page.html", "page"),
            ("https://google.github.io/adk-docs/page.php", "page"),
            ("https://google.github.io/adk-docs/page with spaces", "page_with_spaces"),
        ]
        
        for url, expected in test_cases:
            result = self.generator.get_filename_from_url(url)
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

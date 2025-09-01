#!/usr/bin/env python3
"""
Tests for Exclude URLs Functionality

Tests that the crawler properly excludes specified URLs and URL patterns.
"""

import unittest
from unittest.mock import Mock, patch
import tempfile
import shutil
import os

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doc2md import WebCrawler, DocumentConverter


class TestExcludeUrls(unittest.TestCase):
    """Test cases for exclude URLs functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_exclude_specific_url(self):
        """Test that a specific URL is excluded."""
        base_url = "https://google.github.io/adk-docs/"
        exclude_urls = ["https://google.github.io/adk-docs/api-reference/java"]
        
        crawler = WebCrawler(base_url, exclude_urls=exclude_urls)
        
        # Test that the excluded URL is not considered valid
        self.assertTrue(crawler.is_excluded("https://google.github.io/adk-docs/api-reference/java"))
        self.assertTrue(crawler.is_excluded("https://google.github.io/adk-docs/api-reference/java/"))
        
        # Test that other URLs are still valid
        self.assertFalse(crawler.is_excluded("https://google.github.io/adk-docs/get-started"))
        self.assertFalse(crawler.is_excluded("https://google.github.io/adk-docs/tutorials/"))
    
    def test_exclude_url_pattern(self):
        """Test that URL patterns are properly excluded."""
        base_url = "https://google.github.io/adk-docs/"
        exclude_urls = ["https://google.github.io/adk-docs/api-reference/"]
        
        crawler = WebCrawler(base_url, exclude_urls=exclude_urls)
        
        # Test that all URLs under the excluded pattern are excluded
        excluded_urls = [
            "https://google.github.io/adk-docs/api-reference/",
            "https://google.github.io/adk-docs/api-reference/java",
            "https://google.github.io/adk-docs/api-reference/python",
            "https://google.github.io/adk-docs/api-reference/cli",
            "https://google.github.io/adk-docs/api-reference/rest-api",
        ]
        
        for url in excluded_urls:
            with self.subTest(url=url):
                self.assertTrue(
                    crawler.is_excluded(url),
                    f"URL should be excluded: {url}"
                )
        
        # Test that URLs outside the pattern are not excluded
        valid_urls = [
            "https://google.github.io/adk-docs/",
            "https://google.github.io/adk-docs/get-started",
            "https://google.github.io/adk-docs/tutorials/",
            "https://google.github.io/adk-docs/agents/",
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertFalse(
                    crawler.is_excluded(url),
                    f"URL should not be excluded: {url}"
                )
    
    def test_multiple_exclude_patterns(self):
        """Test that multiple exclude patterns work correctly."""
        base_url = "https://google.github.io/adk-docs/"
        exclude_urls = [
            "https://google.github.io/adk-docs/api-reference/",
            "https://google.github.io/adk-docs/admin/",
            "https://google.github.io/adk-docs/internal/"
        ]
        
        crawler = WebCrawler(base_url, exclude_urls=exclude_urls)
        
        # Test excluded patterns
        self.assertTrue(crawler.is_excluded("https://google.github.io/adk-docs/api-reference/java"))
        self.assertTrue(crawler.is_excluded("https://google.github.io/adk-docs/admin/users"))
        self.assertTrue(crawler.is_excluded("https://google.github.io/adk-docs/internal/debug"))
        
        # Test valid URLs
        self.assertFalse(crawler.is_excluded("https://google.github.io/adk-docs/get-started"))
        self.assertFalse(crawler.is_excluded("https://google.github.io/adk-docs/tutorials/"))
    
    def test_exclude_urls_in_converter(self):
        """Test that exclude URLs work in the DocumentConverter."""
        base_url = "https://google.github.io/adk-docs/"
        exclude_urls = ["https://google.github.io/adk-docs/api-reference/"]
        
        converter = DocumentConverter(
            base_url=base_url,
            output_dir=self.temp_dir,
            exclude_urls=exclude_urls
        )
        
        # Check that the crawler has the exclude patterns
        self.assertEqual(converter.crawler.exclude_urls, exclude_urls)
        self.assertEqual(len(converter.crawler.exclude_patterns), 1)
        
        # Test that the crawler excludes the right URLs
        self.assertTrue(converter.crawler.is_excluded("https://google.github.io/adk-docs/api-reference/java"))
        self.assertFalse(converter.crawler.is_excluded("https://google.github.io/adk-docs/get-started"))
    
    def test_exclude_urls_edge_cases(self):
        """Test edge cases for exclude URLs."""
        base_url = "https://google.github.io/adk-docs/"
        
        # Test with trailing slash
        exclude_urls_trailing = ["https://google.github.io/adk-docs/api-reference/"]
        crawler_trailing = WebCrawler(base_url, exclude_urls=exclude_urls_trailing)
        
        # Test without trailing slash
        exclude_urls_no_trailing = ["https://google.github.io/adk-docs/api-reference"]
        crawler_no_trailing = WebCrawler(base_url, exclude_urls=exclude_urls_no_trailing)
        
        # Both should exclude the same URLs
        test_urls = [
            "https://google.github.io/adk-docs/api-reference",
            "https://google.github.io/adk-docs/api-reference/",
            "https://google.github.io/adk-docs/api-reference/java",
            "https://google.github.io/adk-docs/api-reference/python",
        ]
        
        for url in test_urls:
            with self.subTest(url=url):
                self.assertTrue(crawler_trailing.is_excluded(url))
                self.assertTrue(crawler_no_trailing.is_excluded(url))
    
    def test_exclude_urls_normalization(self):
        """Test that exclude URLs are properly normalized."""
        base_url = "https://google.github.io/adk-docs/"
        exclude_urls = [
            "https://google.github.io/adk-docs/api-reference/java?param=value#section",
            "https://google.github.io/adk-docs/admin/users/",
        ]
        
        crawler = WebCrawler(base_url, exclude_urls=exclude_urls)
        
        # Check that exclude patterns are normalized (no query params or fragments)
        self.assertIn("https://google.github.io/adk-docs/api-reference/java", crawler.exclude_patterns)
        self.assertIn("https://google.github.io/adk-docs/admin/users", crawler.exclude_patterns)
        
        # Test that normalized URLs are excluded
        self.assertTrue(crawler.is_excluded("https://google.github.io/adk-docs/api-reference/java"))
        self.assertTrue(crawler.is_excluded("https://google.github.io/adk-docs/admin/users"))
    
    def test_no_exclude_urls(self):
        """Test that crawler works normally when no exclude URLs are specified."""
        base_url = "https://google.github.io/adk-docs/"
        crawler = WebCrawler(base_url)  # No exclude_urls
        
        # Should not exclude any URLs
        self.assertFalse(crawler.is_excluded("https://google.github.io/adk-docs/api-reference/java"))
        self.assertFalse(crawler.is_excluded("https://google.github.io/adk-docs/get-started"))
        
        # Check that exclude patterns list is empty
        self.assertEqual(len(crawler.exclude_patterns), 0)


if __name__ == '__main__':
    unittest.main()

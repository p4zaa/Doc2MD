#!/usr/bin/env python3
"""
Tests for Path-Restricted Crawling

Tests that the crawler only crawls URLs under the specified base path.
"""

import unittest
from unittest.mock import Mock, patch
import tempfile
import shutil
import os

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doc2md import WebCrawler


class TestPathRestriction(unittest.TestCase):
    """Test cases for path-restricted crawling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_adk_docs_path_restriction(self):
        """Test that ADK docs crawler only crawls under /adk-docs path."""
        base_url = "https://google.github.io/adk-docs/"
        crawler = WebCrawler(base_url)
        
        # URLs that should be included (under /adk-docs)
        valid_urls = [
            "https://google.github.io/adk-docs/",
            "https://google.github.io/adk-docs/get-started",
            "https://google.github.io/adk-docs/tutorials/agent-team",
            "https://google.github.io/adk-docs/agents/llm-agents",
            "https://google.github.io/adk-docs/tools/function-tools/overview",
        ]
        
        # URLs that should be excluded (outside /adk-docs)
        invalid_urls = [
            "https://google.github.io/",
            "https://google.github.io/other-docs",
            "https://google.github.io/blog",
            "https://google.github.io/support",
            "https://google.github.io/adk-docs-archive",  # Different path
        ]
        
        # Test valid URLs
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(
                    crawler.is_same_domain(url),
                    f"URL should be included: {url}"
                )
        
        # Test invalid URLs
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(
                    crawler.is_same_domain(url),
                    f"URL should be excluded: {url}"
                )
    
    def test_root_domain_crawling(self):
        """Test that root domain crawler can access all paths."""
        base_url = "https://google.github.io/"
        crawler = WebCrawler(base_url)
        
        # All these should be accessible from root domain
        test_urls = [
            "https://google.github.io/",
            "https://google.github.io/adk-docs",
            "https://google.github.io/other-docs",
            "https://google.github.io/blog",
            "https://google.github.io/support",
        ]
        
        for url in test_urls:
            with self.subTest(url=url):
                self.assertTrue(
                    crawler.is_same_domain(url),
                    f"URL should be accessible from root: {url}"
                )
    
    def test_nested_path_restriction(self):
        """Test deeply nested path restrictions."""
        base_url = "https://google.github.io/adk-docs/tutorials/"
        crawler = WebCrawler(base_url)
        
        # URLs that should be included (under /adk-docs/tutorials/)
        valid_urls = [
            "https://google.github.io/adk-docs/tutorials/",
            "https://google.github.io/adk-docs/tutorials/agent-team",
            "https://google.github.io/adk-docs/tutorials/advanced/patterns",
        ]
        
        # URLs that should be excluded
        invalid_urls = [
            "https://google.github.io/adk-docs/",
            "https://google.github.io/adk-docs/get-started",
            "https://google.github.io/adk-docs/agents/",
            "https://google.github.io/",
        ]
        
        # Test valid URLs
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(
                    crawler.is_same_domain(url),
                    f"URL should be included: {url}"
                )
        
        # Test invalid URLs
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(
                    crawler.is_same_domain(url),
                    f"URL should be excluded: {url}"
                )
    
    def test_crawler_initialization(self):
        """Test that crawler properly stores base path information."""
        test_cases = [
            ("https://google.github.io/", "/"),
            ("https://google.github.io/adk-docs", "/adk-docs"),
            ("https://google.github.io/adk-docs/", "/adk-docs"),
            ("https://google.github.io/adk-docs/tutorials", "/adk-docs/tutorials"),
            ("https://google.github.io/adk-docs/tutorials/", "/adk-docs/tutorials"),
        ]
        
        for base_url, expected_path in test_cases:
            with self.subTest(base_url=base_url):
                crawler = WebCrawler(base_url)
                self.assertEqual(crawler.base_path, expected_path)
                self.assertEqual(crawler.domain, "google.github.io")


if __name__ == '__main__':
    unittest.main()

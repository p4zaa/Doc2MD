"""
Web Document to Markdown Converter

A comprehensive library for converting web documents to markdown format
with configurable crawling depth and organized folder structure.
"""

__version__ = "1.0.0"
__author__ = "Doc2MD Team"

from .converter import DocumentConverter
from .crawler import WebCrawler
from .markdown_generator import MarkdownGenerator
from .link_tree import LinkTreeGenerator

__all__ = [
    "DocumentConverter",
    "WebCrawler", 
    "MarkdownGenerator",
    "LinkTreeGenerator"
]

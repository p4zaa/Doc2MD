#!/usr/bin/env python3
"""
Exclude URLs Demo for Doc2MD

This script demonstrates how to exclude specific URLs or URL patterns
from crawling without requiring external dependencies.
"""

from urllib.parse import urlparse

def is_excluded(url, exclude_patterns):
    """
    Check if URL should be excluded from crawling.
    This is the logic used in the WebCrawler class.
    """
    def normalize_url(url):
        """Normalize URL by removing fragments and query parameters."""
        parsed = urlparse(url)
        clean_parsed = parsed._replace(fragment='', query='')
        return clean_parsed.geturl()
    
    normalized_url = normalize_url(url)
    
    # Check if the URL matches any exclude pattern
    for exclude_pattern in exclude_patterns:
        normalized_pattern = normalize_url(exclude_pattern)
        
        # Check exact match
        if normalized_url == normalized_pattern:
            return True
        
        # Check if URL starts with exclude pattern (for path-based exclusion)
        if normalized_pattern.endswith('/') and normalized_url.startswith(normalized_pattern):
            return True
        
        # Check if exclude pattern ends with / and URL starts with it
        if not normalized_pattern.endswith('/') and normalized_url.startswith(normalized_pattern + '/'):
            return True
    
    return False

def demonstrate_exclude_urls():
    """Demonstrate exclude URLs functionality."""
    
    print("🚀 Doc2MD Exclude URLs Demo")
    print("=" * 60)
    
    # Test case 1: Exclude API reference pages
    print("\n📚 Test Case 1: Exclude API Reference Pages")
    print("Base URL: https://google.github.io/adk-docs/")
    print("Exclude: https://google.github.io/adk-docs/api-reference/")
    print("-" * 50)
    
    base_url = "https://google.github.io/adk-docs/"
    exclude_patterns = ["https://google.github.io/adk-docs/api-reference/"]
    
    test_urls = [
        # URLs that SHOULD be excluded (under /api-reference/)
        ("https://google.github.io/adk-docs/api-reference/", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/api-reference/java", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/api-reference/python", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/api-reference/cli", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/api-reference/rest-api", "🚫 EXCLUDED"),
        
        # URLs that SHOULD be included (not under /api-reference/)
        ("https://google.github.io/adk-docs/", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/get-started", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/tutorials/agent-team", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/agents/llm-agents", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/tools/function-tools/overview", "✅ INCLUDED"),
    ]
    
    for url, expected in test_urls:
        result = is_excluded(url, exclude_patterns)
        status = "🚫 EXCLUDED" if result else "✅ INCLUDED"
        print(f"{status:<12} {url}")
    
    # Test case 2: Multiple exclude patterns
    print("\n🚫 Test Case 2: Multiple Exclude Patterns")
    print("Base URL: https://google.github.io/adk-docs/")
    print("Exclude: API reference, Admin, Internal pages")
    print("-" * 50)
    
    exclude_patterns_multiple = [
        "https://google.github.io/adk-docs/api-reference/",
        "https://google.github.io/adk-docs/admin/",
        "https://google.github.io/adk-docs/internal/"
    ]
    
    test_urls_multiple = [
        # URLs that SHOULD be excluded
        ("https://google.github.io/adk-docs/api-reference/java", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/admin/users", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/internal/debug", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/admin/settings", "🚫 EXCLUDED"),
        
        # URLs that SHOULD be included
        ("https://google.github.io/adk-docs/get-started", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/tutorials/", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/agents/", "✅ INCLUDED"),
    ]
    
    for url, expected in test_urls_multiple:
        result = is_excluded(url, exclude_patterns_multiple)
        status = "🚫 EXCLUDED" if result else "✅ INCLUDED"
        print(f"{status:<12} {url}")
    
    # Test case 3: Exact URL exclusion vs Path pattern exclusion
    print("\n🎯 Test Case 3: Exact vs Path Pattern Exclusion")
    print("Exclude: https://google.github.io/adk-docs/specific-page")
    print("-" * 50)
    
    exclude_patterns_exact = ["https://google.github.io/adk-docs/specific-page"]
    
    test_urls_exact = [
        # Exact match should be excluded
        ("https://google.github.io/adk-docs/specific-page", "🚫 EXCLUDED"),
        
        # Similar URLs should NOT be excluded
        ("https://google.github.io/adk-docs/specific-page-other", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/specific-page/", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/specific-page/subpage", "✅ INCLUDED"),
    ]
    
    for url, expected in test_urls_exact:
        result = is_excluded(url, exclude_patterns_exact)
        status = "🚫 EXCLUDED" if result else "✅ INCLUDED"
        print(f"{status:<12} {url}")
    
    # Test case 4: URL normalization
    print("\n🔧 Test Case 4: URL Normalization")
    print("Exclude: https://google.github.io/adk-docs/api-reference/")
    print("Note: Query parameters and fragments are automatically removed")
    print("-" * 50)
    
    exclude_patterns_norm = ["https://google.github.io/adk-docs/api-reference/"]
    
    test_urls_norm = [
        # These should all be excluded despite different formats
        ("https://google.github.io/adk-docs/api-reference/java", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/api-reference/java?param=value", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/api-reference/java#section", "🚫 EXCLUDED"),
        ("https://google.github.io/adk-docs/api-reference/java?param=value#section", "🚫 EXCLUDED"),
    ]
    
    for url, expected in test_urls_norm:
        result = is_excluded(url, exclude_patterns_norm)
        status = "🚫 EXCLUDED" if result else "✅ INCLUDED"
        print(f"{status:<12} {url}")
    
    print("\n" + "=" * 60)
    print("💡 Key Benefits of URL Exclusion:")
    print("  • Skip API reference pages that are not user-facing")
    print("  • Exclude admin/internal pages from documentation")
    print("  • Focus crawling on relevant content only")
    print("  • Reduce conversion time and output size")
    print("  • More targeted and useful documentation")

def show_cli_usage():
    """Show how to use exclude URLs in the CLI."""
    print("\n" + "=" * 60)
    print("🖥️  CLI Usage Examples:")
    print("=" * 60)
    
    examples = [
        {
            "description": "Exclude API reference pages",
            "command": 'doc2md convert https://google.github.io/adk-docs/ --exclude "https://google.github.io/adk-docs/api-reference/"'
        },
        {
            "description": "Exclude multiple patterns",
            "command": 'doc2md convert https://google.github.io/adk-docs/ \\\n  --exclude "https://google.github.io/adk-docs/api-reference/" \\\n  --exclude "https://google.github.io/adk-docs/admin/" \\\n  --exclude "https://google.github.io/adk-docs/internal/"'
        },
        {
            "description": "Exclude with depth limit",
            "command": 'doc2md convert https://google.github.io/adk-docs/ --depth 2 --exclude "https://google.github.io/adk-docs/api-reference/"'
        }
    ]
    
    for example in examples:
        print(f"\n📝 {example['description']}:")
        print(f"  {example['command']}")

def show_programmatic_usage():
    """Show how to use exclude URLs programmatically."""
    print("\n" + "=" * 60)
    print("🐍 Programmatic Usage Examples:")
    print("=" * 60)
    
    examples = [
        {
            "description": "Basic exclusion",
            "code": """from doc2md import DocumentConverter

exclude_urls = ["https://google.github.io/adk-docs/api-reference/"]
converter = DocumentConverter(
    base_url="https://google.github.io/adk-docs/",
    exclude_urls=exclude_urls
)
result = converter.convert()"""
        },
        {
            "description": "Multiple exclusions",
            "code": """exclude_urls = [
    "https://google.github.io/adk-docs/api-reference/",
    "https://google.github.io/adk-docs/admin/",
    "https://google.github.io/adk-docs/internal/"
]

converter = DocumentConverter(
    base_url="https://google.github.io/adk-docs/",
    exclude_urls=exclude_urls
)"""
        },
        {
            "description": "Custom crawler with exclusions",
            "code": """from doc2md import WebCrawler

crawler = WebCrawler(
    base_url="https://google.github.io/adk-docs/",
    exclude_urls=["https://google.github.io/adk-docs/api-reference/"]
)
content = crawler.crawl()"""
        }
    ]
    
    for example in examples:
        print(f"\n📚 {example['description']}:")
        print("  Code:")
        print("    " + "\n    ".join(example['code'].split('\n')))

def main():
    """Run all demo functions."""
    try:
        demonstrate_exclude_urls()
        show_cli_usage()
        show_programmatic_usage()
        
        print("\n\n🎉 Exclude URLs demo completed successfully!")
        print("\n💡 To try the actual conversion with exclusions:")
        print("   1. Use the CLI: doc2md convert <url> --exclude <pattern>")
        print("   2. Or use the programmatic API with exclude_urls parameter")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

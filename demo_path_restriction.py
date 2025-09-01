#!/usr/bin/env python3
"""
Path Restriction Demo

This script demonstrates how Doc2MD restricts crawling to specific paths
without requiring external dependencies.
"""

from urllib.parse import urlparse

def is_same_domain_and_path(url, base_url):
    """
    Check if URL belongs to the same domain and path scope.
    This is the logic used in the WebCrawler class.
    """
    parsed = urlparse(url)
    base_parsed = urlparse(base_url)
    
    # Check domain first
    if parsed.netloc != base_parsed.netloc:
        return False
    
    # Check if URL path starts with the base URL path
    base_path = base_parsed.path
    
    # If base URL has a path, ensure the URL is under that path
    if base_path and base_path != '/':
        if not parsed.path.startswith(base_path):
            return False
    
    return True

def demonstrate_path_restriction():
    """Demonstrate path restriction behavior."""
    
    print("🚀 Doc2MD Path Restriction Demo")
    print("=" * 50)
    
    # Test case 1: ADK Documentation
    print("\n📚 Test Case 1: Google ADK Documentation")
    print("Base URL: https://google.github.io/adk-docs/")
    print("-" * 40)
    
    base_url = "https://google.github.io/adk-docs/"
    
    test_urls = [
        # URLs that SHOULD be included (under /adk-docs)
        ("https://google.github.io/adk-docs/", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/get-started", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/tutorials/agent-team", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/agents/llm-agents", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/tools/function-tools/overview", "✅ INCLUDED"),
        
        # URLs that SHOULD be excluded (outside /adk-docs)
        ("https://google.github.io/", "❌ EXCLUDED"),
        ("https://google.github.io/other-docs", "❌ EXCLUDED"),
        ("https://google.github.io/blog", "❌ EXCLUDED"),
        ("https://google.github.io/support", "❌ EXCLUDED"),
        ("https://google.github.io/adk-docs-archive", "❌ EXCLUDED"),
    ]
    
    for url, expected in test_urls:
        result = is_same_domain_and_path(url, base_url)
        status = "✅ INCLUDED" if result else "❌ EXCLUDED"
        print(f"{status:<12} {url}")
    
    # Test case 2: Root domain
    print("\n🌐 Test Case 2: Root Domain")
    print("Base URL: https://google.github.io/")
    print("-" * 40)
    
    base_url_root = "https://google.github.io/"
    
    test_urls_root = [
        ("https://google.github.io/", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs", "✅ INCLUDED"),
        ("https://google.github.io/other-docs", "✅ INCLUDED"),
        ("https://google.github.io/blog", "✅ INCLUDED"),
        ("https://google.github.io/support", "✅ INCLUDED"),
    ]
    
    for url, expected in test_urls_root:
        result = is_same_domain_and_path(url, base_url_root)
        status = "✅ INCLUDED" if result else "❌ EXCLUDED"
        print(f"{status:<12} {url}")
    
    # Test case 3: Nested path
    print("\n📁 Test Case 3: Nested Path")
    print("Base URL: https://google.github.io/adk-docs/tutorials/")
    print("-" * 40)
    
    base_url_nested = "https://google.github.io/adk-docs/tutorials/"
    
    test_urls_nested = [
        # URLs that SHOULD be included (under /adk-docs/tutorials/)
        ("https://google.github.io/adk-docs/tutorials/", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/tutorials/agent-team", "✅ INCLUDED"),
        ("https://google.github.io/adk-docs/tutorials/advanced/patterns", "✅ INCLUDED"),
        
        # URLs that SHOULD be excluded
        ("https://google.github.io/adk-docs/", "❌ EXCLUDED"),
        ("https://google.github.io/adk-docs/get-started", "❌ EXCLUDED"),
        ("https://google.github.io/adk-docs/agents/", "❌ EXCLUDED"),
        ("https://google.github.io/", "❌ EXCLUDED"),
    ]
    
    for url, expected in test_urls_nested:
        result = is_same_domain_and_path(url, base_url_nested)
        status = "✅ INCLUDED" if result else "❌ EXCLUDED"
        print(f"{status:<12} {url}")
    
    print("\n" + "=" * 50)
    print("💡 Key Benefits of Path Restriction:")
    print("  • Prevents crawling unrelated content")
    print("  • Focuses conversion on specific documentation")
    print("  • Respects website structure and boundaries")
    print("  • More efficient and targeted crawling")

if __name__ == "__main__":
    demonstrate_path_restriction()

#!/usr/bin/env python3
"""
Advanced Usage Example for Doc2MD

This example demonstrates advanced features like custom depth control,
batch processing, and custom configuration.
"""

from doc2md import DocumentConverter, WebCrawler, MarkdownGenerator
import logging
from pathlib import Path
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

def example_limited_depth():
    """Example with limited crawl depth."""
    print("\n🔍 Example 1: Limited Depth Crawling")
    print("=" * 40)
    
    target_url = "https://google.github.io/adk-docs/"
    
    # Crawl only 2 levels deep, excluding API reference pages
    exclude_urls = ["https://google.github.io/adk-docs/api-reference/"]
    
    converter = DocumentConverter(
        base_url=target_url,
        output_dir="limited_depth_output",
        max_depth=2,
        delay=0.5,  # Faster crawling
        exclude_urls=exclude_urls
    )
    
    try:
        result = converter.convert()
        print(f"✅ Limited depth conversion completed!")
        print(f"📊 Pages crawled: {result['total_pages_crawled']}")
        print(f"🔍 Crawl depth: {result['crawl_depth']}")
    except Exception as e:
        print(f"❌ Failed: {e}")

def example_custom_crawler():
    """Example using custom crawler configuration."""
    print("\n🕷️  Example 2: Custom Crawler Configuration")
    print("=" * 40)
    
    target_url = "https://google.github.io/adk-docs/"
    
    # Create custom crawler with specific settings and exclusions
    exclude_urls = ["https://google.github.io/adk-docs/api-reference/"]
    
    crawler = WebCrawler(
        base_url=target_url,
        max_depth=3,
        delay=2.0,  # Slower, more respectful crawling
        exclude_urls=exclude_urls
    )
    
    try:
        # Crawl the site
        content = crawler.crawl()
        print(f"✅ Custom crawling completed!")
        print(f"📊 Pages discovered: {len(content)}")
        
        # Get site structure
        structure = crawler.get_site_structure()
        print(f"🌐 Domain: {structure['domain']}")
        print(f"🔍 Max depth: {structure['max_depth']}")
        
        # Show URLs by depth
        depth_groups = {}
        for url, depth in structure['url_depths'].items():
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append(url)
        
        for depth in sorted(depth_groups.keys()):
            print(f"  Level {depth}: {len(depth_groups[depth])} pages")
            
    except Exception as e:
        print(f"❌ Failed: {e}")

def example_batch_processing():
    """Example of batch processing multiple sites."""
    print("\n📚 Example 3: Batch Processing Multiple Sites")
    print("=" * 40)
    
    sites = [
        "https://docs.site1.com",
        "https://docs.site2.com",
        "https://docs.site3.com"
    ]
    
    for i, site_url in enumerate(sites, 1):
        print(f"\n🔄 Processing site {i}/{len(sites)}: {site_url}")
        
        try:
            converter = DocumentConverter(
                base_url=site_url,
                output_dir=f"batch_output/site_{i}",
                max_depth=1,  # Quick crawl for demo
                delay=1.0
            )
            
            # Quick validation
            if not converter.validate_url():
                print(f"  ❌ Site not accessible, skipping...")
                continue
            
            # Preview first
            preview = converter.preview_conversion()
            if 'error' not in preview:
                print(f"  📊 Estimated pages: {preview['estimated_pages']}")
                
                # Convert
                result = converter.convert()
                print(f"  ✅ Converted {result['total_files_generated']} pages")
            else:
                print(f"  ❌ Preview failed: {preview['error']}")
                
        except Exception as e:
            print(f"  ❌ Failed: {e}")
        
        # Wait between sites
        if i < len(sites):
            print("  ⏱️  Waiting 5 seconds before next site...")
            time.sleep(5)

def example_custom_markdown():
    """Example with custom markdown generation."""
    print("\n✍️  Example 4: Custom Markdown Generation")
    print("=" * 40)
    
    target_url = "https://google.github.io/adk-docs/"
    
    try:
        # Create custom markdown generator
        md_generator = MarkdownGenerator(base_url=target_url)
        
        # Test with sample HTML content
        sample_html = """
        <html>
        <head><title>Sample Page</title></head>
        <body>
            <h1>Welcome to Sample Page</h1>
            <p>This is a <strong>sample</strong> paragraph with <a href="/link">a link</a>.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </body>
        </html>
        """
        
        # Convert to markdown
        markdown = md_generator.generate_markdown(sample_html, target_url)
        
        print("✅ Custom markdown generation completed!")
        print("\n📄 Generated Markdown:")
        print("-" * 30)
        print(markdown)
        print("-" * 30)
        
    except Exception as e:
        print(f"❌ Failed: {e}")

def example_error_handling():
    """Example showing error handling and recovery."""
    print("\n🛡️  Example 5: Error Handling and Recovery")
    print("=" * 40)
    
    # Test with invalid URL
    invalid_url = "https://invalid-site-that-does-not-exist.com"
    
    try:
        converter = DocumentConverter(
            base_url=invalid_url,
            output_dir="error_test_output"
        )
        
        # This should fail
        result = converter.convert()
        
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}")
        print(f"📝 Error message: {e}")
        
        # Show how to handle errors gracefully
        print("\n🔄 Attempting recovery with different approach...")
        
        try:
            # Try with a different configuration
            converter = DocumentConverter(
                base_url=invalid_url,
                output_dir="error_test_output",
                max_depth=1,
                delay=5.0  # Longer delay
            )
            
            # Validate first
            if converter.validate_url():
                print("  ✅ Recovery successful!")
            else:
                print("  ❌ Recovery failed - site truly inaccessible")
                
        except Exception as recovery_error:
            print(f"  ❌ Recovery also failed: {recovery_error}")

def main():
    """Run all examples."""
    print("🚀 Doc2MD Advanced Usage Examples")
    print("=" * 50)
    
    # Run examples
    example_limited_depth()
    example_custom_crawler()
    example_batch_processing()
    example_custom_markdown()
    example_error_handling()
    
    print("\n✅ All examples completed!")
    print("\n💡 Tips:")
    print("  - Use max_depth=0 for unlimited crawling")
    print("  - Adjust delay based on site responsiveness")
    print("  - Always validate URLs before conversion")
    print("  - Use preview mode to estimate conversion size")

if __name__ == "__main__":
    main()

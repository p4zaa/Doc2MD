#!/usr/bin/env python3
"""
Basic Usage Example for Doc2MD

This example demonstrates how to use the DocumentConverter class
programmatically to convert a web document to markdown.
"""
# Add parent directory to path for imports
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doc2md import DocumentConverter
import logging

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)

def main():
    """Example of basic usage."""
    
    # Example URL - replace with your target document site
    target_url = "https://google.github.io/adk-docs/" #"https://example-docs.com"
    
    print(f"🚀 Starting conversion of {target_url}")
    print("=" * 50)
    print("📁 Path Restriction: This will ONLY crawl URLs under /adk-docs/")
    print("   It will NOT crawl other content on google.github.io")
    print("=" * 50)
    
    try:
        # Create converter instance
        # - max_depth=0 means crawl all pages (unlimited)
        # - delay=1.0 means wait 1 second between requests
        # - The crawler automatically restricts to URLs under the base path
        # - exclude_urls prevents crawling specific URLs or URL patterns
        exclude_urls = [
            "https://google.github.io/adk-docs/api-reference/java",
            "https://google.github.io/adk-docs/api-reference/python"
        ]
        
        converter = DocumentConverter(
            base_url=target_url,
            output_dir="example_output",
            max_depth=0,
            delay=1.0,
            exclude_urls=exclude_urls,
            generate_readme=False,  # Disable README.md generation
            raw_output=False,  # Enable post-processing (cleaned output)
            ai_optimization_level="enhanced",  # Maximum AI optimization
            force_triple_backticks=True,  # Force triple backticks for AI compatibility
            reduce_empty_lines=True  # Reduce empty lines for cleaner output
        )
        
        # Optional: Validate URL before conversion
        print("🔍 Validating URL...")
        if not converter.validate_url():
            print("❌ URL validation failed!")
            return
        
        print("✅ URL validation successful!")
        
        # Optional: Preview conversion
        print("\n📋 Generating preview...")
        preview = converter.preview_conversion()
        
        if 'error' in preview:
            print(f"❌ Preview failed: {preview['error']}")
            return
        
        print(f"📊 Estimated pages: {preview['estimated_pages']}")
        print(f"🌐 Domain: {preview['domain']}")
        
        # Perform the conversion
        print("\n🔄 Starting conversion...")
        result = converter.convert()
        
        # Display results
        print("\n✅ Conversion completed successfully!")
        print(f"📊 Total pages crawled: {result['total_pages_crawled']}")
        print(f"📄 Total files generated: {result['total_files_generated']}")
        print(f"📁 Output directory: {result['output_directory']}")
        
        # Get conversion statistics
        stats = converter.get_conversion_stats()
        print(f"🌐 Site domain: {stats['site_domain']}")
        print(f"🔍 Crawl depth: {stats['crawl_depth']}")
        
        if converter.generate_readme:
            print(f"\n📖 Start browsing your converted documents in: {result['output_directory']}/README.md")
        else:
            print(f"\n📁 Your converted documents are in: {result['output_directory']}/")
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

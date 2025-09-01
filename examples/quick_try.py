# Add parent directory to path for imports
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from doc2md import DocumentConverter

def main():
    """Example of basic usage."""
    
    # Example URL - replace with your target document site
    target_url = "https://google.github.io/adk-docs/"
    output_dir = "/Users/pa/Local Documents/Temporary Space/Doc2MD Output"
    
    print(f"🚀 Starting conversion of {target_url}")
    
    try:
        exclude_urls = [
            "https://google.github.io/adk-docs/api-reference/java",
            #"https://google.github.io/adk-docs/api-reference/python"
        ]
        
        converter = DocumentConverter(
            base_url=target_url,
            output_dir=output_dir,
            max_depth=2,
            delay=1.0,
            exclude_urls=exclude_urls,
            force_triple_backticks=False,
            debug=False
        )
        
        # Optional: Validate URL before conversion
        print("🔍 Validating URL...")
        if not converter.validate_url():
            print("❌ URL validation failed!")
            return
        
        print("✅ URL validation successful!")

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
        
        print(f"\n📖 Start browsing your converted documents in: {result['output_directory']}/README.md")
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
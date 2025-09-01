#!/usr/bin/env python3
"""
Debug script to run DocumentConverter with debug logging

This will help us see exactly where the first line content is getting lost.
"""

def main():
    """Run the DocumentConverter with debug logging."""
    
    print("🔍 Debug: DocumentConverter with Debug Logging")
    print("=" * 60)
    
    try:
        # Import the converter
        from doc2md import DocumentConverter
        
        print("✅ Successfully imported DocumentConverter")
        
        # Create converter with debug enabled
        print("\n🔧 Creating DocumentConverter with debug=True...")
        converter = DocumentConverter(
            base_url="https://google.github.io/adk-docs/",
            output_dir="debug_output",
            max_depth=1,  # Limit depth for faster debugging
            debug=True    # Enable debug logging
        )
        
        print("✅ DocumentConverter created with debug logging enabled")
        print("🔍 You should see detailed debug logs showing:")
        print("   • Original HTML content analysis")
        print("   • HTML cleaning process")
        print("   • HTML pre-processing steps")
        print("   • html2text conversion")
        print("   • Content preservation checks")
        
        print("\n🚀 Starting conversion...")
        print("=" * 60)
        
        # Run the conversion
        result = converter.convert()
        
        print("\n" + "=" * 60)
        print("✅ Conversion completed!")
        print("=" * 60)
        
        print(f"📊 Results:")
        print(f"   • Total pages crawled: {result['total_pages_crawled']}")
        print(f"   • Total files generated: {result['total_files_generated']}")
        print(f"   • Output directory: {result['output_directory']}")
        
        print(f"\n🔍 Check the debug logs above to see:")
        print(f"   • Where 'GOOGLE_GENAI_USE_VERTEXAI=0' content is lost")
        print(f"   • Whether html2text is receiving the content")
        print(f"   • If our pre-processing is working correctly")
        
        print(f"\n📁 Check the generated files in: {result['output_directory']}")
        print(f"   Look for files containing 'GOOGLE_API_KEY' to see the results")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the Doc2MD project root directory")
        print("And that all dependencies are installed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

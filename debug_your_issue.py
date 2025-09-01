#!/usr/bin/env python3
"""
Simple script to debug your specific issue with 'adk --version' not appearing

This script will help you identify exactly where the content is being lost.
"""

def show_debug_instructions():
    """Show how to debug your issue."""
    
    print("🔍 Debugging Your 'adk --version' Issue")
    print("=" * 60)
    
    print("\n📝 **The Problem:**")
    print("  Your markdown output shows:")
    print("  ```")
    print("  ```")
    print("  (missing 'adk --version' content)")
    
    print("\n🔍 **Debug Steps:**")
    print("-" * 40)
    
    steps = [
        "1. **Enable Debug Logging**:",
        "   • Add debug=True to your DocumentConverter",
        "   • This will show exactly where content is lost",
        "",
        "2. **Check the Logs**:",
        "   • Look for messages about 'adk --version'",
        "   • Check if it's found in original HTML",
        "   • Check if it's lost during cleaning",
        "   • Check if it's lost during markdown conversion",
        "",
        "3. **Common Causes**:",
        "   • Website uses JavaScript to load content",
        "   • HTML structure is different than expected",
        "   • Content is in a different format",
        "   • HTML cleaning is too aggressive"
    ]
    
    for step in steps:
        print(f"  {step}")

def show_usage_example():
    """Show how to use debug mode."""
    
    print("\n" + "=" * 60)
    print("🚀 Debug Mode Usage")
    print("=" * 60)
    
    print("\n📝 **Python API with Debug:**")
    print("-" * 40)
    
    code_example = '''from doc2md import DocumentConverter

# Enable debug mode to see exactly what's happening
converter = DocumentConverter(
    base_url="https://your-website.com",
    output_dir="output",
    max_depth=2,
    debug=True  # This enables detailed logging
)

# Convert the website
result = converter.convert()

# Check the logs for debug information
print("Check the console output and conversion.log for debug info")'''
    
    print(code_example)
    
    print("\n📝 **Command Line with Debug:**")
    print("-" * 40)
    
    cli_example = '''# Add --debug flag to enable debug logging
doc2md https://your-website.com --debug

# This will show detailed information about:
# - HTML content found
# - Code blocks detected
# - Content processing steps
# - Where content might be lost'''
    
    print(cli_example)

def show_what_to_look_for():
    """Show what debug messages to look for."""
    
    print("\n" + "=" * 60)
    print("🔍 What to Look For in Debug Logs")
    print("=" * 60)
    
    print("\n📋 **Key Debug Messages:**")
    print("-" * 40)
    
    messages = [
        "✅ **Content Found**:",
        "  • 'Found 'adk --version' in original HTML'",
        "  • 'Found 'adk --version' in cleaned HTML'",
        "  • 'Found 'adk --version' in html2text output'",
        "",
        "❌ **Content Lost**:",
        "  • 'adk --version' NOT found in original HTML'",
        "  • 'adk --version' NOT found in cleaned HTML'",
        "  • 'adk --version' NOT found in html2text output'",
        "",
        "🔧 **Code Block Processing**:",
        "  • 'Found <pre> tag with content: ...'",
        "  • 'Found <code> tag: ...'",
        "  • 'Preserving code block with content: ...'"
    ]
    
    for message in messages:
        print(f"  {message}")

def show_troubleshooting_tips():
    """Show troubleshooting tips."""
    
    print("\n" + "=" * 60)
    print("🛠️ Troubleshooting Tips")
    print("=" * 60)
    
    print("\n📝 **If Content is NOT in Original HTML:**")
    print("-" * 50)
    
    tips1 = [
        "• Website uses JavaScript to load content",
        "• Content is dynamically generated",
        "• You need a JavaScript-enabled crawler",
        "• Try using a different crawling approach"
    ]
    
    for tip in tips1:
        print(f"  {tip}")
    
    print("\n📝 **If Content is Lost During Cleaning:**")
    print("-" * 50)
    
    tips2 = [
        "• HTML cleaning is too aggressive",
        "• Code blocks are being removed",
        "• Modify the clean_html method",
        "• Check what HTML elements contain your content"
    ]
    
    for tip in tips2:
        print(f"  {tip}")
    
    print("\n📝 **If Content is Lost During Markdown Conversion:**")
    print("-" * 50)
    
    tips3 = [
        "• html2text doesn't recognize the HTML structure",
        "• Code blocks are not properly formatted",
        "• The fix methods are removing content",
        "• Check the HTML structure of your code blocks"
    ]
    
    for tip in tips3:
        print(f"  {tip}")

def main():
    """Run the debug guide."""
    try:
        show_debug_instructions()
        show_usage_example()
        show_what_to_look_for()
        show_troubleshooting_tips()
        
        print("\n\n🎉 Debug Guide Completed!")
        print("\n💡 **Next Steps:**")
        print("  1. Enable debug mode in your DocumentConverter")
        print("  2. Run the conversion and check the logs")
        print("  3. Look for the specific debug messages")
        print("  4. Identify exactly where 'adk --version' is lost")
        print("  5. Fix the issue based on what you find")
        
        print("\n🚀 **Quick Test:**")
        print("  Try this simple test first:")
        print("  converter = DocumentConverter(url, debug=True)")
        print("  result = converter.convert()")
        print("  # Check console output for debug info")
        
    except Exception as e:
        print(f"\n❌ Debug guide failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

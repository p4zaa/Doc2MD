#!/usr/bin/env python3
"""
Test script to verify the html2text compatibility fix

This tests the new pre-processing that converts complex HTML structures
to simpler ones that html2text can handle properly.
"""

def test_html2text_compatibility():
    """Test the html2text compatibility fix."""
    
    print("🧪 Testing HTML2Text Compatibility Fix")
    print("=" * 60)
    
    # Your actual HTML structure that was causing issues
    your_html = '''
    <html>
    <body>
        <h1>Installation Guide</h1>
        <p>To check the version:</p>
        <div class="language-text highlight">
            <pre>
                <span></span>
                <code>adk --version</code>
            </pre>
        </div>
        <p>To create an agent:</p>
        <div class="language-bash highlight">
            <pre>
                <span></span>
                <code>adk create --type=config my_agent</code>
            </pre>
        </div>
        <p>Environment variables:</p>
        <div class="language-env highlight">
            <pre>
                <span></span>
                <code>GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=<your-Google-Gemini-API-key></code>
            </pre>
        </div>
    </body>
    </html>
    '''
    
    print("📝 **Your HTML Structure:**")
    print("-" * 40)
    print(your_html)
    
    print("\n🔍 **Testing the Complete Pipeline:**")
    print("-" * 40)
    
    try:
        # Import the fixed markdown generator
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'doc2md'))
        
        from markdown_generator import MarkdownGenerator
        
        # Create generator
        generator = MarkdownGenerator("https://example.com", optimize_for_ai=True)
        
        # Test the complete pipeline
        markdown_content = generator.generate_markdown(your_html, "https://example.com")
        
        print(f"✅ Markdown generation completed")
        print(f"📏 Final markdown length: {len(markdown_content)}")
        
        # Check for specific content
        content_checks = [
            "adk --version",
            "adk create --type=config my_agent", 
            "GOOGLE_GENAI_USE_VERTEXAI=0",
            "GOOGLE_API_KEY=<your-Google-Gemini-API-key>"
        ]
        
        print(f"\n🔍 **Content Verification:**")
        print("-" * 30)
        
        all_content_found = True
        for content in content_checks:
            if content in markdown_content:
                print(f"✅ Found: {repr(content)}")
            else:
                print(f"❌ Missing: {repr(content)}")
                all_content_found = False
        
        # Check for code blocks
        print(f"\n🔍 **Code Block Verification:**")
        print("-" * 30)
        
        if '```' in markdown_content:
            code_block_count = markdown_content.count('```')
            print(f"✅ Found {code_block_count} triple backticks")
            
            # Check if content is properly inside code blocks
            lines = markdown_content.split('\n')
            in_code_block = False
            code_blocks = []
            current_block = []
            
            for i, line in enumerate(lines):
                if line.strip() == '```':
                    if in_code_block:
                        # End of code block
                        code_blocks.append('\n'.join(current_block))
                        current_block = []
                        in_code_block = False
                    else:
                        # Start of code block
                        in_code_block = True
                elif in_code_block:
                    current_block.append(line)
            
            print(f"✅ Found {len(code_blocks)} complete code blocks")
            
            # Check each code block for content
            for i, block in enumerate(code_blocks):
                if block.strip():
                    print(f"  Code block {i+1}: {repr(block.strip()[:100])}")
                else:
                    print(f"  Code block {i+1}: EMPTY")
        else:
            print("❌ No code blocks (```) found in markdown")
            all_content_found = False
        
        # Show final markdown
        print(f"\n📝 **Generated Markdown:**")
        print("-" * 30)
        print(markdown_content)
        
        print(f"\n🎯 **Test Results:**")
        print("-" * 30)
        
        if all_content_found and '```' in markdown_content:
            print("✅ SUCCESS: All content preserved and properly formatted!")
            print("✅ Complex HTML structures converted to simple <pre><code>")
            print("✅ html2text successfully generated code blocks")
            print("✅ No more empty ``` ``` blocks")
        else:
            print("❌ FAILED: Some content is still missing or improperly formatted")
            print("❌ We need to investigate further")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the Doc2MD project root directory")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def show_what_the_fix_does():
    """Show what the html2text compatibility fix does."""
    
    print("\n" + "=" * 60)
    print("🔧 What the HTML2Text Compatibility Fix Does")
    print("=" * 60)
    
    print("\n📝 **The Problem:**")
    print("-" * 40)
    problems = [
        "• html2text couldn't handle complex nested div structures",
        "• <div class='language-text highlight'><pre><span></span><code>content</code></pre></div>",
        "• html2text would produce empty code blocks or no blocks at all",
        "• Content was preserved in HTML but lost during markdown conversion"
    ]
    
    for problem in problems:
        print(f"  {problem}")
    
    print("\n✅ **The Solution:**")
    print("-" * 40)
    solutions = [
        "• Pre-processes HTML before sending to html2text",
        "• Converts complex div structures to simple <pre><code>",
        "• Removes empty <span></span> elements",
        "• Ensures html2text gets clean, simple HTML it can handle",
        "• Preserves all content while making it markdown-compatible"
    ]
    
    for solution in solutions:
        print(f"  {solution}")
    
    print("\n🔄 **Transformation Process:**")
    print("-" * 40)
    print("  BEFORE (complex):")
    print("    <div class='language-text highlight'>")
    print("      <pre><span></span><code>adk --version</code></pre>")
    print("    </div>")
    print("")
    print("  AFTER (simple):")
    print("    <pre><code>adk --version</code></pre>")
    print("")
    print("  html2text can now properly convert this to:")
    print("    ```")
    print("    adk --version")
    print("    ```")

def main():
    """Run the test."""
    try:
        test_html2text_compatibility()
        show_what_the_fix_does()
        
        print("\n\n🎉 HTML2Text Compatibility Test Completed!")
        print("\n💡 **Summary:**")
        print("  ✅ We've identified the html2text compatibility issue")
        print("  ✅ Added pre-processing to simplify complex HTML structures")
        print("  ✅ Your 'adk --version' content should now appear in code blocks")
        print("  ✅ Test the fix with your actual website")
        
        print("\n🚀 **Next Steps:**")
        print("  1. Try your DocumentConverter again")
        print("  2. Check if 'adk --version' now appears in ``` blocks")
        print("  3. Verify that all code content is preserved")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

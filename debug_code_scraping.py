#!/usr/bin/env python3
"""
Debug script to identify why code content is not being scraped

This script helps debug the issue where content like 'adk --version' 
is not appearing in the final markdown output.
"""

import sys
import os

# Add the doc2md package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'doc2md'))

def test_html_parsing():
    """Test HTML parsing with sample content."""
    
    print("🧪 Testing HTML Parsing and Code Block Detection")
    print("=" * 60)
    
    # Sample HTML that should contain code blocks
    test_html_cases = [
        # Case 1: Standard <pre><code> tags
        {
            "name": "Standard <pre><code> tags",
            "html": '''
            <html>
            <body>
                <h1>Installation Guide</h1>
                <p>To check the version:</p>
                <pre><code>adk --version</code></pre>
                <p>That's it!</p>
            </body>
            </html>
            '''
        },
        
        # Case 2: Just <pre> tags (no <code>)
        {
            "name": "Just <pre> tags (no <code>)",
            "html": '''
            <html>
            <body>
                <h1>Installation Guide</h1>
                <p>To check the version:</p>
                <pre>adk --version</pre>
                <p>That's it!</p>
            </body>
            </html>
            '''
        },
        
        # Case 3: Just <code> tags (no <pre>)
        {
            "name": "Just <code> tags (no <pre>)",
            "html": '''
            <html>
            <body>
                <h1>Installation Guide</h1>
                <p>To check the version:</p>
                <code>adk --version</code>
                <p>That's it!</p>
            </body>
            </html>
            '''
        },
        
        # Case 4: Mixed content
        {
            "name": "Mixed content",
            "html": '''
            <html>
            <body>
                <h1>Installation Guide</h1>
                <p>To check the version:</p>
                <pre><code>adk --version</code></pre>
                <p>Or use:</p>
                <pre>adk --help</pre>
                <p>That's it!</p>
            </body>
            </html>
            '''
        }
    ]
    
    for i, test_case in enumerate(test_html_cases, 1):
        print(f"\n🔍 Test Case {i}: {test_case['name']}")
        print("-" * 50)
        
        # Test the HTML cleaning logic
        test_html_cleaning(test_case['html'], test_case['name'])
        
        # Test the markdown generation logic
        test_markdown_generation(test_case['html'], test_case['name'])

def test_html_cleaning(html_content, test_name):
    """Test the HTML cleaning logic."""
    
    print(f"📝 Testing HTML Cleaning for: {test_name}")
    
    try:
        from markdown_generator import MarkdownGenerator
        
        # Create generator
        generator = MarkdownGenerator("https://example.com", optimize_for_ai=True)
        
        # Test HTML cleaning
        cleaned_html = generator.clean_html(html_content)
        
        print(f"  Original HTML length: {len(html_content)}")
        print(f"  Cleaned HTML length: {len(cleaned_html)}")
        
        # Check if content is preserved
        if 'adk --version' in html_content:
            if 'adk --version' in cleaned_html:
                print("  ✅ 'adk --version' preserved in cleaned HTML")
            else:
                print("  ❌ 'adk --version' LOST during HTML cleaning!")
        else:
            print("  ⚠️  'adk --version' not in original HTML")
        
        # Show what was cleaned
        print(f"  Cleaned HTML preview: {cleaned_html[:200]}...")
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def test_markdown_generation(html_content, test_name):
    """Test the markdown generation logic."""
    
    print(f"📝 Testing Markdown Generation for: {test_name}")
    
    try:
        from markdown_generator import MarkdownGenerator
        
        # Create generator
        generator = MarkdownGenerator("https://example.com", optimize_for_ai=True)
        
        # Test markdown generation
        markdown_content = generator.generate_markdown(html_content, "https://example.com")
        
        print(f"  Generated markdown length: {len(markdown_content)}")
        
        # Check if content is in final output
        if 'adk --version' in markdown_content:
            print("  ✅ 'adk --version' found in final markdown")
            
            # Check if it's in a code block
            if '```' in markdown_content:
                print("  ✅ Code blocks (```) found in markdown")
                
                # Find the code block containing adk --version
                lines = markdown_content.split('\n')
                for i, line in enumerate(lines):
                    if 'adk --version' in line:
                        print(f"  📍 'adk --version' found at line {i}: {repr(line)}")
                        # Check if it's between ``` markers
                        if i > 0 and i < len(lines) - 1:
                            prev_line = lines[i-1].strip()
                            next_line = lines[i+1].strip()
                            if prev_line == '```' and next_line == '```':
                                print("  ✅ 'adk --version' is properly inside code block")
                            else:
                                print("  ❌ 'adk --version' is NOT inside code block")
                        break
            else:
                print("  ❌ No code blocks (```) found in markdown")
        else:
            print("  ❌ 'adk --version' NOT found in final markdown")
        
        # Show markdown preview
        print(f"  Markdown preview: {markdown_content[:300]}...")
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def show_debugging_tips():
    """Show debugging tips for the user."""
    
    print("\n" + "=" * 60)
    print("🔍 Debugging Tips")
    print("=" * 60)
    
    print("\n📋 **Common Issues and Solutions:**")
    print("-" * 40)
    
    issues = [
        {
            "issue": "Content not in HTML",
            "description": "The content was never crawled from the website",
            "solution": "Check if the website uses JavaScript to load content",
            "debug": "Look at the original HTML from the crawler"
        },
        {
            "issue": "Content removed during cleaning",
            "description": "HTML cleaning is too aggressive",
            "solution": "Modify the clean_html method to preserve more content",
            "debug": "Check cleaned HTML vs original HTML"
        },
        {
            "issue": "html2text not processing code blocks",
            "description": "html2text doesn't recognize the HTML structure",
            "solution": "Pre-process HTML to ensure proper <pre><code> structure",
            "debug": "Check html2text output vs cleaned HTML"
        },
        {
            "issue": "Code blocks being stripped",
            "description": "The fix methods are removing content",
            "solution": "Review the _fix_empty_code_blocks logic",
            "debug": "Check markdown at each step of processing"
        }
    ]
    
    for i, issue_info in enumerate(issues, 1):
        print(f"\n🔍 Issue {i}: {issue_info['issue']}")
        print(f"  Description: {issue_info['description']}")
        print(f"  Solution: {issue_info['solution']}")
        print(f"  Debug: {issue_info['debug']}")

def show_next_steps():
    """Show next steps for debugging."""
    
    print("\n" + "=" * 60)
    print("🚀 Next Steps")
    print("=" * 60)
    
    print("\n📝 **To Debug Your Issue:**")
    print("-" * 40)
    
    steps = [
        "1. **Enable Debug Logging**:",
        "   • Set logging level to DEBUG in your script",
        "   • Look for the debug messages we added",
        "",
        "2. **Check Each Step**:",
        "   • Original HTML from crawler",
        "   • HTML after cleaning",
        "   • html2text output",
        "   • Final markdown",
        "",
        "3. **Identify Where Content is Lost**:",
        "   • Is it not crawled?",
        "   • Is it removed during cleaning?",
        "   • Is it lost during markdown conversion?",
        "",
        "4. **Test with Simple HTML**:",
        "   • Try with the test cases above",
        "   • Compare with your actual website HTML"
    ]
    
    for step in steps:
        print(f"  {step}")

def main():
    """Run the debug script."""
    try:
        test_html_parsing()
        show_debugging_tips()
        show_next_steps()
        
        print("\n\n🎉 Debug Script Completed!")
        print("\n💡 **Key Points:**")
        print("  ✅ We've added extensive debugging to Doc2MD")
        print("  ✅ The debug logs will show exactly where content is lost")
        print("  ✅ Test with the sample HTML cases above")
        print("  ✅ Check your website's actual HTML structure")
        
    except Exception as e:
        print(f"\n❌ Debug script failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to verify Doc2MD generates triple backticks (```) for code blocks
"""

import sys
import os

# Add the doc2md package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'doc2md'))

try:
    from markdown_generator import MarkdownGenerator
    
    def test_code_block_generation():
        """Test that code blocks use triple backticks."""
        
        print("🧪 Testing Doc2MD Code Block Generation")
        print("=" * 50)
        
        # Sample HTML with code
        html_content = '''
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Code Examples</h1>
            
            <p>Here's a Python function:</p>
            <pre><code>def hello_world():
    print("Hello, World!")
    return "Success"</code></pre>
            
            <p>And some JavaScript:</p>
            <pre><code>function greet() {
    console.log("Hello from JavaScript!");
}</code></pre>
            
            <p>And HTML:</p>
            <pre><code>&lt;div class="example"&gt;
    &lt;p&gt;This is HTML code&lt;/p&gt;
&lt;/div&gt;</code></pre>
        </body>
        </html>
        '''
        
        # Create markdown generator
        generator = MarkdownGenerator("https://example.com", optimize_for_ai=True)
        
        # Convert to markdown
        markdown_content = generator.generate_markdown(html_content, "https://example.com")
        
        print("📝 Generated Markdown:")
        print("-" * 30)
        print(markdown_content)
        
        print("\n🔍 Verification:")
        print("-" * 30)
        
        # Check for triple backticks
        if "```" in markdown_content:
            print("✅ Triple backticks (```) found in output")
            
            # Count occurrences
            backtick_count = markdown_content.count("```")
            print(f"   Found {backtick_count} triple backtick markers")
            
            # Check for language hints
            if "```python" in markdown_content:
                print("✅ Python language hint found")
            if "```javascript" in markdown_content:
                print("✅ JavaScript language hint found")
            if "```html" in markdown_content:
                print("✅ HTML language hint found")
                
        else:
            print("❌ No triple backticks found")
            
        # Check for [code] syntax (should NOT be present)
        if "[code]" in markdown_content:
            print("❌ [code] syntax found (this should not happen)")
        else:
            print("✅ No [code] syntax found (correct!)")
            
        print("\n🎯 Result:")
        if "```" in markdown_content and "[code]" not in markdown_content:
            print("✅ SUCCESS: Doc2MD is correctly using triple backticks (```)")
        else:
            print("❌ FAILED: Doc2MD is not using the correct syntax")
            
    if __name__ == "__main__":
        test_code_block_generation()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the Doc2MD project root directory")
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()

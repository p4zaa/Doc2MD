#!/usr/bin/env python3
"""
Test script to simulate the exact HTML structure provided by the user

This tests the conversion of:
<div class="language-text highlight"><pre><span></span><code>GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=&lt;your-Google-Gemini-API-key&gt;
</code></pre></div>
"""

def test_exact_html_structure():
    """Test the exact HTML structure provided by the user."""
    
    print("🧪 Testing Exact HTML Structure")
    print("=" * 60)
    
    # The exact HTML structure provided by the user
    test_html = '''<div class="language-text highlight"><pre><span></span><code>GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=&lt;your-Google-Gemini-API-key&gt;
</code></pre></div>'''
    
    print("📝 **Original HTML:**")
    print("-" * 30)
    print(test_html)
    
    print(f"\n🔍 **Content Analysis:**")
    print("-" * 30)
    
    # Check what content is in the HTML
    if 'GOOGLE_GENAI_USE_VERTEXAI=0' in test_html:
        print("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in HTML")
    else:
        print("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in HTML")
    
    if 'GOOGLE_API_KEY=' in test_html:
        print("✅ Found 'GOOGLE_API_KEY=' in HTML")
    else:
        print("❌ 'GOOGLE_API_KEY=' NOT found in HTML")
    
    if '&lt;your-Google-Gemini-API-key&gt;' in test_html:
        print("✅ Found '&lt;your-Google-Gemini-API-key&gt;' in HTML (encoded)")
    else:
        print("❌ '&lt;your-Google-Gemini-API-key&gt;' NOT found in HTML")
    
    print(f"\n🔧 **Testing HTML Pre-processing:**")
    print("-" * 40)
    
    try:
        # Import BeautifulSoup for HTML parsing
        from bs4 import BeautifulSoup
        
        # Parse the HTML
        soup = BeautifulSoup(test_html, 'html.parser')
        
        # Find the div with code classes
        div_tag = soup.find('div', class_='language-text highlight')
        if div_tag:
            print("✅ Found div with 'language-text highlight' classes")
            
            # Find the pre tag
            pre_tag = div_tag.find('pre')
            if pre_tag:
                print("✅ Found <pre> tag inside div")
                
                # Find the code tag
                code_tag = pre_tag.find('code')
                if code_tag:
                    print("✅ Found <code> tag inside <pre>")
                    
                    # Get the code content
                    code_content = code_tag.get_text()
                    print(f"📝 Code content: {repr(code_content)}")
                    
                    # Check for specific lines
                    lines = code_content.split('\n')
                    print(f"📊 Content has {len(lines)} lines:")
                    for i, line in enumerate(lines):
                        if line.strip():
                            print(f"  Line {i+1}: {repr(line)}")
                    
                    # Check for specific content
                    if 'GOOGLE_GENAI_USE_VERTEXAI=0' in code_content:
                        print("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in code content")
                    else:
                        print("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in code content")
                    
                    if 'GOOGLE_API_KEY=' in code_content:
                        print("✅ Found 'GOOGLE_API_KEY=' in code content")
                    else:
                        print("❌ 'GOOGLE_API_KEY=' NOT found in code content")
                    
                    # Test the pre-processing logic
                    print(f"\n🔧 **Testing Pre-processing Logic:**")
                    print("-" * 40)
                    
                    # Simulate the pre-processing logic
                    div_classes = ' '.join(div_tag.get('class', [])).lower()
                    print(f"Div classes: {div_classes}")
                    
                    if any(keyword in div_classes for keyword in ['language', 'highlight', 'code', 'syntax']):
                        print("✅ Div has code-related classes")
                        
                        if pre_tag and pre_tag.find('code'):
                            code_content = pre_tag.find('code').get_text().strip()
                            if code_content:
                                print(f"✅ Found code content: {repr(code_content)}")
                                
                                # Check if this would be processed correctly
                                if 'GOOGLE_GENAI_USE_VERTEXAI=0' in code_content:
                                    print("✅ First line would be preserved")
                                else:
                                    print("❌ First line would be lost")
                            else:
                                print("❌ No code content found")
                        else:
                            print("❌ No <pre><code> structure found")
                    else:
                        print("❌ Div doesn't have code-related classes")
                    
                else:
                    print("❌ No <code> tag found inside <pre>")
            else:
                print("❌ No <pre> tag found inside div")
        else:
            print("❌ No div with 'language-text highlight' classes found")
        
    except ImportError:
        print("❌ BeautifulSoup not available, skipping detailed analysis")
    
    print(f"\n🎯 **Expected Result:**")
    print("-" * 30)
    print("The HTML should be converted to:")
    print("```")
    print("GOOGLE_GENAI_USE_VERTEXAI=0")
    print("GOOGLE_API_KEY=<your-Google-Gemini-API-key>")
    print("```")
    
    print(f"\n🚀 **Next Steps:**")
    print("-" * 30)
    print("1. Run your DocumentConverter with debug=True")
    print("2. Check the debug logs to see where content is lost")
    print("3. The issue might be in html2text conversion")
    print("4. We may need to adjust the HTML pre-processing")

def show_html_structure_analysis():
    """Show analysis of the HTML structure."""
    
    print("\n" + "=" * 60)
    print("🔍 HTML Structure Analysis")
    print("=" * 60)
    
    print("\n📝 **The HTML Structure:**")
    print("-" * 40)
    print("""<div class="language-text highlight">
  <pre>
    <span></span>
    <code>
      GOOGLE_GENAI_USE_VERTEXAI=0
      GOOGLE_API_KEY=&lt;your-Google-Gemini-API-key&gt;
    </code>
  </pre>
</div>""")
    
    print("\n🔍 **Potential Issues:**")
    print("-" * 40)
    issues = [
        "• The <span></span> tag might be interfering with content extraction",
        "• html2text might not handle this nested structure properly",
        "• The encoded &lt; and &gt; might be causing issues",
        "• The multiline content might be split incorrectly"
    ]
    
    for issue in issues:
        print(f"  {issue}")
    
    print("\n✅ **Our Fix Should Handle:**")
    print("-" * 40)
    fixes = [
        "• Detect div with 'language-text highlight' classes",
        "• Extract content from <pre><code> structure",
        "• Remove empty <span> tags",
        "• Preserve multiline content",
        "• Convert to simple <pre><code> structure"
    ]
    
    for fix in fixes:
        print(f"  {fix}")

def main():
    """Run the test."""
    try:
        test_exact_html_structure()
        show_html_structure_analysis()
        
        print("\n\n🎯 **Summary:**")
        print("=" * 60)
        print("✅ We've analyzed the exact HTML structure")
        print("✅ The content IS present in the original HTML")
        print("✅ Our pre-processing should detect and handle it")
        print("✅ The issue might be in the html2text conversion step")
        print("✅ Run with debug=True to see exactly where content is lost")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

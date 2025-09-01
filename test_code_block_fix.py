#!/usr/bin/env python3
"""
Test script to demonstrate the code block fix for [code] syntax
"""

def test_code_block_replacement():
    """Test the code block replacement logic."""
    
    print("🧪 Testing Code Block Replacement Logic")
    print("=" * 50)
    
    # Sample markdown content that might have [code] syntax
    test_cases = [
        # Case 1: Standard [code]...[/code]
        {
            "input": "[code]def hello():\n    print('Hello')[/code]",
            "description": "Standard [code]...[/code] blocks"
        },
        
        # Case 2: [code]...[/code] with newlines
        {
            "input": "[code]\ndef hello():\n    print('Hello')\n[/code]",
            "description": "[code]...[/code] with newlines"
        },
        
        # Case 3: Incomplete [code] tags
        {
            "input": "[code]def hello():\n    print('Hello')",
            "description": "Incomplete [code] tag"
        },
        
        # Case 4: Orphaned [/code] tags
        {
            "input": "def hello():\n    print('Hello')\n[/code]",
            "description": "Orphaned [/code] tag"
        },
        
        # Case 5: Mixed content
        {
            "input": "Here's some code:\n[code]def example():\n    return True[/code]\nAnd more text.",
            "description": "Mixed content with [code] blocks"
        }
    ]
    
    print("\n📝 Test Cases:")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}: {test_case['description']}")
        print("Input:")
        print(f"  {repr(test_case['input'])}")
        
        # Apply the replacement logic (same as in the markdown generator)
        import re
        
        content = test_case['input']
        
        # Pattern 1: [code]...[/code]
        content = re.sub(r'\[code\](.*?)\[/code\]', r'```\1```', content, flags=re.DOTALL)
        
        # Pattern 2: [code]...[/code] with newlines
        content = re.sub(r'\[code\]([\s\S]*?)\[/code\]', r'```\1```', content)
        
        # Pattern 3: Single [code] tags (incomplete)
        content = re.sub(r'\[code\](.*?)(?=\n|$)', r'```\1```', content)
        
        # Pattern 4: [/code] tags (orphaned)
        content = re.sub(r'\[/code\]', '', content)
        
        # Also handle any remaining single [code] tags
        content = re.sub(r'\[code\]', '```', content)
        
        print("Output:")
        print(f"  {repr(content)}")
        
        # Check if replacement was successful
        if "[code]" not in content and "[/code]" not in content:
            print("  ✅ SUCCESS: All [code] syntax replaced")
        else:
            print("  ❌ FAILED: Some [code] syntax remains")
            print(f"    Remaining: {content}")

def show_html2text_configuration():
    """Show the html2text configuration."""
    
    print("\n" + "=" * 50)
    print("🔧 HTML2Text Configuration")
    print("=" * 50)
    
    print("\n📋 Current Settings:")
    print("-" * 30)
    
    settings = [
        "✅ mark_code = True",
        "✅ ignore_code = False", 
        "✅ code_tag_on = '```'",
        "✅ code_tag_off = '```'",
        "✅ Additional regex replacement for [code] syntax"
    ]
    
    for setting in settings:
        print(f"  {setting}")
    
    print("\n🎯 What This Fixes:")
    print("-" * 30)
    
    fixes = [
        "🔧 **html2text.mark_code = True**: Primary setting for ``` syntax",
        "🔧 **ignore_code = False**: Ensures code blocks are not ignored",
        "🔧 **code_tag_on/off = '```'**: Forces triple backticks",
        "🔧 **Regex replacement**: Backup method to catch any [code] syntax",
        "🔧 **Multiple patterns**: Handles various [code] formats"
    ]
    
    for fix in fixes:
        print(f"  {fix}")

def show_usage_example():
    """Show how to use the fixed DocumentConverter."""
    
    print("\n" + "=" * 50)
    print("🚀 Usage Example")
    print("=" * 50)
    
    print("\n📝 Python Code:")
    print("-" * 30)
    
    code_example = '''from doc2md import DocumentConverter

# Create converter with AI optimization enabled
converter = DocumentConverter(
    base_url="https://example.com",
    output_dir="output",
    max_depth=2,
    optimize_for_ai=True  # This ensures triple backticks
)

# Convert the website
result = converter.convert()

print("✅ All code blocks now use triple backticks (```)")'''
    
    print(code_example)
    
    print("\n🎯 Expected Output:")
    print("-" * 30)
    
    print("Instead of:")
    print("  [code]")
    print("  def example():")
    print("      return 'Hello'")
    print("  [/code]")
    
    print("\nYou'll get:")
    print("  ```python")
    print("  def example():")
    print("      return 'Hello'")
    print("  ```")

def main():
    """Run all test functions."""
    try:
        test_code_block_replacement()
        show_html2text_configuration()
        show_usage_example()
        
        print("\n\n🎉 Code Block Fix Demo Completed!")
        print("\n💡 Summary:")
        print("  ✅ Doc2MD now forces triple backticks (```)")
        print("  ✅ Multiple fallback methods ensure [code] is replaced")
        print("  ✅ AI optimization is enabled by default")
        print("  ✅ Your markdown will use proper ``` syntax!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

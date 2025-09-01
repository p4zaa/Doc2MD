#!/usr/bin/env python3
"""
Test script to demonstrate the new token-optimized AI optimization level.
"""

from doc2md import DocumentConverter

def test_token_optimization():
    """Test the new token-optimized AI optimization level."""
    
    print("🧪 Testing Token-Optimized AI Optimization Level")
    print("=" * 60)
    
    # Test HTML content with various elements that can be optimized
    test_html = """
    <html>
    <head><title>Token Optimization Test</title></head>
    <body>
        <h1>Main Heading with Excessive Spaces</h1>
        
        
        <p>This paragraph has    excessive    spaces    between    words.</p>
        
        <h2>Another Section</h2>
        
        <p>More content with redundant punctuation!!!</p>
        
        <h3>Subsection</h3>
        
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
            <li>Item 3</li>
        </ul>
        
        <pre><code>def example_function():
    print("Hello World")
    return True</code></pre>
        
        <p>Text with excessive dashes --- and underscores ___</p>
        
        <h4>Deep Subsection</h4>
        
        <p>Content with multiple punctuation marks???</p>
    </body>
    </html>
    """
    
    test_cases = [
        {
            "name": "Minimal AI Optimization",
            "ai_optimization_level": "minimal",
            "description": "Basic code block formatting"
        },
        {
            "name": "Standard AI Optimization",
            "ai_optimization_level": "standard",
            "description": "Language hints and basic enhancement"
        },
        {
            "name": "Enhanced AI Optimization",
            "ai_optimization_level": "enhanced",
            "description": "Semantic markers and advanced enhancement"
        },
        {
            "name": "Token-Optimized AI Optimization",
            "ai_optimization_level": "token-optimized",
            "description": "Maximum token reduction for cost-effective RAG"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        print(f"   AI Optimization Level: {test_case['ai_optimization_level'].title()}")
        
        # Create converter with specific settings
        converter = DocumentConverter(
            base_url="https://example.com",
            output_dir=f"test_{test_case['ai_optimization_level']}",
            generate_readme=False,
            raw_output=False,
            force_triple_backticks=True,
            ai_optimization_level=test_case['ai_optimization_level'],
            reduce_empty_lines=True
        )
        
        # Generate markdown
        markdown_output = converter.markdown_generator.generate_markdown(
            test_html, 
            "https://example.com/token-test"
        )
        
        # Analyze token optimization
        lines = markdown_output.split('\n')
        total_chars = len(markdown_output)
        total_words = len(markdown_output.split())
        empty_lines = sum(1 for line in lines if line.strip() == '')
        semantic_markers = markdown_output.count('<!--')
        excessive_spaces = len([line for line in lines if '  ' in line])
        
        print("   Output analysis:")
        print(f"   - Total characters: {total_chars}")
        print(f"   - Total words: {total_words}")
        print(f"   - Empty lines: {empty_lines}")
        print(f"   - Semantic markers: {semantic_markers}")
        print(f"   - Lines with excessive spaces: {excessive_spaces}")
        
        # Calculate rough token estimate (approximate)
        rough_tokens = total_chars // 4  # Rough estimate: 4 chars per token
        print(f"   - Rough token estimate: ~{rough_tokens}")
        
        # Show sample of output
        print("   Sample output (first 12 lines):")
        for j, line in enumerate(lines[:12]):
            if line.strip() == '':
                print(f"   {j+1:2d}: [EMPTY]")
            else:
                # Truncate long lines for display
                display_line = line[:60] + '...' if len(line) > 60 else line
                print(f"   {j+1:2d}: {display_line}")
        
        print("   " + "-" * 60)
    
    print(f"\n🎯 Key Benefits of Token-Optimized Level:")
    print("   - Maximum token reduction for cost-effective RAG systems")
    print("   - Removes excessive whitespace and punctuation")
    print("   - Eliminates semantic markers to save tokens")
    print("   - Standardizes formatting for consistency")
    print("   - Maintains readability while minimizing tokens")
    print("   - Perfect for high-volume RAG operations")
    
    print(f"\n💡 Use Cases:")
    print("   - Cost-sensitive RAG systems")
    print("   - High-volume document processing")
    print("   - When token count directly impacts costs")
    print("   - Batch processing of large document collections")
    print("   - Production RAG systems with budget constraints")

if __name__ == "__main__":
    test_token_optimization()

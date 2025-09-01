#!/usr/bin/env python3
"""
Demo Script for Doc2MD

This script demonstrates the basic functionality of the Doc2MD library.
It shows how to convert a simple HTML page to markdown format.
"""

from doc2md import DocumentConverter, MarkdownGenerator
import tempfile
import os
from pathlib import Path

def demo_simple_conversion():
    """Demonstrate simple HTML to markdown conversion."""
    print("🚀 Doc2MD Demo - Simple HTML to Markdown Conversion")
    print("=" * 60)
    
    # Sample HTML content (simulating a web page)
    sample_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google ADK Documentation</title>
        <meta name="description" content="Agent Development Kit documentation for AI agents">
        <meta name="keywords" content="AI, agents, Google, ADK, documentation">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/get-started">Get Started</a></li>
                    <li><a href="/tutorials">Tutorials</a></li>
                </nav>
            </header>
        
        <main>
            <h1>Welcome to Google ADK Documentation</h1>
            <p>This is a <strong>sample page</strong> that demonstrates how Doc2MD works with the Google ADK docs.</p>
            
            <h2>Features</h2>
            <ul>
                <li>Clean HTML to Markdown conversion</li>
                <li>Automatic link processing</li>
                <li>Metadata extraction</li>
                <li>Organized folder structure</li>
            </ul>
            
            <h2>Code Example</h2>
            <pre><code>from doc2md import DocumentConverter

converter = DocumentConverter("https://google.github.io/adk-docs/")
result = converter.convert()
print(f"Converted {result['total_files_generated']} pages!")</code></pre>
            
            <h2>Getting Started</h2>
            <p>To get started with Doc2MD:</p>
            <ol>
                <li>Install the library: <code>pip install doc2md</code></li>
                <li>Import the converter: <code>from doc2md import DocumentConverter</code></li>
                <li>Convert your first site: <code>converter.convert()</code></li>
            </ol>
            
            <h3>Advanced Configuration</h3>
            <p>You can customize the conversion process with various options:</p>
            <ul>
                <li><strong>Depth Control:</strong> Limit crawling depth</li>
                <li><strong>Request Delay:</strong> Control crawling speed</li>
                <li><strong>Output Directory:</strong> Specify where files are saved</li>
            </ul>
        </main>
        
        <footer>
            <p>&copy; 2024 Google ADK Documentation. Made with ❤️ using Doc2MD.</p>
        </footer>
    </body>
    </html>
    """
    
    print("📄 Sample HTML Content:")
    print("-" * 40)
    print("Title: Sample Documentation Page")
    print("Description: A sample page for demonstration")
    print("Content: Welcome page with features, code examples, and getting started guide")
    print()
    
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Output Directory: {temp_dir}")
        
        # Initialize the markdown generator
        md_generator = MarkdownGenerator("https://docs.example.com")
        
        # Convert HTML to markdown
        print("\n🔄 Converting HTML to Markdown...")
        markdown_content = md_generator.generate_markdown(
            sample_html, 
            "https://docs.example.com"
        )
        
        # Save the markdown file
        output_file = Path(temp_dir) / "sample_page.md"
        output_file.write_text(markdown_content, encoding='utf-8')
        
        print(f"✅ Markdown file saved: {output_file}")
        
        # Display the generated markdown
        print("\n📝 Generated Markdown Content:")
        print("-" * 40)
        print(markdown_content)
        print("-" * 40)
        
        # Show file statistics
        file_size = output_file.stat().st_size
        print(f"\n📊 File Statistics:")
        print(f"  File size: {file_size} bytes")
        print(f"  Lines: {len(markdown_content.splitlines())}")
        print(f"  Characters: {len(markdown_content)}")

def demo_converter_initialization():
    """Demonstrate converter initialization and configuration."""
    print("\n\n🔧 Doc2MD Demo - Converter Configuration")
    print("=" * 60)
    
    # Show different configuration options
    configs = [
        {
            "name": "Basic Configuration",
            "config": {"base_url": "https://google.github.io/adk-docs/", "output_dir": "docs"}
        },
        {
            "name": "Limited Depth",
            "config": {"base_url": "https://google.github.io/adk-docs/", "output_dir": "docs", "max_depth": 2}
        },
        {
            "name": "Respectful Crawling",
            "config": {"base_url": "https://google.github.io/adk-docs/", "output_dir": "docs", "delay": 2.0}
        },
        {
            "name": "Full Configuration",
            "config": {
                "base_url": "https://google.github.io/adk-docs/",
                "output_dir": "my_documentation",
                "max_depth": 3,
                "delay": 1.5
            }
        }
    ]
    
    for config in configs:
        print(f"\n📋 {config['name']}:")
        print("  Configuration:")
        for key, value in config['config'].items():
            if key == "max_depth" and value == 0:
                print(f"    {key}: {value} (unlimited)")
            else:
                print(f"    {key}: {value}")
        
        # Create converter instance (but don't run it)
        try:
            converter = DocumentConverter(**config['config'])
            print(f"  ✅ Valid configuration")
        except Exception as e:
            print(f"  ❌ Invalid configuration: {e}")

def demo_usage_examples():
    """Show usage examples."""
    print("\n\n💡 Doc2MD Demo - Usage Examples")
    print("=" * 60)
    
    examples = [
        {
            "title": "Simple Conversion",
            "code": """from doc2md import DocumentConverter

converter = DocumentConverter("https://google.github.io/adk-docs/")
result = converter.convert()
print(f"Converted {result['total_files_generated']} pages!")""",
            "description": "Basic usage with default settings"
        },
        {
            "title": "Preview Mode",
            "code": """# Preview before converting
preview = converter.preview_conversion()
if 'error' not in preview:
    print(f"Estimated pages: {preview['estimated_pages']}")
    print(f"Domain: {preview['domain']}")""",
            "description": "See what the conversion would look like"
        },
        {
            "title": "URL Validation",
            "code": """# Validate URL before converting
if converter.validate_url():
    result = converter.convert()
    print("Conversion successful!")
else:
    print("URL is not accessible")""",
            "description": "Check accessibility before starting"
        },
        {
            "title": "Error Handling",
            "code": """try:
    result = converter.convert()
except Exception as e:
    print(f"Conversion failed: {e}")
    # Try with different settings
    converter.delay = 5.0
    converter.max_depth = 1""",
            "description": "Handle errors gracefully"
        }
    ]
    
    for example in examples:
        print(f"\n📚 {example['title']}:")
        print(f"  Description: {example['description']}")
        print("  Code:")
        print("    " + "\n    ".join(example['code'].split('\n')))

def main():
    """Run all demo functions."""
    try:
        demo_simple_conversion()
        demo_converter_initialization()
        demo_usage_examples()
        
        print("\n\n🎉 Demo completed successfully!")
        print("\n💡 To try the actual conversion:")
        print("   1. Replace 'https://docs.example.com' with a real documentation site")
        print("   2. Run: python examples/basic_usage.py")
        print("   3. Or use the CLI: doc2md convert <your-url>")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

# Doc2MD - Web Document to Markdown Converter

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/doc2md.svg)](https://badge.fury.io/py/doc2md)

A comprehensive Python library for converting web documents to markdown format with configurable crawling depth, organized folder structure, and navigation trees.

## 🚀 Features

- **🌐 Smart Web Crawling**: Automatically discovers and crawls all pages under a document domain and path
- **📊 Depth Control**: Set crawl depth (0 = unlimited, N = N levels deep)
- **📝 Clean Markdown**: Converts HTML to clean, readable markdown format
- **📁 Organized Structure**: Creates nested folders mirroring the original site hierarchy
- **🔗 Link Preservation**: Updates internal links to point to local markdown files
- **🧭 Navigation**: Generates comprehensive README files and navigation trees
- **⚡ Performance**: Configurable delays and respectful crawling
- **🛠️ CLI Interface**: Easy-to-use command-line tool
- **📚 API**: Full programmatic access to all functionality
- **🚫 URL Exclusion**: Exclude specific URLs or URL patterns from crawling
- **🤖 AI Optimization**: Optimized markdown output for RAG databases and AI agents

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install doc2md
```

### From Source

```bash
git clone https://github.com/yourusername/doc2md.git
cd doc2md
pip install -e .
```

### Dependencies

The library requires Python 3.7+ and the following packages:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `html2text` - HTML to markdown conversion
- `click` - CLI interface
- `tqdm` - Progress bars

## 🎯 Quick Start

### Path Restriction Behavior

Doc2MD automatically restricts crawling to URLs under the specified base path. For example:

- **`https://google.github.io/adk-docs/`** - Only crawls URLs under `/adk-docs/`
- **`https://google.github.io/`** - Crawls all URLs under the entire domain
- **`https://google.github.io/adk-docs/tutorials/`** - Only crawls URLs under `/adk-docs/tutorials/`

This ensures you only convert the specific documentation section you're interested in, not the entire website.

### AI Agent & RAG Optimization

Doc2MD automatically optimizes markdown output for AI agents and RAG (Retrieval-Augmented Generation) systems:

**Code Block Formatting:**
- Uses standard triple backticks (```) for code blocks
- Automatically detects and adds language hints (```python, ```java, ```html)
- **Fixes empty code blocks** (``` ``` → ```content```)
- **Preserves orphaned content** (content outside blocks → inside blocks)
- Maintains clean, structured markdown for better AI parsing

**Benefits for AI Systems:**
- **Better Vector Embeddings**: Clear semantic boundaries for chunking
- **Improved Code Understanding**: Language-specific syntax highlighting
- **Enhanced Context Awareness**: Clear separation between code and text
- **RAG Database Friendly**: Optimized for vector database storage and retrieval

**Example Output:**
```markdown
# Installation Guide

Here's how to install the package:

```bash
pip install doc2md
```

For development installation:

```bash
pip install -e .
```
```

### URL Exclusion

You can exclude specific URLs or URL patterns from crawling using the `--exclude` flag:

```bash
# Exclude API reference pages
doc2md convert https://google.github.io/adk-docs/ --exclude "https://google.github.io/adk-docs/api-reference/"

# Exclude multiple patterns
doc2md convert https://google.github.io/adk-docs/ \
  --exclude "https://google.github.io/adk-docs/api-reference/" \
  --exclude "https://google.github.io/adk-docs/admin/" \
  --exclude "https://google.github.io/adk-docs/internal/"
```

**Exclusion Rules:**
- **Exact match**: `https://google.github.io/adk-docs/api-reference/java` excludes only that page
- **Path pattern**: `https://google.github.io/adk-docs/api-reference/` excludes all pages under that path
- **Multiple exclusions**: Use multiple `--exclude` flags for different patterns
- **Normalized**: URLs are automatically normalized (query parameters and fragments are removed)

### Command Line Usage

```bash
# Convert entire documentation site (unlimited depth)
doc2md convert https://google.github.io/adk-docs/

# Convert with limited depth (2 levels)
doc2md convert https://google.github.io/adk-docs/ --depth 2

# Exclude specific URLs or patterns
doc2md convert https://google.github.io/adk-docs/ --exclude "https://google.github.io/adk-docs/api-reference/" --exclude "https://google.github.io/adk-docs/admin/"

# Specify output directory
doc2md convert https://google.github.io/adk-docs/ --output my_docs

# Preview conversion without converting
doc2md preview https://google.github.io/adk-docs/

# Validate URL accessibility
doc2md validate https://google.github.io/adk-docs/
```

### Programmatic Usage

```python
from doc2md import DocumentConverter

# Create converter
converter = DocumentConverter(
    base_url="https://google.github.io/adk-docs/",
    output_dir="docs",
    max_depth=0,  # 0 = unlimited
    delay=1.0,    # 1 second between requests
    exclude_urls=["https://google.github.io/adk-docs/api-reference/"]  # Exclude API docs
)

# Convert the entire site
result = converter.convert()

print(f"Converted {result['total_files_generated']} pages!")
```

## 📚 Detailed Usage

### Basic Conversion

```python
from doc2md import DocumentConverter

# Simple conversion
converter = DocumentConverter("https://google.github.io/adk-docs/")
result = converter.convert()
```

### Advanced Configuration

```python
from doc2md import DocumentConverter

# Advanced configuration
converter = DocumentConverter(
    base_url="https://google.github.io/adk-docs/",
    output_dir="my_documentation",
    max_depth=3,        # Crawl 3 levels deep
    delay=2.0           # Wait 2 seconds between requests
)

# Validate before converting
if converter.validate_url():
    result = converter.convert()
    print(f"Success! Generated {result['total_files_generated']} files")
else:
    print("URL is not accessible")
```

### Preview Mode

```python
# Preview what the conversion would look like
preview = converter.preview_conversion()

if 'error' not in preview:
    print(f"Estimated pages: {preview['estimated_pages']}")
    print(f"Domain: {preview['domain']}")
    
    print("Sample file structure:")
    for url, local_path in preview['sample_file_structure'].items():
        print(f"  {url} → {local_path}")
```

### Custom Components

```python
from doc2md import WebCrawler, MarkdownGenerator, LinkTreeGenerator

# Use individual components
crawler = WebCrawler("https://google.github.io/adk-docs/", max_depth=2)
content = crawler.crawl()

md_generator = MarkdownGenerator("https://google.github.io/adk-docs/")
for url, html in content.items():
    markdown = md_generator.generate_markdown(html, url)
    # Save markdown content...
```

## 📁 Output Structure

The library creates a well-organized folder structure:

```
docs/
├── README.md              # Main navigation and overview
├── NAVIGATION.md          # Complete site map
├── index.md               # Home page
├── getting_started/
│   ├── README.md          # Folder navigation
│   ├── index.md           # Getting started page
│   └── installation.md    # Installation guide
└── guides/
    ├── README.md          # Folder navigation
    ├── index.md           # Guides overview
    ├── advanced/
    │   └── tips.md        # Advanced tips
    └── faq.md             # FAQ page
```

## ⚙️ Configuration Options

### Crawler Settings

- **`max_depth`**: Maximum crawl depth (0 = unlimited)
- **`delay`**: Delay between requests in seconds
- **`User-Agent`**: Custom user agent string
- **`path_restriction`**: Automatically restricts crawling to URLs under the specified base path

### Markdown Generation

- **HTML Cleaning**: Removes scripts, styles, navigation elements
- **Link Processing**: Updates internal links to local files
- **Metadata Extraction**: Preserves page titles and meta information
- **AI Optimization**: Uses triple backticks (```) for code blocks with language hints
- **Missing First Lines Fix**: Automatically detects and reconstructs missing first lines in code blocks
- **Content Reconstruction**: Rebuilds incomplete code blocks and places orphaned content properly
- **RAG Friendly**: Structured output optimized for vector databases and AI agents

### Output Organization

- **Folder Structure**: Mirrors original site hierarchy
- **File Naming**: Clean, readable filenames
- **Navigation**: Comprehensive README files in each folder

## 🔧 Advanced Features

### Batch Processing

```python
sites = [
    "https://docs.site1.com",
    "https://docs.site2.com",
    "https://docs.site3.com"
]

for site in sites:
    converter = DocumentConverter(site, output_dir=f"output/{site.split('//')[1]}")
    try:
        result = converter.convert()
        print(f"✅ {site}: {result['total_files_generated']} files")
    except Exception as e:
        print(f"❌ {site}: {e}")
```

### Error Handling

```python
try:
    result = converter.convert()
except Exception as e:
    print(f"Conversion failed: {e}")
    
    # Try with different settings
    converter.delay = 5.0  # Increase delay
    converter.max_depth = 1  # Reduce depth
    
    if converter.validate_url():
        result = converter.convert()
```

### Custom HTML Cleaning

```python
from doc2md import MarkdownGenerator

generator = MarkdownGenerator("https://docs.example.com")

# Custom HTML content
html_content = "<h1>Custom Content</h1><p>Your HTML here</p>"
markdown = generator.generate_markdown(html_content, "https://docs.example.com")
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=doc2md
```

## 📖 Examples

Check the `examples/` directory for complete working examples:

- `basic_usage.py` - Simple conversion examples
- `advanced_usage.py` - Advanced features and configurations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [html2text](https://github.com/Alir3z4/html2text) for HTML to markdown conversion
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Click](https://click.palletsprojects.com/) for the CLI framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/doc2md/issues)
- **Documentation**: [GitHub README](https://github.com/yourusername/doc2md#readme)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/doc2md/discussions)

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Core conversion functionality
- CLI interface
- Comprehensive testing
- Documentation and examples

---

**Made with ❤️ for the documentation community**
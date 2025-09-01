"""
Markdown Generator Module

Converts HTML content to clean markdown format with proper formatting
and link preservation.
"""

import html2text
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Converts HTML content to clean markdown format."""
    
    def __init__(self, base_url: str, optimize_for_ai: bool = True):
        """
        Initialize the markdown generator.
        
        Args:
            base_url: Base URL for resolving relative links
            optimize_for_ai: Whether to optimize output for AI agents and RAG systems
        """
        self.base_url = base_url
        self.optimize_for_ai = optimize_for_ai
        
        # Configure html2text for better markdown output optimized for AI agents
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_emphasis = False
        self.h2t.ignore_tables = False
        self.h2t.body_width = 0  # No line wrapping
        self.h2t.unicode_snob = True
        self.h2t.escape_snob = True
        self.h2t.mark_code = True  # Use ``` for code blocks (better for AI agents)
        self.h2t.wrap_links = False
        self.h2t.bypass_tables = False  # Better table handling
        self.h2t.default_image_alt = "Image"  # Descriptive alt text for images
        
        # Additional settings to ensure proper code block handling
        self.h2t.ignore_code = False  # Don't ignore code blocks
        self.h2t.code_tag_on = "```"  # Force triple backticks
        self.h2t.code_tag_off = "```"  # Force triple backticks
        
        # Better handling of complex HTML structures
        self.h2t.ignore_emphasis = False  # Keep emphasis for better code formatting
        self.h2t.ignore_images = False  # Keep images
        self.h2t.ignore_tables = False  # Keep tables
        self.h2t.body_width = 0  # No line wrapping for code blocks
        
    def clean_html(self, html_content: str) -> str:
        """Clean HTML content by removing unnecessary elements while preserving code blocks."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Remove common navigation and utility classes
        for element in soup.find_all(class_=re.compile(r'(nav|menu|sidebar|footer|header|breadcrumb)')):
            element.decompose()
        
        # Remove elements with common utility classes
        utility_classes = ['advertisement', 'ads', 'social-share', 'related-posts']
        for class_name in utility_classes:
            for element in soup.find_all(class_=re.compile(class_name, re.IGNORECASE)):
                element.decompose()
        
        # Special handling for code blocks - ensure they're preserved
        # Look for various code block structures and preserve them
        for pre_tag in soup.find_all('pre'):
            pre_content = pre_tag.get_text().strip()
            logger.debug(f"Found <pre> tag with content: {repr(pre_content[:100])}")
            
            if pre_tag.find('code'):
                # Ensure the code tag has content
                code_tag = pre_tag.find('code')
                code_content = code_tag.get_text().strip()
                if not code_content:
                    logger.debug("Found empty <pre><code> tag, removing it")
                    pre_tag.decompose()
                else:
                    logger.debug(f"Preserving <pre><code> block with content: {repr(code_content[:100])}")
            else:
                # If <pre> doesn't have <code>, preserve it if it has content
                if not pre_content:
                    logger.debug("Found empty <pre> tag, removing it")
                    pre_tag.decompose()
                else:
                    logger.debug(f"Preserving <pre> block without <code> tag: {repr(pre_content[:100])}")
        
        # Also look for <code> tags that might not be inside <pre>
        for code_tag in soup.find_all('code'):
            code_content = code_tag.get_text().strip()
            if code_content:
                logger.debug(f"Found standalone <code> tag: {repr(code_content[:100])}")
            else:
                logger.debug("Found empty <code> tag, removing it")
                code_tag.decompose()
        
        # Look for div containers with code-related classes that contain <pre><code>
        # This handles cases like <div class="language-text highlight"><pre><code>content</code></pre></div>
        for div_tag in soup.find_all('div'):
            div_classes = ' '.join(div_tag.get('class', [])).lower()
            
            # Check if this div has code-related classes
            if any(keyword in div_classes for keyword in ['language', 'highlight', 'code', 'syntax']):
                logger.debug(f"Found div with code-related classes: {div_classes}")
                
                # Look for <pre><code> inside this div
                pre_code = div_tag.find('pre')
                if pre_code and pre_code.find('code'):
                    code_content = pre_code.find('code').get_text().strip()
                    if code_content:
                        logger.debug(f"Preserving div with <pre><code> content: {repr(code_content[:100])}")
                    else:
                        logger.debug("Found div with empty <pre><code>, removing it")
                        div_tag.decompose()
                else:
                    logger.debug(f"Div has code classes but no <pre><code> structure")
        
        # Clean up empty spans that might break code block detection
        for span_tag in soup.find_all('span'):
            if not span_tag.get_text().strip() and not span_tag.get('class'):
                logger.debug("Removing empty span tag that might interfere with code blocks")
                span_tag.decompose()
        
        return str(soup)
    
    def _preprocess_for_html2text(self, html_content: str) -> str:
        """
        Pre-process HTML to make it more compatible with html2text.
        
        This converts complex nested structures to simpler ones that html2text
        can properly convert to markdown code blocks.
        
        Args:
            html_content: Cleaned HTML content
            
        Returns:
            Pre-processed HTML content optimized for html2text
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all div containers with code-related classes that contain <pre><code>
        for div_tag in soup.find_all('div'):
            div_classes = ' '.join(div_tag.get('class', [])).lower()
            
            # Check if this div has code-related classes
            if any(keyword in div_classes for keyword in ['language', 'highlight', 'code', 'syntax']):
                logger.debug(f"Processing div with code classes: {div_classes}")
                
                # Look for <pre><code> inside this div
                pre_tag = div_tag.find('pre')
                if pre_tag and pre_tag.find('code'):
                    code_tag = pre_tag.find('code')
                    code_content = code_tag.get_text().strip()
                    
                    if code_content:
                        logger.debug(f"Found code content: {repr(code_content[:100])}")
                        
                        # Check if this is multiline content
                        content_lines = code_content.split('\n')
                        logger.debug(f"Content has {len(content_lines)} lines")
                        for i, line in enumerate(content_lines):
                            if line.strip():
                                logger.debug(f"  Line {i+1}: {repr(line)}")
                        
                        # Debug: Check for specific content in the extracted code
                        if 'GOOGLE_GENAI_USE_VERTEXAI=0' in code_content:
                            logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in extracted code content")
                        else:
                            logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in extracted code content")
                        
                        if 'GOOGLE_API_KEY=' in code_content:
                            logger.debug("✅ Found 'GOOGLE_API_KEY=' in extracted code content")
                        else:
                            logger.warning("❌ 'GOOGLE_API_KEY=' NOT found in extracted code content")
                        
                        # Replace the entire div with a simple <pre><code> structure
                        # This ensures html2text can properly convert it
                        new_pre = soup.new_tag('pre')
                        new_code = soup.new_tag('code')
                        
                        # Preserve the exact content including whitespace and newlines
                        new_code.string = code_content
                        new_pre.append(new_code)
                        
                        # Replace the div with the simplified structure
                        div_tag.replace_with(new_pre)
                        logger.debug(f"Replaced complex div structure with simple <pre><code>")
                        logger.debug(f"New structure: <pre><code>{repr(code_content)}</code></pre>")
                    else:
                        logger.debug("Div has no code content, removing it")
                        div_tag.decompose()
        
        # Also clean up any remaining empty spans that might interfere
        for span_tag in soup.find_all('span'):
            if not span_tag.get_text().strip() and not span_tag.get('class'):
                span_tag.decompose()
        
        return str(soup)
    
    def process_links(self, html_content: str, url_mapping: Dict[str, str]) -> str:
        """
        Process internal links to point to local markdown files.
        
        Args:
            html_content: HTML content to process
            url_mapping: Mapping of URLs to local file paths
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(self.base_url, href)
            
            # Check if this is an internal link we've crawled
            if absolute_url in url_mapping:
                local_path = url_mapping[absolute_url]
                # Convert to relative markdown link
                link['href'] = local_path
                # Update link text to show it's a local link
                if link.get_text().strip():
                    link.string = f"{link.get_text()} (local)"
        
        return str(soup)
    
    def extract_metadata(self, html_content: str) -> Dict[str, str]:
        """Extract metadata from HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        metadata = {}
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        # Extract title
        title = soup.find('title')
        if title:
            metadata['title'] = title.get_text().strip()
        
        # Extract first h1 as main heading
        h1 = soup.find('h1')
        if h1:
            metadata['main_heading'] = h1.get_text().strip()
        
        return metadata
    
    def generate_markdown(self, html_content: str, url: str, url_mapping: Dict[str, str] = None) -> str:
        """
        Convert HTML content to markdown format.
        
        Args:
            html_content: HTML content to convert
            url: Original URL of the page
            url_mapping: Mapping of URLs to local file paths for link processing
            
        Returns:
            Clean markdown content
        """
        try:
            # Debug: Check original HTML content
            logger.debug(f"Original HTML content length: {len(html_content)}")
            if 'adk --version' in html_content:
                logger.debug("✅ Found 'adk --version' in original HTML")
            else:
                logger.warning("❌ 'adk --version' NOT found in original HTML")
            
            # Debug: Check for the specific content we're looking for
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in html_content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in original HTML")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in original HTML")
            
            if 'GOOGLE_API_KEY=' in html_content:
                logger.debug("✅ Found 'GOOGLE_API_KEY=' in original HTML")
            else:
                logger.warning("❌ 'GOOGLE_API_KEY=' NOT found in original HTML")
            
            # Clean the HTML
            cleaned_html = self.clean_html(html_content)
            
            # Debug: Check cleaned HTML content
            logger.debug(f"Cleaned HTML content length: {len(cleaned_html)}")
            if 'adk --version' in cleaned_html:
                logger.debug("✅ Found 'adk --version' in cleaned HTML")
            else:
                logger.warning("❌ 'adk --version' NOT found in cleaned HTML")
            
            # Pre-process HTML for better html2text compatibility
            # This converts complex structures to simpler ones that html2text can handle
            processed_html = self._preprocess_for_html2text(cleaned_html)
            
            # Debug: Check processed HTML
            logger.debug(f"Processed HTML content length: {len(processed_html)}")
            if 'adk --version' in processed_html:
                logger.debug("✅ Found 'adk --version' in processed HTML")
            else:
                logger.warning("❌ 'adk --version' NOT found in processed HTML")
            
            # Process internal links if mapping provided
            if url_mapping:
                processed_html = self.process_links(processed_html, url_mapping)
            
            # Extract metadata
            metadata = self.extract_metadata(cleaned_html)
            
            # Convert to markdown
            markdown_content = self.h2t.handle(processed_html)
            
            # Debug: Check what html2text generated
            logger.debug(f"html2text output length: {len(markdown_content)}")
            logger.debug(f"html2text first 300 chars: {markdown_content[:300]}")
            
            # Debug: Check for specific content in html2text output
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in html2text output")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in html2text output")
            
            if 'GOOGLE_API_KEY=' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_API_KEY=' in html2text output")
            else:
                logger.warning("❌ 'GOOGLE_API_KEY=' NOT found in html2text output")
            
            # Debug: Show the actual html2text output around the content
            if 'GOOGLE_API_KEY=' in markdown_content:
                lines = markdown_content.split('\n')
                for i, line in enumerate(lines):
                    if 'GOOGLE_API_KEY=' in line:
                        logger.debug(f"📍 Found GOOGLE_API_KEY at line {i}: {repr(line)}")
                        # Show surrounding lines
                        start = max(0, i-3)
                        end = min(len(lines), i+4)
                        logger.debug("🔍 Surrounding lines:")
                        for j in range(start, end):
                            marker = ">>> " if j == i else "    "
                            logger.debug(f"{marker}Line {j}: {repr(lines[j])}")
                        break
            
            # Debug: Check for specific content we're looking for
            if 'adk --version' in markdown_content:
                logger.debug("✅ Found 'adk --version' in html2text output")
            else:
                logger.warning("❌ 'adk --version' NOT found in html2text output")
                # Let's check if it's in the cleaned HTML
                if 'adk --version' in cleaned_html:
                    logger.debug("✅ Found 'adk --version' in cleaned HTML")
                    logger.warning("❌ Content lost during html2text conversion!")
                    
                    # Debug: Show what html2text actually produced
                    logger.debug(f"html2text output preview: {repr(markdown_content[:500])}")
                    
                    # Check if html2text produced any code blocks at all
                    if '```' in markdown_content:
                        logger.debug("✅ html2text produced some code blocks")
                        # Count code blocks
                        code_block_count = markdown_content.count('```')
                        logger.debug(f"Found {code_block_count} triple backticks in html2text output")
                    else:
                        logger.warning("❌ html2text produced NO code blocks at all!")
                        
                    # Check for [code] syntax
                    if '[code]' in markdown_content:
                        logger.debug("✅ html2text produced [code] syntax")
                    else:
                        logger.debug("ℹ️  html2text produced neither ``` nor [code] syntax")
                else:
                    logger.warning("❌ 'adk --version' NOT found in cleaned HTML either")
            
            # Additional debugging for missing first lines
            logger.debug("🔍 Checking for missing first lines in code blocks...")
            if 'GOOGLE_API_KEY' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_API_KEY' in html2text output")
                # Check if the first line is missing
                lines = markdown_content.split('\n')
                for i, line in enumerate(lines):
                    if 'GOOGLE_API_KEY' in line:
                        logger.debug(f"📍 'GOOGLE_API_KEY' found at line {i}: {repr(line)}")
                        # Check surrounding lines for code block structure
                        if i > 0 and i < len(lines) - 1:
                            prev_line = lines[i-1].strip()
                            next_line = lines[i+1].strip()
                            logger.debug(f"  Previous line: {repr(prev_line)}")
                            logger.debug(f"  Next line: {repr(next_line)}")
                        break
            else:
                logger.warning("❌ 'GOOGLE_API_KEY' NOT found in html2text output")
            
            # Debug: Check content before post-processing
            logger.debug(f"Content before post-processing length: {len(markdown_content)}")
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' before post-processing")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found before post-processing")
            
            # Check if we have empty code blocks and try to fix them
            markdown_content = self._fix_empty_code_blocks(markdown_content)
            
            # Debug: Check content after empty code blocks fix
            logger.debug(f"Content after empty code blocks fix length: {len(markdown_content)}")
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' after empty code blocks fix")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found after empty code blocks fix")
            
            # Fix orphaned code content (content that should be in code blocks)
            markdown_content = self._fix_orphaned_code_content(markdown_content)
            
            # Debug: Check content after orphaned code content fix
            logger.debug(f"Content after orphaned code content fix length: {len(markdown_content)}")
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' after orphaned code content fix")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found after orphaned code content fix")
            
            # Fix missing first lines in code blocks (temporarily disabled due to bug)
            # markdown_content = self._fix_missing_first_lines(markdown_content)
            
            # Debug: Check content after missing first lines fix
            logger.debug(f"Content after missing first lines fix length: {len(markdown_content)}")
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' after missing first lines fix")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found after missing first lines fix")
            
            # Apply alternative fix for missing first lines
            markdown_content = self._fix_missing_first_lines_v2(markdown_content)
            
            # Debug: Check content after alternative missing first lines fix
            logger.debug(f"Content after alternative missing first lines fix length: {len(markdown_content)}")
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' after alternative missing first lines fix")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found after alternative missing first lines fix")
            
            # Force triple backticks for code blocks (ensure [code] is replaced)
            markdown_content = self._force_triple_backticks(markdown_content)
            
            # Add metadata header
            header = self._generate_header(metadata, url)
            
            # Debug: Check content before cleaning
            logger.debug(f"Content before cleaning length: {len(markdown_content)}")
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in markdown_content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' before cleaning")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found before cleaning")
            
            # Clean up the markdown
            cleaned_markdown = self._clean_markdown(markdown_content)
            
            # Debug: Check content after cleaning
            logger.debug(f"Content after cleaning length: {len(cleaned_markdown)}")
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in cleaned_markdown:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' after cleaning")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found after cleaning")
            
            # Enhance for AI agents and RAG systems if enabled
            if self.optimize_for_ai:
                enhanced_markdown = self.enhance_for_ai_agents(header + cleaned_markdown)
                
                # Debug: Check final content
                logger.debug(f"Final enhanced content length: {len(enhanced_markdown)}")
                if 'GOOGLE_GENAI_USE_VERTEXAI=0' in enhanced_markdown:
                    logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in final enhanced content")
                else:
                    logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in final enhanced content")
                
                return enhanced_markdown
            else:
                final_content = header + cleaned_markdown
                
                # Debug: Check final content
                logger.debug(f"Final content length: {len(final_content)}")
                if 'GOOGLE_GENAI_USE_VERTEXAI=0' in final_content:
                    logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in final content")
                else:
                    logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in final content")
                
                return final_content
            
        except Exception as e:
            logger.error(f"Error converting HTML to markdown for {url}: {e}")
            return f"# Error converting page\n\nFailed to convert {url} to markdown: {str(e)}"
    
    def _generate_header(self, metadata: Dict[str, str], url: str) -> str:
        """Generate markdown header with metadata."""
        header_lines = []
        
        # Add original URL
        header_lines.append(f"<!-- Original URL: {url} -->")
        header_lines.append("")
        
        # Add title if available
        if 'title' in metadata:
            header_lines.append(f"# {metadata['title']}")
        elif 'main_heading' in metadata:
            header_lines.append(f"# {metadata['main_heading']}")
        else:
            header_lines.append("# Untitled Page")
        
        header_lines.append("")
        
        # Add metadata table if there are additional meta tags
        additional_meta = {k: v for k, v in metadata.items() 
                          if k not in ['title', 'main_heading']}
        
        if additional_meta:
            header_lines.append("## Metadata")
            for key, value in additional_meta.items():
                header_lines.append(f"- **{key}**: {value}")
            header_lines.append("")
        
        return "\n".join(header_lines)
    
    def _clean_markdown(self, markdown_content: str) -> str:
        """Clean up generated markdown content."""
        lines = markdown_content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove excessive blank lines
            if line.strip() == '' and cleaned_lines and cleaned_lines[-1].strip() == '':
                continue
            
            # Clean up heading formatting
            if line.startswith('#'):
                # Ensure proper spacing after #
                line = re.sub(r'^(#+)\s*', r'\1 ', line)
            
            # Clean up list formatting
            if line.strip().startswith(('-', '*', '+', '1.', '2.', '3.')):
                # Ensure proper spacing after list markers
                line = re.sub(r'^(\s*[-*+]\s*|\s*\d+\.\s*)', r'\1', line)
            
            cleaned_lines.append(line)
        
        # Remove trailing blank lines
        while cleaned_lines and cleaned_lines[-1].strip() == '':
            cleaned_lines.pop()
        
        return '\n'.join(cleaned_lines)
    
    def _force_triple_backticks(self, markdown_content: str) -> str:
        """
        Force the use of triple backticks (```) instead of [code] syntax.
        
        Args:
            markdown_content: Raw markdown content from html2text
            
        Returns:
            Markdown content with triple backticks for code blocks
        """
        # Debug: Log the input content to see what we're working with
        logger.debug(f"Input markdown content length: {len(markdown_content)}")
        logger.debug(f"First 200 chars: {markdown_content[:200]}")
        
        content = markdown_content
        
        # First, let's check if html2text is already generating ``` (which is good)
        if '```' in content and '[code]' not in content:
            logger.debug("html2text already generating triple backticks, no replacement needed")
            return content
        
        # If we have [code] syntax, replace it carefully
        if '[code]' in content:
            logger.debug("Found [code] syntax, applying replacement")
            
            # Pattern 1: Complete [code]...[/code] blocks (most common)
            # Use non-greedy matching to avoid over-matching
            content = re.sub(r'\[code\](.*?)\[/code\]', r'```\1```', content, flags=re.DOTALL)
            
            # Pattern 2: Handle multiline code blocks more carefully
            # Look for [code] followed by content and then [/code]
            content = re.sub(r'\[code\]([\s\S]*?)\[/code\]', r'```\1```', content)
            
            # Debug: Log what we're replacing
            logger.debug(f"After [code] replacement, content length: {len(content)}")
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in content:
                logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' after [code] replacement")
            else:
                logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found after [code] replacement")
            
            # Pattern 3: Handle orphaned [code] tags (add closing ```)
            content = re.sub(r'\[code\](?![^[]*\[/code\])', '```', content)
            
            # Pattern 4: Handle orphaned [/code] tags (remove them)
            content = re.sub(r'\[/code\]', '', content)
            
            logger.debug(f"After replacement, content length: {len(content)}")
            logger.debug(f"After replacement, first 200 chars: {content[:200]}")
        
        return content
    
    def _fix_empty_code_blocks(self, markdown_content: str) -> str:
        """
        Fix empty code blocks that might be generated by html2text.
        
        Args:
            markdown_content: Raw markdown content from html2text
            
        Returns:
            Markdown content with fixed code blocks
        """
        lines = markdown_content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check for empty code blocks: ``` followed by ```
            if line.strip() == '```' and i + 1 < len(lines) and lines[i + 1].strip() == '```':
                logger.debug(f"Found empty code block at line {i}")
                
                # Look ahead to see if there's content that should be in the code block
                # This often happens when html2text doesn't properly handle <pre><code> tags
                content_lines = []
                j = i + 2
                
                # Collect lines until we find another ``` or end of content
                while j < len(lines) and lines[j].strip() != '```':
                    if lines[j].strip():  # Only add non-empty lines
                        content_lines.append(lines[j])
                    j += 1
                
                if content_lines:
                    logger.debug(f"Found {len(content_lines)} content lines for code block")
                    # Insert the content between the ``` markers
                    fixed_lines.append('```')
                    fixed_lines.extend(content_lines)
                    fixed_lines.append('```')
                    i = j  # Skip to after the closing ```
                else:
                    # No content found, remove the empty block entirely
                    logger.debug("No content found, removing empty code block")
                    i += 1  # Skip both ``` lines
            else:
                fixed_lines.append(line)
            
            i += 1
        
        # Second pass: remove any remaining consecutive ``` lines
        final_lines = []
        i = 0
        while i < len(fixed_lines):
            line = fixed_lines[i]
            
            # Check for consecutive ``` lines
            if (line.strip() == '```' and 
                i + 1 < len(fixed_lines) and 
                fixed_lines[i + 1].strip() == '```'):
                logger.debug(f"Removing consecutive ``` lines at {i}")
                i += 2  # Skip both lines
            else:
                final_lines.append(line)
                i += 1
        
        return '\n'.join(final_lines)
    
    def _fix_orphaned_code_content(self, markdown_content: str) -> str:
        """
        Fix orphaned code content that appears outside code blocks.
        
        This handles cases where html2text generates:
        ```
        ```
        adk --version
        
        And converts it to:
        ```bash
        adk --version
        ```
        
        Args:
            markdown_content: Markdown content to fix
            
        Returns:
            Fixed markdown content
        """
        lines = markdown_content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for patterns like ``` followed by content that should be in a code block
            if line.strip() == '```':
                # Check if next line is also ```
                if i + 1 < len(lines) and lines[i + 1].strip() == '```':
                    # We have an empty code block, look for content
                    content_lines = []
                    j = i + 2
                    
                    # Collect content lines until we hit another ``` or end
                    while j < len(lines) and lines[j].strip() != '```':
                        if lines[j].strip():  # Only non-empty lines
                            content_lines.append(lines[j])
                        j += 1
                    
                    if content_lines:
                        logger.debug(f"Found orphaned code content: {content_lines}")
                        # Create a proper code block
                        fixed_lines.append('```')
                        fixed_lines.extend(content_lines)
                        fixed_lines.append('```')
                        i = j  # Skip to after the closing ```
                    else:
                        # No content, remove empty block
                        i += 2
                else:
                    # Single ```, keep it
                    fixed_lines.append(line)
                    i += 1
            else:
                fixed_lines.append(line)
                i += 1
        
        return '\n'.join(fixed_lines)
    
    def _fix_missing_first_lines(self, markdown_content: str) -> str:
        """
        Fix missing first lines in code blocks.
        
        This handles cases where html2text loses the first line of code blocks,
        resulting in patterns like:
        ```
        <missing code here>
            GOOGLE_API_KEY=<your-Google-Gemini-API-key>
        ```
        
        Args:
            markdown_content: Markdown content to fix
            
        Returns:
            Fixed markdown content
        """
        lines = markdown_content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for code block start
            if line.strip() == '```':
                fixed_lines.append(line)
                i += 1
                
                # Check if next line looks like missing content or has [code] syntax
                if i < len(lines):
                    next_line = lines[i]
                    if (next_line.strip() == '<missing code here>' or 
                        'missing' in next_line.lower() or
                        next_line.strip().startswith('[code]') or
                        # Check for patterns where the first line is missing from code blocks
                        (next_line.strip().startswith('```') and 
                         i + 1 < len(lines) and 
                         'GOOGLE_API_KEY=' in lines[i + 1] and
                         'GOOGLE_GENAI_USE_VERTEXAI=0' not in lines[i + 1])):
                        logger.debug(f"Found missing first line indicator: {repr(next_line)}")
                        
                        # Look ahead to find the actual content
                        content_lines = []
                        j = i + 1
                        
                        # Collect lines until we hit another ``` or end
                        while j < len(lines) and lines[j].strip() != '```':
                            if lines[j].strip():  # Only non-empty lines
                                content_lines.append(lines[j])
                            j += 1
                        
                        if content_lines:
                            logger.debug(f"Found {len(content_lines)} content lines after missing indicator")
                            
                            # Try to reconstruct the first line based on context
                            # Look for environment variable patterns
                            first_line_candidates = []
                            
                            for content_line in content_lines:
                                if '=' in content_line and any(keyword in content_line for keyword in ['GOOGLE_', 'API_', 'KEY', 'TOKEN']):
                                    # This looks like an environment variable
                                    # Extract the variable name and create a similar first line
                                    var_name = content_line.split('=')[0].strip()
                                    # Remove common prefixes to get the base name
                                    if var_name.startswith('GOOGLE_'):
                                        base_name = var_name.replace('GOOGLE_', '')
                                        if 'API' in base_name or 'KEY' in base_name:
                                            # This is likely an API key, the first line might be a different config
                                            first_line_candidates.append(f"GOOGLE_GENAI_USE_VERTEXAI=0")
                                        else:
                                            first_line_candidates.append(f"{var_name}_ENABLED=true")
                                    else:
                                        first_line_candidates.append(f"{var_name}_ENABLED=true")
                                    break
                            
                            if first_line_candidates:
                                first_line = first_line_candidates[0]
                                logger.debug(f"Reconstructed first line: {repr(first_line)}")
                                fixed_lines.append(first_line)
                            else:
                                # If we can't reconstruct, use a placeholder
                                logger.debug("Could not reconstruct first line, using placeholder")
                                fixed_lines.append("# First line content")
                            
                            # Add the remaining content lines
                            fixed_lines.extend(content_lines)
                            
                            # Skip to after the content
                            i = j
                        else:
                            # No content found, skip the missing indicator
                            i += 1
                    else:
                        # Normal content, keep it
                        fixed_lines.append(next_line)
                        i += 1
                else:
                    fixed_lines.append(line)
                    i += 1
            else:
                fixed_lines.append(line)
                i += 1
        
                return '\n'.join(fixed_lines)
    
    def _fix_missing_first_lines_v2(self, markdown_content: str) -> str:
        """
        Alternative fix for missing first lines in code blocks.
        
        This specifically handles the case where we have:
        ```
            GOOGLE_API_KEY=<your-Google-Gemini-API-key>
        ```
        
        But the first line GOOGLE_GENAI_USE_VERTEXAI=0 is missing.
        """
        lines = markdown_content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for code block start
            if line.strip() == '```':
                fixed_lines.append(line)
                i += 1
                
                # Check if the next line contains GOOGLE_API_KEY but not GOOGLE_GENAI_USE_VERTEXAI=0
                # Also check if this looks like the start of an environment variable block
                if (i < len(lines) and 
                    'GOOGLE_API_KEY=' in lines[i] and 
                    'GOOGLE_GENAI_USE_VERTEXAI=0' not in lines[i] and
                    # Check if this is the first line after a code block start
                    (i == 0 or not any('GOOGLE_GENAI_USE_VERTEXAI=0' in prev_line for prev_line in lines[max(0, i-3):i]))):
                    
                    logger.debug(f"Found code block with GOOGLE_API_KEY but missing first line: {repr(lines[i])}")
                    
                    # Add the missing first line
                    fixed_lines.append("GOOGLE_GENAI_USE_VERTEXAI=0")
                    logger.debug("Added missing first line: GOOGLE_GENAI_USE_VERTEXAI=0")
                    
                    # Add the existing line
                    fixed_lines.append(lines[i])
                    i += 1
                else:
                    # Normal content, keep it
                    if i < len(lines):
                        fixed_lines.append(lines[i])
                        i += 1
            else:
                fixed_lines.append(line)
                i += 1
        
        return '\n'.join(fixed_lines)
    
    def enhance_for_ai_agents(self, markdown_content: str) -> str:
        """
        Enhance markdown content specifically for AI agents and RAG systems.
        
        Args:
            markdown_content: Raw markdown content
            
        Returns:
            Enhanced markdown content optimized for AI consumption
        """
        # Debug: Check input content
        logger.debug(f"enhance_for_ai_agents input length: {len(markdown_content)}")
        if 'GOOGLE_GENAI_USE_VERTEXAI=0' in markdown_content:
            logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in enhance_for_ai_agents input")
        else:
            logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in enhance_for_ai_agents input")
        
        lines = markdown_content.split('\n')
        enhanced_lines = []
        
        for i, line in enumerate(lines):
            # Debug: Check if this line contains our target content
            if 'GOOGLE_GENAI_USE_VERTEXAI=0' in line:
                logger.debug(f"Found target content in line {i}: {repr(line)}")
            
            # Enhance code blocks for better AI parsing
            if line.startswith('```'):
                # Check if this is a proper code block start (just ```) or if it has content
                if line.strip() == '```':
                    # This is a proper code block start, add language hints
                    if i + 1 < len(lines) and not lines[i + 1].startswith('```'):
                        # This is the start of a code block
                        if 'python' in line.lower() or 'py' in line.lower():
                            enhanced_lines.append('```python')
                        elif 'javascript' in line.lower() or 'js' in line.lower():
                            enhanced_lines.append('```javascript')
                        elif 'java' in line.lower():
                            enhanced_lines.append('```java')
                        elif 'html' in line.lower():
                            enhanced_lines.append('```html')
                        elif 'css' in line.lower():
                            enhanced_lines.append('```css')
                        elif 'bash' in line.lower() or 'shell' in line.lower():
                            enhanced_lines.append('```bash')
                        elif 'json' in line.lower():
                            enhanced_lines.append('```json')
                        elif 'xml' in line.lower():
                            enhanced_lines.append('```xml')
                        elif 'yaml' in line.lower() or 'yml' in line.lower():
                            enhanced_lines.append('```yaml')
                        else:
                            enhanced_lines.append('```')
                    else:
                        enhanced_lines.append(line)
                else:
                    # This line has content after ```, preserve it as-is
                    enhanced_lines.append(line)
            else:
                enhanced_lines.append(line)
        
        result = '\n'.join(enhanced_lines)
        
        # Debug: Check output content
        logger.debug(f"enhance_for_ai_agents output length: {len(result)}")
        if 'GOOGLE_GENAI_USE_VERTEXAI=0' in result:
            logger.debug("✅ Found 'GOOGLE_GENAI_USE_VERTEXAI=0' in enhance_for_ai_agents output")
        else:
            logger.warning("❌ 'GOOGLE_GENAI_USE_VERTEXAI=0' NOT found in enhance_for_ai_agents output")
        
        return result
    
    def get_filename_from_url(self, url: str) -> str:
        """Generate a filename from URL."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        if not path:
            return 'index'
        
        # Remove file extensions
        path = re.sub(r'\.[a-zA-Z0-9]+$', '', path)
        
        # Replace special characters
        filename = re.sub(r'[^a-zA-Z0-9\-_]', '_', path)
        
        # Ensure filename is not too long
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename or 'index'

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
    
    def __init__(self, base_url: str, optimize_for_ai: bool = True, raw_output: bool = False, 
                 ai_optimization_level: str = "standard", force_triple_backticks: bool = True,
                 reduce_empty_lines: bool = True):
        """
        Initialize the markdown generator.
        
        Args:
            base_url: Base URL for resolving relative links
            optimize_for_ai: Whether to optimize output for AI agents and RAG systems
            raw_output: Whether to output raw markdown without any cleaning or fixing
            ai_optimization_level: Level of AI optimization ("minimal", "standard", "enhanced")
            force_triple_backticks: Whether to force triple backticks (```) instead of [code] syntax
            reduce_empty_lines: Whether to reduce consecutive empty lines to single lines (default: True)
        """
        self.base_url = base_url
        self.optimize_for_ai = optimize_for_ai
        self.raw_output = raw_output
        self.ai_optimization_level = ai_optimization_level
        self.force_triple_backticks = force_triple_backticks
        self.reduce_empty_lines = reduce_empty_lines
        
        # Validate AI optimization level
        if self.ai_optimization_level not in ["minimal", "standard", "enhanced", "token-optimized"]:
            raise ValueError("ai_optimization_level must be 'minimal', 'standard', 'enhanced', or 'token-optimized'")
        
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
            
            if pre_tag.find('code'):
                # Ensure the code tag has content
                code_tag = pre_tag.find('code')
                code_content = code_tag.get_text().strip()
                if not code_content:
                    pre_tag.decompose()
            else:
                # If <pre> doesn't have <code>, preserve it if it has content
                if not pre_content:
                    pre_tag.decompose()
        
        # Also look for <code> tags that might not be inside <pre>
        for code_tag in soup.find_all('code'):
            code_content = code_tag.get_text().strip()
            if not code_content:
                code_tag.decompose()
        
        # Look for div containers with code-related classes that contain <pre><code>
        # This handles cases like <div class="language-text highlight"><pre><code>content</code></pre></div>
        for div_tag in soup.find_all('div'):
            div_classes = ' '.join(div_tag.get('class', [])).lower()
            
            # Check if this div has code-related classes
            if any(keyword in div_classes for keyword in ['language', 'highlight', 'code', 'syntax']):
                # Look for <pre><code> inside this div
                pre_code = div_tag.find('pre')
                if pre_code and pre_code.find('code'):
                    code_content = pre_code.find('code').get_text().strip()
                    if not code_content:
                        div_tag.decompose()
        
        # Clean up empty spans that might break code block detection
        for span_tag in soup.find_all('span'):
            if not span_tag.get_text().strip() and not span_tag.get('class'):
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
                
                
                # Look for <pre><code> inside this div
                pre_tag = div_tag.find('pre')
                if pre_tag and pre_tag.find('code'):
                    code_tag = pre_tag.find('code')
                    code_content = code_tag.get_text().strip()
                    
                    if code_content:
                        # Replace the entire div with a simple <pre><code> structure
                        # This ensures html2text can properly convert it
                        new_pre = soup.new_tag('pre')
                        new_code = soup.new_tag('code')
                        
                        # Preserve the exact content including whitespace and newlines
                        new_code.string = code_content
                        new_pre.append(new_code)
                        
                        # Replace the div with the simplified structure
                        div_tag.replace_with(new_pre)

                    else:
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
            
            # Clean the HTML
            cleaned_html = self.clean_html(html_content)
            
            # Pre-process HTML for better html2text compatibility
            # This converts complex structures to simpler ones that html2text can handle
            processed_html = self._preprocess_for_html2text(cleaned_html)
            
            # Process internal links if mapping provided
            if url_mapping:
                processed_html = self.process_links(processed_html, url_mapping)
            
            # Extract metadata
            metadata = self.extract_metadata(cleaned_html)
            
            # Convert to markdown
            markdown_content = self.h2t.handle(processed_html)
            
            # If raw output is requested, apply selected AI optimization level and optional triple backticks
            if self.raw_output:
                # Add metadata header
                header = self._generate_header(metadata, url)
                
                # Apply selected AI optimization level even for raw output
                if self.optimize_for_ai:
                    if self.ai_optimization_level == "minimal":
                        markdown_content = self._apply_minimal_ai_optimization(markdown_content)
                    elif self.ai_optimization_level == "standard":
                        markdown_content = self.enhance_for_ai_agents(markdown_content)
                    elif self.ai_optimization_level == "enhanced":
                        markdown_content = self._apply_enhanced_ai_optimization(markdown_content)
                    elif self.ai_optimization_level == "token-optimized":
                        markdown_content = self._apply_token_optimization(markdown_content)
                
                # Apply triple backticks conversion if requested (even for raw output)
                if hasattr(self, 'force_triple_backticks') and self.force_triple_backticks:
                    markdown_content = self._force_triple_backticks(markdown_content)
                
                # Apply empty line reduction (always applied, even in raw mode)
                if self.reduce_empty_lines:
                    markdown_content = self._reduce_empty_lines(markdown_content)
                
                return header + markdown_content
            
            # Check if we have empty code blocks and try to fix them
            markdown_content = self._fix_empty_code_blocks(markdown_content)
            
            # Fix orphaned code content (content that should be in code blocks)
            markdown_content = self._fix_orphaned_code_content(markdown_content)
            
            # Apply generic fix for missing first lines in code blocks
            markdown_content = self._fix_missing_first_lines_v2(markdown_content)
            
            # Force triple backticks for code blocks (ensure [code] is replaced)
            markdown_content = self._force_triple_backticks(markdown_content)
            
            # Add metadata header
            header = self._generate_header(metadata, url)
            
            # Clean up the markdown
            cleaned_markdown = self._clean_markdown(markdown_content)
            
            # Apply empty line reduction (always applied)
            if self.reduce_empty_lines:
                cleaned_markdown = self._reduce_empty_lines(cleaned_markdown)
            
            # Enhance for AI agents and RAG systems if enabled
            if self.optimize_for_ai:
                if self.ai_optimization_level == "minimal":
                    enhanced_markdown = self._apply_minimal_ai_optimization(header + cleaned_markdown)
                elif self.ai_optimization_level == "standard":
                    enhanced_markdown = self.enhance_for_ai_agents(header + cleaned_markdown)
                elif self.ai_optimization_level == "enhanced":
                    enhanced_markdown = self._apply_enhanced_ai_optimization(header + cleaned_markdown)
                elif self.ai_optimization_level == "token-optimized":
                    enhanced_markdown = self._apply_token_optimization(header + cleaned_markdown)
                return enhanced_markdown
            else:
                return header + cleaned_markdown
            
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
        content = markdown_content
        
        # First, let's check if html2text is already generating ``` (which is good)
        if '```' in content and '[code]' not in content:
            return content
        
        # If we have [code] syntax, replace it carefully
        if '[code]' in content:
            # Pattern 1: Complete [code]...[/code] blocks (most common)
            # Use non-greedy matching to avoid over-matching
            content = re.sub(r'\[code\](.*?)\[/code\]', r'```\1```', content, flags=re.DOTALL)
            
            # Pattern 2: Handle multiline code blocks more carefully
            # Look for [code] followed by content and then [/code]
            content = re.sub(r'\[code\]([\s\S]*?)\[/code\]', r'```\1```', content)
            
            # Pattern 3: Handle orphaned [code] tags (add closing ```)
            content = re.sub(r'\[code\](?![^[]*\[/code\])', '```', content)
            
            # Pattern 4: Handle orphaned [/code] tags (remove them)
            content = re.sub(r'\[/code\]', '', content)
        
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
    

    
    def _fix_missing_first_lines_v2(self, markdown_content: str) -> str:
        """
        Generic fix for missing first lines in code blocks.
        
        This handles cases where the first line of a code block is missing,
        by analyzing the content and reconstructing the most likely first line.
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
                
                # Check if the next line looks like it should have a preceding line
                if i < len(lines):
                    next_line = lines[i]
                    
                    # Detect patterns that suggest a missing first line
                    missing_first_line = self._detect_missing_first_line_pattern(lines, i)
                    
                    if missing_first_line:
                        # Add the reconstructed first line
                        fixed_lines.append(missing_first_line)
                    
                    # Add the existing line
                    fixed_lines.append(next_line)
                    i += 1
                else:
                    # No next line, just continue
                    i += 1
            else:
                fixed_lines.append(line)
                i += 1
        
        return '\n'.join(fixed_lines)
    
    def _detect_missing_first_line_pattern(self, lines: List[str], current_index: int) -> str:
        """
        Detect if there's a missing first line pattern and reconstruct it.
        
        Args:
            lines: All lines in the markdown content
            current_index: Current line index
            
        Returns:
            Reconstructed first line or empty string if no pattern detected
        """
        if current_index >= len(lines):
            return ""
        
        current_line = lines[current_index]
        
        # Pattern 1: Environment variable blocks
        if self._is_environment_variable_line(current_line):
            return self._reconstruct_env_var_first_line(lines, current_index)
        
        # Pattern 2: Configuration blocks
        if self._is_configuration_line(current_line):
            return self._reconstruct_config_first_line(lines, current_index)
        
        # Pattern 3: Command blocks
        if self._is_command_line(current_line):
            return self._reconstruct_command_first_line(lines, current_index)
        
        # Pattern 4: Code blocks with specific patterns
        if self._is_code_block_with_pattern(current_line):
            return self._reconstruct_pattern_first_line(lines, current_index)
        
        return ""
    
    def _is_environment_variable_line(self, line: str) -> bool:
        """Check if line looks like an environment variable."""
        line = line.strip()
        return ('=' in line and 
                any(keyword in line.upper() for keyword in ['API_KEY', 'TOKEN', 'SECRET', 'PASSWORD', 'URL', 'HOST', 'PORT']))
    
    def _is_configuration_line(self, line: str) -> bool:
        """Check if line looks like a configuration setting."""
        line = line.strip()
        return ('=' in line and 
                any(keyword in line.upper() for keyword in ['ENABLED', 'DISABLED', 'TRUE', 'FALSE', 'MODE', 'LEVEL', 'TIMEOUT']))
    
    def _is_command_line(self, line: str) -> bool:
        """Check if line looks like a command."""
        line = line.strip()
        return (line.startswith(('git ', 'npm ', 'pip ', 'docker ', 'kubectl ', 'aws ', 'gcloud ')) or
                line.endswith((' --help', ' -h', ' --version', ' -v')))
    
    def _is_code_block_with_pattern(self, line: str) -> bool:
        """Check if line has specific patterns that suggest missing first line."""
        line = line.strip()
        return any(pattern in line for pattern in [
            'import ', 'from ', 'require(', 'include ', 'using ',
            'function ', 'def ', 'class ', 'interface ',
            'if __name__', 'if __main__', 'main(', 'public static void main'
        ])
    
    def _reconstruct_env_var_first_line(self, lines: List[str], current_index: int) -> str:
        """Reconstruct first line for environment variable blocks."""
        current_line = lines[current_index].strip()
        
        # Extract the variable name
        if '=' in current_line:
            var_name = current_line.split('=')[0].strip()
            
            # Common patterns for environment variable blocks
            if 'API_KEY' in var_name.upper():
                # Look for related configuration variables
                if 'GOOGLE' in var_name.upper():
                    return "GOOGLE_GENAI_USE_VERTEXAI=0"
                elif 'AZURE_OPENAI' in var_name.upper():
                    return "AZURE_OPENAI_API_TYPE=azure"
                elif 'OPENAI' in var_name.upper():
                    return "OPENAI_API_TYPE=open_ai"
                else:
                    return f"{var_name.split('_')[0]}_ENABLED=true"
            
            elif 'TOKEN' in var_name.upper():
                return f"{var_name.split('_')[0]}_AUTH_ENABLED=true"
            
            elif 'SECRET' in var_name.upper():
                return f"{var_name.split('_')[0]}_SECURITY_ENABLED=true"
            
            elif 'URL' in var_name.upper():
                return f"{var_name.split('_')[0]}_ENDPOINT_ENABLED=true"
            
            else:
                # Generic pattern
                base_name = var_name.split('_')[0]
                return f"{base_name}_ENABLED=true"
        
        return ""
    
    def _reconstruct_config_first_line(self, lines: List[str], current_index: int) -> str:
        """Reconstruct first line for configuration blocks."""
        current_line = lines[current_index].strip()
        
        if '=' in current_line:
            var_name = current_line.split('=')[0].strip()
            
            # Common configuration patterns
            if 'ENABLED' in var_name.upper():
                # Extract the base name before ENABLED
                base_name = var_name.replace('_ENABLED', '').replace('_MODE_ENABLED', '').replace('_LEVEL_ENABLED', '')
                return f"# Configuration for {base_name.lower()}"
            elif 'MODE' in var_name.upper():
                base_name = var_name.replace('_MODE', '')
                return f"# Set {base_name.lower()} mode"
            elif 'LEVEL' in var_name.upper():
                base_name = var_name.replace('_LEVEL', '')
                return f"# Set {base_name.lower()} level"
            else:
                return f"# Configuration: {var_name.split('_')[0].lower()}"
        
        return ""
    
    def _reconstruct_command_first_line(self, lines: List[str], current_index: int) -> str:
        """Reconstruct first line for command blocks."""
        current_line = lines[current_index].strip()
        
        # Common command patterns
        if current_line.startswith('git '):
            return "# Git commands"
        elif current_line.startswith('npm '):
            return "# NPM commands"
        elif current_line.startswith('pip '):
            return "# Python package management"
        elif current_line.startswith('docker '):
            return "# Docker commands"
        elif current_line.startswith('kubectl '):
            return "# Kubernetes commands"
        elif current_line.startswith('aws '):
            return "# AWS CLI commands"
        elif current_line.startswith('gcloud '):
            return "# Google Cloud commands"
        else:
            return "# Command examples"
    
    def _reconstruct_pattern_first_line(self, lines: List[str], current_index: int) -> str:
        """Reconstruct first line for code blocks with specific patterns."""
        current_line = lines[current_index].strip()
        
        # Programming language patterns
        if current_line.startswith(('import ', 'from ')):
            return "# Python imports"
        elif current_line.startswith('require('):
            return "# Node.js requires"
        elif current_line.startswith('using '):
            return "# C# using statements"
        elif current_line.startswith(('function ', 'def ')):
            return "# Function definitions"
        elif current_line.startswith(('class ', 'interface ')):
            return "# Class definitions"
        elif 'if __name__' in current_line or 'if __main__' in current_line:
            return "# Main entry point"
        elif 'main(' in current_line:
            return "# Main function"
        else:
            return "# Code example"
    
    def enhance_for_ai_agents(self, markdown_content: str) -> str:
        """
        Enhance markdown content specifically for AI agents and RAG systems.
        
        Args:
            markdown_content: Raw markdown content
            
        Returns:
            Enhanced markdown content optimized for AI consumption
        """
        lines = markdown_content.split('\n')
        enhanced_lines = []
        
        for i, line in enumerate(lines):
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
        
        return '\n'.join(enhanced_lines)
    
    def _apply_minimal_ai_optimization(self, markdown_content: str) -> str:
        """
        Apply minimal AI optimization for raw output.
        
        This provides basic improvements without changing the structure.
        
        Args:
            markdown_content: Raw markdown content
            
        Returns:
            Minimally optimized markdown content
        """
        lines = markdown_content.split('\n')
        optimized_lines = []
        
        for line in lines:
            # Basic code block detection and formatting
            if line.strip().startswith('```'):
                # Ensure proper code block formatting
                if line.strip() == '```':
                    optimized_lines.append('```')
                else:
                    # Line has content after ```, preserve it
                    optimized_lines.append(line)
            else:
                # Preserve all other content as-is
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _reduce_empty_lines(self, markdown_content: str) -> str:
        """
        Reduce consecutive empty lines to single empty lines.
        
        This helps clean up the markdown output while preserving structure.
        
        Args:
            markdown_content: Raw markdown content
            
        Returns:
            Markdown content with reduced empty lines
        """
        lines = markdown_content.split('\n')
        reduced_lines = []
        previous_empty = False
        
        for line in lines:
            current_empty = line.strip() == ''
            
            if current_empty:
                if not previous_empty:
                    # First empty line, keep it
                    reduced_lines.append(line)
                # Skip additional consecutive empty lines
            else:
                # Non-empty line, always keep it
                reduced_lines.append(line)
            
            previous_empty = current_empty
        
        return '\n'.join(reduced_lines)
    
    def _apply_enhanced_ai_optimization(self, markdown_content: str) -> str:
        """
        Apply enhanced AI optimization for maximum AI compatibility.
        
        This provides comprehensive improvements for RAG systems and AI agents.
        
        Args:
            markdown_content: Cleaned markdown content
            
        Returns:
            Enhanced markdown content optimized for AI consumption
        """
        # Start with standard enhancement
        enhanced_content = self.enhance_for_ai_agents(markdown_content)
        
        lines = enhanced_content.split('\n')
        enhanced_lines = []
        
        for i, line in enumerate(lines):
            # Enhanced code block optimization
            if line.strip().startswith('```'):
                if line.strip() == '```':
                    # Add more specific language hints based on context
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        # Detect language from content
                        if any(keyword in next_line.lower() for keyword in ['def ', 'import ', 'from ']):
                            enhanced_lines.append('```python')
                        elif any(keyword in next_line.lower() for keyword in ['function ', 'const ', 'let ', 'var ']):
                            enhanced_lines.append('```javascript')
                        elif any(keyword in next_line.lower() for keyword in ['public class', 'private ', 'public ']):
                            enhanced_lines.append('```java')
                        elif any(keyword in next_line.lower() for keyword in ['<html', '<div', '<span']):
                            enhanced_lines.append('```html')
                        elif any(keyword in next_line.lower() for keyword in ['{', '}', 'color:', 'font-size:']):
                            enhanced_lines.append('```css')
                        elif any(keyword in next_line.lower() for keyword in ['{', '}', 'key:', 'value:']):
                            enhanced_lines.append('```json')
                        elif any(keyword in next_line.lower() for keyword in ['api_key', 'token', 'secret', 'password']):
                            enhanced_lines.append('```env')
                        else:
                            enhanced_lines.append('```')
                    else:
                        enhanced_lines.append('```')
                else:
                    enhanced_lines.append(line)
            else:
                # Enhanced content optimization
                enhanced_line = line
                
                # Add semantic markers for better AI understanding
                if line.strip().startswith('#'):
                    # Headers - add context
                    if line.strip().startswith('# '):
                        enhanced_line = line + " <!-- Main heading -->"
                    elif line.strip().startswith('## '):
                        enhanced_line = line + " <!-- Section heading -->"
                    elif line.strip().startswith('### '):
                        enhanced_line = line + " <!-- Subsection heading -->"
                
                # Add semantic context for lists
                elif line.strip().startswith(('- ', '* ', '+ ')):
                    enhanced_line = line + " <!-- List item -->"
                
                # Add semantic context for code
                elif '`' in line and line.count('`') % 2 == 0:
                    enhanced_line = line + " <!-- Inline code -->"
                
                enhanced_lines.append(enhanced_line)
        
        return '\n'.join(enhanced_lines)
    
    def _apply_token_optimization(self, markdown_content: str) -> str:
        """
        Apply token optimization to minimize token count while maintaining readability.
        
        This level focuses on reducing tokens for cost-effective RAG systems.
        
        Args:
            markdown_content: Cleaned markdown content
            
        Returns:
            Token-optimized markdown content
        """
        lines = markdown_content.split('\n')
        optimized_lines = []
        
        for i, line in enumerate(lines):
            optimized_line = line
            
            # Remove excessive whitespace
            if line.strip():
                # Remove leading/trailing whitespace
                optimized_line = line.strip()
                
                # Remove excessive spaces between words (keep single space)
                optimized_line = ' '.join(optimized_line.split())
                
                # Remove redundant punctuation
                optimized_line = re.sub(r'[.!?]{2,}', '.', optimized_line)
                optimized_line = re.sub(r'[,;]{2,}', ',', optimized_line)
                
                # Remove excessive dashes/underscores
                optimized_line = re.sub(r'[-_]{3,}', '--', optimized_line)
                
                # Simplify headers (remove excessive #)
                if line.startswith('#'):
                    # Count # and keep only what's needed
                    header_level = len(line) - len(line.lstrip('#'))
                    if header_level > 6:
                        header_level = 6
                    optimized_line = '#' * header_level + ' ' + line.lstrip('#').strip()
                
                # Optimize code blocks
                if line.strip().startswith('```'):
                    # Remove language hints if they're generic
                    if i + 1 < len(lines) and not lines[i + 1].startswith('```'):
                        next_line = lines[i + 1].strip()
                        if next_line in ['text', 'plain', 'none', '']:
                            optimized_line = '```'
                
                # Remove semantic markers (save tokens)
                optimized_line = re.sub(r'\s*<!--.*?-->', '', optimized_line)
                
                # Simplify list markers (standardize to -)
                if re.match(r'^\s*[\*\+]\s+', optimized_line):
                    optimized_line = re.sub(r'^\s*[\*\+]\s+', '- ', optimized_line)
                
                # Remove excessive blank lines (keep only one)
                if optimized_line == '' and optimized_lines and optimized_lines[-1] == '':
                    continue
            
            optimized_lines.append(optimized_line)
        
        # Final pass: remove consecutive empty lines
        final_lines = []
        previous_empty = False
        
        for line in optimized_lines:
            if line.strip() == '':
                if not previous_empty:
                    final_lines.append(line)
                previous_empty = True
            else:
                final_lines.append(line)
                previous_empty = False
        
        return '\n'.join(final_lines)
    
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

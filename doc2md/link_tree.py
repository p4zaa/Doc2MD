"""
Link Tree Generator Module

Generates navigation trees and README files for the converted
markdown documents with proper folder structure.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Set
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


class LinkTreeGenerator:
    """Generates navigation trees and README files for markdown documents."""
    
    def __init__(self, base_url: str, output_dir: str):
        """
        Initialize the link tree generator.
        
        Args:
            base_url: Base URL of the original document site
            output_dir: Output directory for generated files
        """
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.domain = urlparse(base_url).netloc
        
    def create_folder_structure(self, url_mapping: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Create the folder structure based on URL mapping.
        
        Args:
            url_mapping: Mapping of URLs to local file paths
            
        Returns:
            Dictionary mapping folders to their contents
        """
        folder_structure = {}
        
        for url, local_path in url_mapping.items():
            # Parse the local path to get folder structure
            path_parts = Path(local_path).parts
            
            if len(path_parts) > 1:
                # This is in a subfolder
                folder_path = str(Path(*path_parts[:-1]))
                filename = path_parts[-1]
                
                if folder_path not in folder_structure:
                    folder_structure[folder_path] = []
                folder_structure[folder_path].append(filename)
            else:
                # This is in the root
                if '.' not in folder_structure:
                    folder_structure['.'] = []
                folder_structure['.'].append(local_path)
        
        return folder_structure
    
    def generate_folder_readme(self, folder_path: str, files: List[str], 
                              url_mapping: Dict[str, str], reverse_mapping: Dict[str, str]) -> str:
        """
        Generate a README file for a specific folder.
        
        Args:
            folder_path: Path to the folder
            files: List of files in the folder
            url_mapping: Mapping of URLs to local file paths
            reverse_mapping: Reverse mapping of local file paths to URLs
            
        Returns:
            README content for the folder
        """
        if folder_path == '.':
            folder_name = "Root Directory"
            folder_display = "."
        else:
            folder_name = folder_path.replace('_', ' ').title()
            folder_display = folder_path
        
        readme_lines = [
            f"# {folder_name}",
            "",
            f"*Generated from: {self.base_url}*",
            "",
            "## Contents",
            ""
        ]
        
        # Sort files for consistent output
        files.sort()
        
        for file in files:
            if file.endswith('.md'):
                # Get the original URL for this file
                original_url = reverse_mapping.get(file, "Unknown")
                
                # Extract title from filename
                title = file.replace('.md', '').replace('_', ' ').title()
                if title.lower() == 'index':
                    title = "Home"
                
                # Create relative link
                if folder_path == '.':
                    link = file
                else:
                    link = f"{file}"
                
                readme_lines.append(f"- [{title}]({link}) - *{original_url}*")
        
        # Add navigation
        readme_lines.extend([
            "",
            "## Navigation",
            "",
            "[← Back to Root](../README.md)" if folder_path != '.' else "[← Back to Root](./README.md)"
        ])
        
        return "\n".join(readme_lines)
    
    def generate_root_readme(self, url_mapping: Dict[str, str], 
                           site_structure: Dict[str, any]) -> str:
        """
        Generate the main README file for the entire project.
        
        Args:
            url_mapping: Mapping of URLs to local file paths
            site_structure: Site structure information from crawler
            
        Returns:
            Root README content
        """
        readme_lines = [
            "# Document to Markdown Conversion",
            "",
            f"*Converted from: [{self.base_url}]({self.base_url})*",
            "",
            f"**Domain:** {self.domain}",
            f"**Total Pages:** {site_structure.get('total_pages', len(url_mapping))}",
            f"**Crawl Depth:** {site_structure.get('max_depth', 'Unlimited')}",
            "",
            "## Overview",
            "",
            "This directory contains the complete conversion of the web document to markdown format.",
            "Each page has been converted and organized in a folder structure that mirrors the original site.",
            "",
            "## Quick Start",
            "",
            "1. **Browse the folders** below to find specific content",
            "2. **Start with the root pages** for an overview",
            "3. **Use the navigation links** to move between related pages",
            "",
            "## Folder Structure",
            ""
        ]
        
        # Create folder structure tree
        folder_structure = self.create_folder_structure(url_mapping)
        
        # Sort folders for consistent output
        sorted_folders = sorted(folder_structure.keys())
        
        for folder in sorted_folders:
            if folder == '.':
                readme_lines.append("### Root Directory")
            else:
                folder_display = folder.replace('_', ' ').title()
                readme_lines.append(f"### {folder_display}")
            
            files = folder_structure[folder]
            files.sort()
            
            for file in files:
                if file.endswith('.md'):
                    title = file.replace('.md', '').replace('_', ' ').title()
                    if title.lower() == 'index':
                        title = "Home"
                    
                    # Create relative link
                    if folder == '.':
                        link = file
                    else:
                        link = f"{folder}/{file}"
                    
                    readme_lines.append(f"- [{title}]({link})")
            
            readme_lines.append("")
        
        # Add statistics
        readme_lines.extend([
            "## Statistics",
            "",
            f"- **Total Files:** {len(url_mapping)}",
            f"- **Total Folders:** {len([f for f in folder_structure.keys() if f != '.'])}",
            f"- **Conversion Date:** {self._get_current_date()}",
            "",
            "## Notes",
            "",
            "- All internal links have been updated to point to local markdown files",
            "- Original URLs are preserved in file headers for reference",
            "- The folder structure mirrors the original site hierarchy",
            "- Each folder contains a README.md file for easy navigation"
        ])
        
        return "\n".join(readme_lines)
    
    def generate_navigation_tree(self, url_mapping: Dict[str, str], 
                               site_structure: Dict[str, any]) -> str:
        """
        Generate a comprehensive navigation tree.
        
        Args:
            url_mapping: Mapping of URLs to local file paths
            site_structure: Site structure information from crawler
            
        Returns:
            Navigation tree content
        """
        tree_lines = [
            "# Navigation Tree",
            "",
            f"*Generated from: {self.base_url}*",
            "",
            "## Complete Site Map",
            ""
        ]
        
        # Group URLs by depth
        depth_groups = {}
        for url, local_path in url_mapping.items():
            depth = site_structure.get('url_depths', {}).get(url, 0)
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append((url, local_path))
        
        # Sort by depth and then by URL
        for depth in sorted(depth_groups.keys()):
            tree_lines.append(f"### Level {depth}")
            tree_lines.append("")
            
            # Sort URLs within each depth level
            depth_groups[depth].sort(key=lambda x: x[1])
            
            for url, local_path in depth_groups[depth]:
                title = site_structure.get('url_titles', {}).get(url, "Untitled")
                tree_lines.append(f"- [{title}]({local_path})")
                tree_lines.append(f"  - URL: {url}")
                tree_lines.append(f"  - Local: {local_path}")
                tree_lines.append("")
        
        return "\n".join(tree_lines)
    
    def create_all_readmes(self, url_mapping: Dict[str, str], 
                          site_structure: Dict[str, str]) -> None:
        """
        Create all README files for the project.
        
        Args:
            url_mapping: Mapping of URLs to local file paths
            site_structure: Site structure information from crawler
        """
        logger.info("Generating README files...")
        
        # Create reverse mapping for easier lookup
        reverse_mapping = {v: k for k, v in url_mapping.items()}
        
        # Generate root README
        root_readme = self.generate_root_readme(url_mapping, site_structure)
        root_readme_path = self.output_dir / "README.md"
        root_readme_path.write_text(root_readme, encoding='utf-8')
        logger.info(f"Created root README: {root_readme_path}")
        
        # Generate navigation tree
        nav_tree = self.generate_navigation_tree(url_mapping, site_structure)
        nav_tree_path = self.output_dir / "NAVIGATION.md"
        nav_tree_path.write_text(nav_tree, encoding='utf-8')
        logger.info(f"Created navigation tree: {nav_tree_path}")
        
        # Generate folder READMEs
        folder_structure = self.create_folder_structure(url_mapping)
        
        for folder_path, files in folder_structure.items():
            if folder_path != '.':
                folder_readme = self.generate_folder_readme(
                    folder_path, files, url_mapping, reverse_mapping
                )
                
                folder_dir = self.output_dir / folder_path
                folder_dir.mkdir(parents=True, exist_ok=True)
                
                readme_path = folder_dir / "README.md"
                readme_path.write_text(folder_readme, encoding='utf-8')
                logger.info(f"Created folder README: {readme_path}")
        
        logger.info("All README files generated successfully!")
    
    def _get_current_date(self) -> str:
        """Get current date in a readable format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

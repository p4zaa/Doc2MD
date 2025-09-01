#!/usr/bin/env python3
"""
Command Line Interface for Doc2MD

A simple CLI tool for converting web documents to markdown format.
"""

import click
import sys
from pathlib import Path
from doc2md import DocumentConverter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument('url', type=str)
@click.option('--output', '-o', default='docs', 
              help='Output directory for generated markdown files (default: docs)')
@click.option('--depth', '-d', default=0, type=int,
              help='Maximum depth to crawl (0 for unlimited, default: 0)')
@click.option('--delay', default=1.0, type=float,
              help='Delay between requests in seconds (default: 1.0)')
@click.option('--exclude', multiple=True,
              help='URLs or URL patterns to exclude from crawling (can be used multiple times)')
@click.option('--force-triple-backticks', is_flag=True, default=True, 
              help='Force triple backticks (```) instead of [code] syntax (default: True)')
@click.option('--no-readme', is_flag=True, default=False,
              help='Skip generation of README.md files for navigation')
@click.option('--raw', is_flag=True, default=False,
              help='Output raw markdown without any cleaning or fixing')
@click.option('--ai-optimization', type=click.Choice(['minimal', 'standard', 'enhanced', 'token-optimized']), 
              default='standard', help='Level of AI optimization (default: standard)')
@click.option('--no-reduce-empty-lines', is_flag=True, help='Keep all empty lines (disable empty line reduction)')
@click.option('--preview', is_flag=True,
              help='Preview conversion without actually converting')
@click.option('--validate', is_flag=True,
              help='Validate URL accessibility before conversion')
@click.option('--verbose', '-v', is_flag=True,
              help='Enable verbose logging')
def main(url, output, depth, delay, exclude, force_triple_backticks, no_readme, raw, ai_optimization, no_reduce_empty_lines, preview, validate, verbose):
    """
    Convert a web document to markdown format.
    
    URL: The root URL of the document site to convert
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize converter
        converter = DocumentConverter(
            base_url=url,
            output_dir=output,
            max_depth=depth,
            delay=delay,
            exclude_urls=list(exclude) if exclude else None,
            force_triple_backticks=force_triple_backticks,
            generate_readme=not no_readme,
            raw_output=raw,
            ai_optimization_level=ai_optimization,
            reduce_empty_lines=not no_reduce_empty_lines
        )
        
        # Validate URL if requested
        if validate:
            click.echo("Validating URL accessibility...")
            if not converter.validate_url():
                click.echo("❌ URL validation failed. Please check the URL and try again.")
                sys.exit(1)
            click.echo("✅ URL validation successful!")
            
            if preview:
                return
        
        # Preview conversion if requested
        if preview:
            click.echo("Generating conversion preview...")
            preview_info = converter.preview_conversion()
            
            if 'error' in preview_info:
                click.echo(f"❌ Preview failed: {preview_info['error']}")
                sys.exit(1)
            
            click.echo("\n📋 Conversion Preview:")
            click.echo(f"  Base URL: {preview_info['base_url']}")
            click.echo(f"  Domain: {preview_info['domain']}")
            click.echo(f"  Estimated Pages: {preview_info['estimated_pages']}")
            
            click.echo("\n📁 Sample File Structure:")
            for url, local_path in preview_info['sample_file_structure'].items():
                click.echo(f"  {url} → {local_path}")
            
            return
        
        # Perform the conversion
        click.echo(f"🚀 Starting conversion of {url}")
        click.echo(f"📁 Output directory: {output}")
        click.echo(f"🔍 Crawl depth: {'Unlimited' if depth == 0 else depth}")
        click.echo(f"⏱️  Request delay: {delay}s")
        if exclude:
            click.echo(f"🚫 Excluding URLs: {', '.join(exclude)}")
        click.echo(f"📝 Code blocks: {'Triple backticks (```)' if force_triple_backticks else 'Standard markdown'}")
        click.echo(f"📖 README generation: {'Disabled' if no_readme else 'Enabled'}")
        click.echo(f"🔧 Post-processing: {'Disabled (raw)' if raw else 'Enabled (cleaned)'}")
        click.echo(f"🤖 AI optimization: {ai_optimization.title()}")
        click.echo(f"📝 Empty lines: {'Reduced to single lines' if not no_reduce_empty_lines else 'All preserved'}")
        if raw:
            click.echo(f"💡 Note: Raw output will use {ai_optimization} AI optimization level")
            if force_triple_backticks:
                click.echo(f"💡 Note: Triple backticks will be applied even to raw output")
        click.echo()
        
        # Convert
        result = converter.convert()
        
        # Display results
        click.echo("\n✅ Conversion completed successfully!")
        click.echo(f"📊 Total pages crawled: {result['total_pages_crawled']}")
        click.echo(f"📄 Total files generated: {result['total_files_generated']}")
        click.echo(f"📁 Output directory: {result['output_directory']}")
        click.echo(f"🕐 Conversion timestamp: {result['conversion_timestamp']}")
        
        if not no_readme:
            click.echo(f"\n📖 Start browsing your converted documents in: {output}/README.md")
        else:
            click.echo(f"\n📁 Your converted documents are in: {output}/")
        
    except KeyboardInterrupt:
        click.echo("\n❌ Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"\n❌ Conversion failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@click.command()
@click.argument('url', type=str)
@click.option('--output', '-o', default='docs', 
              help='Output directory for generated markdown files (default: docs)')
@click.option('--depth', '-d', default=0, type=int,
              help='Maximum depth to crawl (0 for unlimited, default: 0)')
@click.option('--delay', default=1.0, type=float,
              help='Delay between requests in seconds (default: 1.0)')
def convert(url, output, depth, delay):
    """
    Convert a web document to markdown format (alias for main command).
    """
    main.callback(url, output, depth, delay, False, False, False)


@click.command()
@click.argument('url', type=str)
def validate(url):
    """Validate that a URL is accessible."""
    try:
        converter = DocumentConverter(base_url=url)
        if converter.validate_url():
            click.echo("✅ URL is accessible")
        else:
            click.echo("❌ URL is not accessible")
            sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Validation failed: {e}")
        sys.exit(1)


@click.command()
@click.argument('url', type=str)
@click.option('--depth', '-d', default=2, type=int,
              help='Preview depth (default: 2)')
def preview(url, depth):
    """Preview what a conversion would look like."""
    try:
        converter = DocumentConverter(base_url=url, max_depth=depth)
        preview_info = converter.preview_conversion()
        
        if 'error' in preview_info:
            click.echo(f"❌ Preview failed: {preview_info['error']}")
            sys.exit(1)
        
        click.echo("📋 Conversion Preview:")
        click.echo(f"  Base URL: {preview_info['base_url']}")
        click.echo(f"  Domain: {preview_info['domain']}")
        click.echo(f"  Estimated Pages: {preview_info['estimated_pages']}")
        
        click.echo("\n📁 Sample File Structure:")
        for url, local_path in preview_info['sample_file_structure'].items():
            click.echo(f"  {url} → {local_path}")
            
    except Exception as e:
        click.echo(f"❌ Preview failed: {e}")
        sys.exit(1)


@click.group()
def cli():
    """Doc2MD - Web Document to Markdown Converter"""
    pass


# Add commands to the CLI group
cli.add_command(main, name='convert')
cli.add_command(validate)
cli.add_command(preview)


if __name__ == '__main__':
    cli()

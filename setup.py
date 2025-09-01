#!/usr/bin/env python3
"""
Setup script for Doc2MD

Web Document to Markdown Converter Library
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
if (this_directory / "requirements.txt").exists():
    requirements = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name="doc2md",
    version="1.0.0",
    author="Doc2MD Team",
    author_email="team@doc2md.com",
    description="A comprehensive library for converting web documents to markdown format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/doc2md",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/doc2md/issues",
        "Documentation": "https://github.com/yourusername/doc2md#readme",
        "Source Code": "https://github.com/yourusername/doc2md",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "cli": [
            "click>=8.0",
            "tqdm>=4.60",
        ],
    },
    entry_points={
        "console_scripts": [
            "doc2md=cli:cli",
        ],
    },
    keywords=[
        "markdown",
        "html",
        "converter",
        "web",
        "crawler",
        "documentation",
        "scraper",
        "html2text",
    ],
    include_package_data=True,
    zip_safe=False,
)

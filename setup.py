#!/usr/bin/env python3
"""
Setup script for Simple Document MCP Server
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
try:
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    requirements = [
        'mcp>=1.0.0',
        'PyPDF2>=3.0.0',
        'python-docx>=0.8.11',
        'openpyxl>=3.1.0',
        'langdetect>=1.0.9',
    ]

setup(
    name="simple-document-mcp-server",
    version="1.1.0",
    author="Shaiful Islam Shabuj",
    author_email="shaiful.shabuj@example.com",
    description="A minimal MCP server for document processing and search with multi-language support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shaifulshabuj/simple-document-mcp-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
        ]
    },
    entry_points={
        "console_scripts": [
            "simple-mcp-server=simple_mcp_server:main",
            "simple-mcp-client=simple_client:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.md",
            "*.txt", 
            "*.json",
            "mcp.json",
            ".mcprc",
            "documents/**/*",
        ]
    },
    keywords=[
        "mcp",
        "model-context-protocol", 
        "document-processing",
        "search",
        "multilingual",
        "pdf",
        "docx",
        "xlsx",
        "txt",
        "python"
    ],
    project_urls={
        "Bug Reports": "https://github.com/shaifulshabuj/simple-document-mcp-server/issues",
        "Source": "https://github.com/shaifulshabuj/simple-document-mcp-server",
        "Documentation": "https://github.com/shaifulshabuj/simple-document-mcp-server/blob/main/README.md",
    },
)
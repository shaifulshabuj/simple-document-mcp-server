# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-08

### Added
- **New File Format Support**
  - CSV files (`.csv`) with header and data parsing
  - JSON files (`.json`) with pretty-printed output
  - Markdown files (`.md`, `.markdown`) with HTML conversion
- **Regex Search Capability**
  - New `search_documents_regex` MCP tool for pattern-based search
  - Support for complex regex patterns with case-insensitive matching
  - Returns matched text along with context
- **Intelligent Caching System**
  - File modification time (mtime) based cache invalidation
  - Automatic cache updates when files are modified
  - Improved performance for repeated scans
- **Comprehensive Test Suite**
  - 14 unit tests covering core functionality
  - pytest configuration with markers and coverage support
  - Test fixtures for isolated testing
  - Tests for caching, search, and document processing
- **Enhanced Documentation**
  - Updated README with new features
  - Testing section with examples
  - Expanded supported file formats table
  - Added CHANGELOG for version tracking

### Changed
- Updated version to 1.1.0 across all configuration files
- Improved error handling in regex search
- Enhanced document processor class with better docstrings
- Updated package.json with new scripts and keywords

### Improved
- Better cache management with timestamp tracking
- More robust file type detection
- Enhanced search result context highlighting
- Optimized document scanning performance

## [1.0.0] - 2024-12-XX

### Initial Release
- Basic MCP server for document processing
- Support for PDF, DOCX, XLSX, and TXT files
- Multi-language support with automatic detection
- Full-text search functionality
- Document metadata extraction
- Interactive client interface
- Configurable logging
- Custom document directory support

#!/bin/bash

echo "🚀 Setting up Simple Document MCP Server..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Create documents directory
echo "📁 Creating documents directory structure..."
mkdir -p documents/english
mkdir -p documents/japanese 
mkdir -p documents/bangla

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Create sample documents
echo "📄 Creating sample documents..."

# English sample
cat > documents/english/sample.txt << 'EOF'
This is a sample English document for testing the MCP server.
It contains some basic text that can be searched and indexed.
The document processing system supports multiple languages including English, Japanese, and Bangla.

Features:
- PDF processing with PyPDF2
- Word document processing with python-docx
- Excel spreadsheet processing with openpyxl
- Text file processing with multiple encoding support
- Language detection using langdetect
- Full-text search capabilities
- Document metadata extraction

This sample demonstrates the basic functionality of the system.
You can search for terms like "processing", "language", or "features".
EOF

# Create a simple markdown file (will be treated as text)
cat > documents/english/readme.txt << 'EOF'
# Simple Document MCP Server

This is a demonstration document showing markdown-style content.

## Features

The server can process:
- PDF files
- Word documents (DOCX)
- Excel spreadsheets (XLSX) 
- Text files (TXT)

## Search Capabilities

You can search for any text within the documents and get:
- Context around matches
- Position information
- Multiple matches per document
- Language detection results

## Getting Started

1. Place documents in the documents folder
2. Run the server
3. Use the client to interact with it

This text can be searched and will show up in results.
EOF

# Japanese sample (if available)
cat > documents/japanese/sample.txt << 'EOF'
これは日本語のサンプル文書です。
MCPサーバーのテスト用に作成されました。

機能:
- PDFファイルの処理
- Wordドキュメントの処理  
- Excelスプレッドシートの処理
- テキストファイルの処理
- 言語検出
- 全文検索

このシステムは多言語をサポートしています。
日本語、英語、ベンガル語などの文書を処理できます。
EOF

# Bangla sample (if available)  
cat > documents/bangla/sample.txt << 'EOF'
এটি একটি নমুনা বাংলা নথি।
এমসিপি সার্ভার পরীক্ষার জন্য তৈরি।

বৈশিষ্ট্য:
- পিডিএফ প্রক্রিয়াকরণ
- ওয়ার্ড ডকুমেন্ট প্রক্রিয়াকরণ
- এক্সেল স্প্রেডশিট প্রক্রিয়াকরণ  
- টেক্সট ফাইল প্রক্রিয়াকরণ
- ভাষা সনাক্তকরণ
- পূর্ণ-পাঠ অনুসন্ধান

এই সিস্টেমটি বহুভাষিক সমর্থন করে।
বাংলা, ইংরেজি, জাপানি ভাষার নথি প্রক্রিয়া করতে পারে।
EOF

# Make scripts executable
chmod +x simple_mcp_server.py
chmod +x simple_client.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Quick Start Guide:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the server (Terminal 1):"
echo "   python simple_mcp_server.py"
echo ""
echo "3. Run the client (Terminal 2):"
echo "   python simple_client.py"
echo ""
echo "4. Or run a quick demo:"
echo "   python simple_client.py demo"
echo ""
echo "📁 Directory structure:"
echo "   documents/english/  - English documents"
echo "   documents/japanese/ - Japanese documents" 
echo "   documents/bangla/   - Bangla documents"
echo ""
echo "🎯 Available client commands:"
echo "   scan           - Index all documents"
echo "   search <query> - Search for text"
echo "   list           - List all documents"
echo "   stats          - Show statistics"
echo "   content <file> - Get document content"
echo "   tools          - Show available tools"
echo "   quit           - Exit"
echo ""
echo "🎉 Happy document processing!"
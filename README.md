# Simple Document MCP Server

A minimal MCP (Model Context Protocol) server for document processing and search with multi-language support.

## 🎯 Features

- **Multi-format Support**: PDF, DOCX, XLSX, and TXT files
- **Multi-language Support**: English, Japanese, Bangla (Bengali), and more
- **Full-text Search**: Search across all indexed documents with context
- **Document Metadata**: Extract file type, language, size, and modification date
- **Interactive Client**: Easy-to-use command-line interface
- **Flexible Directory**: Custom documents directory via command-line arguments
- **Configurable Logging**: Adjustable log levels (DEBUG, INFO, WARNING, ERROR)
- **Error Handling**: Robust error handling and logging
- **Auto-create Directories**: Automatically creates missing document directories

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
# Run the setup script
./setup.sh

# Activate the virtual environment
source venv/bin/activate
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create documents directory
mkdir -p documents
```

## 📖 Usage

### Starting the Server
```bash
# Terminal 1: Start the MCP server
python simple_mcp_server.py                    # Use default ./documents directory
python simple_mcp_server.py --dir /path/docs   # Use custom directory
python simple_mcp_server.py -d ~/Documents     # Use home Documents folder
python simple_mcp_server.py --log-level DEBUG  # Enable debug logging
```

### Using the Client
```bash
# Terminal 2: Start the interactive client
python simple_client.py                       # Use default settings
python simple_client.py --dir /path/docs      # Use custom documents directory
python simple_client.py demo                  # Run demo mode
python simple_client.py demo --dir ~/docs     # Run demo with custom directory
python simple_client.py --log-level DEBUG     # Enable debug logging
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `scan` | Scan and index all documents | `scan` |
| `search <query>` | Search for text in documents | `search machine learning` |
| `list` | List all processed documents | `list` |
| `stats` | Show document collection statistics | `stats` |
| `content <filename>` | Get full content of a document | `content sample.txt` |
| `tools` | Show available MCP tools | `tools` |
| `quit` | Exit the client | `quit` |

## 📁 Directory Structure

```
docmcp/
├── simple_mcp_server.py    # Main MCP server
├── simple_client.py        # Interactive client
├── requirements.txt        # Python dependencies
├── setup.sh               # Automated setup script
├── README.md              # This file
└── documents/             # Document storage
    ├── english/           # English documents
    ├── japanese/          # Japanese documents
    └── bangla/            # Bangla documents
```

## 🔧 MCP Tools

The server provides 5 MCP tools:

1. **scan_documents**: Index all documents in the documents directory
2. **search_documents**: Search for text with configurable result limits
3. **list_documents**: List all processed documents with metadata
4. **get_document_stats**: Get collection statistics (size, languages, types)
5. **get_document_content**: Retrieve full content of a specific document

## 🌍 Language Support

The server automatically detects document language using `langdetect`. Supported languages include:

- **English** (en)
- **Japanese** (ja) 
- **Bangla/Bengali** (bn)
- **And many more** (any language supported by langdetect)

## 📄 Supported File Types

| Extension | Type | Library Used |
|-----------|------|--------------|
| `.pdf` | PDF Documents | PyPDF2 |
| `.docx` | Word Documents | python-docx |
| `.xlsx` | Excel Spreadsheets | openpyxl |
| `.txt` | Text Files | Built-in (multi-encoding) |

## 🔍 Search Features

- **Full-text search** across all document content
- **Context highlighting** around matches
- **Multiple matches** per document with position tracking
- **Result limiting** to prevent overwhelming output
- **Case-insensitive** search

## 🛠️ Development

### Adding New File Types

To add support for new file types, extend the `SimpleDocumentProcessor` class:

```python
def extract_text_from_newtype(self, file_path: Path) -> str:
    # Your extraction logic here
    pass

# Add to the extractors dictionary in process_document()
extractors = {
    '.newext': (self.extract_text_from_newtype, "New Type"),
    # ... existing extractors
}
```

### Customizing Search

The search functionality can be enhanced by modifying the `search_documents` method:

```python
def search_documents(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
    # Add regex support, fuzzy matching, etc.
    pass
```

## 🔒 Error Handling

The server includes comprehensive error handling:

- **File reading errors**: Gracefully handles corrupted or unreadable files
- **Encoding issues**: Tries multiple encodings for text files
- **Missing dependencies**: Clear error messages for missing libraries
- **Server errors**: JSON error responses for client handling

## 📊 Example Output

### Server Help
```bash
$ python simple_mcp_server.py --help
usage: simple_mcp_server.py [-h] [--dir DIR] [--log-level {DEBUG,INFO,WARNING,ERROR}] [--version]

Simple Document MCP Server

options:
  -h, --help            show this help message and exit
  --dir DIR, -d DIR     Directory containing documents to process (default: ./documents)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Set logging level (default: INFO)
  --version             show program's version number and exit
```

### Client Help
```bash
$ python simple_client.py --help
usage: simple_client.py [-h] [--dir DIR] [--log-level {DEBUG,INFO,WARNING,ERROR}] [{interactive,demo}]

Simple Document MCP Client

positional arguments:
  {interactive,demo}    Run in interactive mode or demo mode (default: interactive)

options:
  -h, --help            show this help message and exit
  --dir DIR, -d DIR     Directory containing documents to process (uses server default if not specified)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Set server logging level (default: INFO)
```

### Document Scan with Custom Directory
```
🎬 Running Demo Commands...
📁 Documents directory: /custom/path/docs
✅ Scanned and processed 3 documents

📚 Documents (3):
  1. sample.txt (Text File, en)
     Path: /custom/path/docs/sample.txt
     Size: 1.2 KB
     Preview: This is a sample English document for testing...

  2. sample.txt (Text File, ja)
     Path: /custom/path/docs/sample.txt
     Size: 0.8 KB
     Preview: これは日本語のサンプル文書です...
```

### Search Results
```
🎯 Search Results for 'processing' (2 matches):

  1. sample.txt (Text File, en)
     Path: documents/english/sample.txt
     Position: 156
     Context: ...document **processing** system supports...

  2. readme.txt (Text File, en)
     Path: documents/english/readme.txt
     Position: 89
     Context: ...server can **processing**: - PDF files...
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with the provided client
5. Submit a pull request

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🆘 Troubleshooting

### Common Issues

**"Missing required dependency"**
```bash
pip install -r requirements.txt
```

**"Server not found"**
- Make sure you're in the correct directory
- Check that `simple_mcp_server.py` exists
- Verify Python path in the client

**"No documents found"**
- Check that documents exist in the `documents/` directory
- Run the `scan` command first
- Verify file permissions

**"Language detection failed"**
- Document might be too short for reliable detection
- Try with longer text content
- Check for non-text content in files

### Getting Help

1. Check the server logs for detailed error messages
2. Run the demo client: `python simple_client.py demo`
3. Verify your setup with the sample documents
4. Check file permissions and encoding issues
# MCP Server Setup Guide

This guide explains how to set up the Simple Document MCP Server for use with GitHub MCP and other MCP clients.

## 🔧 Quick Setup for GitHub MCP

### 1. Install the Server

```bash
# Clone or download this repository
git clone https://github.com/yourusername/simple-document-mcp-server.git
cd simple-document-mcp-server

# Set up the environment
./setup.sh
```

### 2. Configure for GitHub MCP

Add the server to your MCP client configuration. For GitHub MCP, add this to your `mcp.json`:

```json
{
  "mcpServers": {
    "simple-document-server": {
      "command": "python",
      "args": ["/path/to/simple_mcp_server.py"],
      "cwd": "/path/to/simple-document-mcp-server",
      "env": {
        "PYTHONPATH": "/path/to/simple-document-mcp-server"
      }
    }
  }
}
```

### 3. With Custom Documents Directory

```json
{
  "mcpServers": {
    "simple-document-server": {
      "command": "python", 
      "args": [
        "/path/to/simple_mcp_server.py",
        "--dir",
        "/path/to/your/documents"
      ],
      "cwd": "/path/to/simple-document-mcp-server",
      "env": {
        "PYTHONPATH": "/path/to/simple-document-mcp-server"
      }
    }
  }
}
```

### 4. With Debug Logging

```json
{
  "mcpServers": {
    "simple-document-server": {
      "command": "python",
      "args": [
        "/path/to/simple_mcp_server.py", 
        "--dir",
        "/path/to/your/documents",
        "--log-level", 
        "DEBUG"
      ],
      "cwd": "/path/to/simple-document-mcp-server",
      "env": {
        "PYTHONPATH": "/path/to/simple-document-mcp-server"
      }
    }
  }
}
```

## 🚀 Alternative Setup Methods

### Method 1: Using the provided mcp.json

```bash
# Copy the provided configuration
cp mcp.json ~/.config/mcp/mcp.json

# Or merge with existing configuration
jq -s '.[0] * .[1]' ~/.config/mcp/mcp.json mcp.json > temp.json
mv temp.json ~/.config/mcp/mcp.json
```

### Method 2: Environment-based Configuration

```bash
# Source the MCP configuration
source .mcprc

# Start the server with environment variables
python simple_mcp_server.py --dir "$MCP_SIMPLE_DOC_SERVER_DIR"
```

### Method 3: Global Installation

```bash
# Install globally (optional)
pip install -e .

# Add to system MCP configuration
sudo mkdir -p /etc/mcp
sudo cp mcp.json /etc/mcp/simple-document-server.json
```

## 📋 MCP Client Examples

### Using with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "simple-document-server": {
      "command": "python",
      "args": ["/absolute/path/to/simple_mcp_server.py"],
      "cwd": "/absolute/path/to/simple-document-mcp-server"
    }
  }
}
```

### Using with MCP CLI

```bash
# Install MCP CLI if not already installed
npm install -g @modelcontextprotocol/cli

# Use with MCP CLI
mcp connect simple-document-server
```

### Using with Custom MCP Client

```python
from mcp.client.stdio import stdio_client, StdioServerParameters

# Connect to the server
server_params = StdioServerParameters(
    command="python",
    args=["simple_mcp_server.py", "--dir", "/path/to/docs"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # Use the session...
```

## 🛠️ Configuration Options

### Server Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--dir` | `-d` | Documents directory | `./documents` |
| `--log-level` | | Logging level | `INFO` |
| `--version` | | Show version | |
| `--help` | `-h` | Show help | |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_SIMPLE_DOC_SERVER_DIR` | Documents directory | `./documents` |
| `MCP_SIMPLE_DOC_SERVER_LOG_LEVEL` | Log level | `INFO` |
| `PYTHONPATH` | Python path | Current directory |

## 🔍 Available Tools

The server provides 5 MCP tools:

1. **`scan_documents`** - Index all documents in the directory
2. **`search_documents`** - Full-text search with context highlighting
3. **`list_documents`** - List documents with metadata
4. **`get_document_stats`** - Collection statistics
5. **`get_document_content`** - Retrieve full document content

## 📂 Supported File Types

- **PDF** (.pdf) - Using PyPDF2
- **Word Documents** (.docx) - Using python-docx  
- **Excel Spreadsheets** (.xlsx) - Using openpyxl
- **Text Files** (.txt) - Multi-encoding support

## 🌍 Language Support

- **Automatic Detection** - Using langdetect library
- **Supported Languages** - English, Japanese, Bangla, and 50+ others
- **Encoding Support** - UTF-8, UTF-16, Latin-1, Shift-JIS, CP932

## 🧪 Testing the Setup

### Quick Test

```bash
# Test with demo mode
python simple_client.py demo

# Test with custom directory
python simple_client.py demo --dir /path/to/your/docs
```

### Verify MCP Integration

```bash
# Check server is discoverable
mcp list-servers

# Test tool availability  
mcp call simple-document-server scan_documents

# Test search functionality
mcp call simple-document-server search_documents '{"query": "test"}'
```

## 🔧 Troubleshooting

### Common Issues

**"Server not found"**
- Check absolute paths in configuration
- Verify Python installation and dependencies
- Ensure virtual environment is activated

**"Permission denied"**
- Check file permissions on server script
- Verify directory permissions for documents folder
- Run with appropriate user permissions

**"Import errors"**
- Install requirements: `pip install -r requirements.txt`
- Check PYTHONPATH environment variable
- Verify virtual environment activation

**"No documents found"**
- Check documents directory exists and has files
- Verify supported file formats (.pdf, .docx, .xlsx, .txt)
- Run scan_documents tool first

### Debug Mode

Enable debug logging for troubleshooting:

```json
{
  "mcpServers": {
    "simple-document-server": {
      "command": "python",
      "args": ["simple_mcp_server.py", "--log-level", "DEBUG"],
      "cwd": "/path/to/server"
    }
  }
}
```

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: See README.md for detailed usage
- **Examples**: Check the demo client implementation

## 🔗 Related Projects

- [Model Context Protocol](https://github.com/modelcontextprotocol/protocol)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/desktop)
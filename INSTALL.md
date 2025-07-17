# Installation Guide

Complete installation guide for the Simple Document MCP Server.

## 📋 Prerequisites

- **Python 3.8+** (recommended: Python 3.10+)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

## 🚀 Installation Methods

### Method 1: Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/shaifulshabuj/simple-document-mcp-server.git
cd simple-document-mcp-server

# Run the setup script
chmod +x setup.sh
./setup.sh

# Activate the environment
source venv/bin/activate
```

### Method 2: Manual Installation

```bash
# Clone and navigate
git clone https://github.com/shaifulshabuj/simple-document-mcp-server.git
cd simple-document-mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create documents directory
mkdir -p documents
```

### Method 3: pip Installation

```bash
# Install from PyPI (when published)
pip install simple-document-mcp-server

# Or install from GitHub
pip install git+https://github.com/shaifulshabuj/simple-document-mcp-server.git
```

### Method 4: Development Installation

```bash
# Clone for development
git clone https://github.com/shaifulshabuj/simple-document-mcp-server.git
cd simple-document-mcp-server

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## 🔧 Configuration for GitHub MCP

### Step 1: Basic MCP Configuration

Create or update your MCP configuration file:

**For Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

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

**For general MCP clients** (`~/.config/mcp/mcp.json`):

```json
{
  "mcpServers": {
    "simple-document-server": {
      "command": "python",
      "args": ["simple_mcp_server.py"],
      "cwd": "/absolute/path/to/simple-document-mcp-server",
      "env": {
        "PYTHONPATH": "/absolute/path/to/simple-document-mcp-server"
      }
    }
  }
}
```

### Step 2: Custom Documents Directory

```json
{
  "mcpServers": {
    "simple-document-server": {
      "command": "python",
      "args": [
        "simple_mcp_server.py",
        "--dir",
        "/path/to/your/documents"
      ],
      "cwd": "/absolute/path/to/simple-document-mcp-server"
    }
  }
}
```

### Step 3: Advanced Configuration

```json
{
  "mcpServers": {
    "simple-document-server": {
      "command": "python",
      "args": [
        "simple_mcp_server.py",
        "--dir",
        "/path/to/your/documents",
        "--log-level",
        "INFO"
      ],
      "cwd": "/absolute/path/to/simple-document-mcp-server",
      "env": {
        "PYTHONPATH": "/absolute/path/to/simple-document-mcp-server",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## 🧪 Verification

### Test 1: Basic Functionality

```bash
# Activate environment
source venv/bin/activate

# Test the server help
python simple_mcp_server.py --help

# Test the client help  
python simple_client.py --help
```

### Test 2: Demo Mode

```bash
# Run demo with default documents
python simple_client.py demo

# Run demo with custom directory
python simple_client.py demo --dir /path/to/your/docs
```

### Test 3: MCP Integration

```bash
# Test MCP connectivity (if you have mcp CLI)
mcp list-servers

# Test tool calls
mcp call simple-document-server scan_documents
mcp call simple-document-server search_documents '{"query": "test"}'
```

## 🔧 Platform-Specific Instructions

### Windows

```cmd
# Clone repository
git clone https://github.com/shaifulshabuj/simple-document-mcp-server.git
cd simple-document-mcp-server

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test
python simple_client.py demo
```

### macOS

```bash
# Install Python (if needed)
brew install python3

# Clone and setup
git clone https://github.com/shaifulshabuj/simple-document-mcp-server.git
cd simple-document-mcp-server
./setup.sh
source venv/bin/activate

# Test
python simple_client.py demo
```

### Linux (Ubuntu/Debian)

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Clone and setup
git clone https://github.com/shaifulshabuj/simple-document-mcp-server.git
cd simple-document-mcp-server
./setup.sh
source venv/bin/activate

# Test
python simple_client.py demo
```

## 🚨 Troubleshooting

### Common Issues

**1. Python not found**
```bash
# Check Python installation
python3 --version
which python3

# On Windows
python --version
where python
```

**2. Permission denied**
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x simple_mcp_server.py
chmod +x simple_client.py
```

**3. Module not found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**4. MCP server not starting**
```bash
# Test server directly
python simple_mcp_server.py --log-level DEBUG

# Check absolute paths in MCP configuration
# Ensure virtual environment is activated before starting MCP client
```

**5. Documents not found**
```bash
# Check directory exists
ls -la documents/

# Create sample documents
mkdir -p documents/test
echo "Test content" > documents/test/sample.txt

# Test with specific directory
python simple_client.py demo --dir documents/test
```

### Debug Mode

Enable detailed logging:

```bash
# Server debug mode
python simple_mcp_server.py --log-level DEBUG

# Client with debug server
python simple_client.py demo --log-level DEBUG
```

### Dependency Issues

```bash
# Update pip
pip install --upgrade pip

# Reinstall specific packages
pip uninstall PyPDF2 python-docx openpyxl langdetect mcp
pip install PyPDF2 python-docx openpyxl langdetect mcp

# Install with specific versions
pip install -r requirements.txt --force-reinstall
```

## 📞 Getting Help

1. **Check the logs** - Use `--log-level DEBUG` for detailed output
2. **Verify paths** - Ensure all paths in configuration are absolute
3. **Test isolation** - Try running components separately
4. **Check permissions** - Ensure read/write access to directories
5. **Update dependencies** - Make sure all packages are current

## 🔗 Next Steps

After successful installation:

1. **Add your documents** - Place files in the documents directory
2. **Configure MCP client** - Set up your preferred MCP client
3. **Customize settings** - Adjust directories and logging as needed
4. **Explore features** - Try all available tools and search capabilities

For detailed usage instructions, see [README.md](README.md) and [MCP_SETUP.md](MCP_SETUP.md).
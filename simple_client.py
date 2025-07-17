#!/usr/bin/env python3
"""
Simple MCP Client
A test client for the Simple Document MCP Server.
"""

import asyncio
import json
import sys
import subprocess
import argparse
from typing import Any, Dict, List
from contextlib import asynccontextmanager

try:
    import mcp
    from mcp.client.session import ClientSession
    from mcp.client.stdio import stdio_client, StdioServerParameters
except ImportError as e:
    print(f"Missing MCP dependency: {e}")
    print("Please install with: pip install mcp")
    sys.exit(1)

class SimpleMCPClient:
    """Simple client for testing the MCP server"""
    
    def __init__(self):
        self.session: ClientSession = None
        self.tools: List[Dict[str, Any]] = []
    
    @asynccontextmanager
    async def connect(self, command_args: List[str]):
        """Connect to the MCP server"""
        # Create server parameters
        server_params = StdioServerParameters(
            command=command_args[0],
            args=command_args[1:]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                await self.initialize()
                yield self
    
    async def initialize(self):
        """Initialize the client and get available tools"""
        # Initialize the session first
        await self.session.initialize()
        
        # Now get the tools
        result = await self.session.list_tools()
        self.tools = result.tools
        print(f"📡 Connected to server with {len(self.tools)} tools")
    
    async def call_tool(self, name: str, arguments: Dict[str, Any] = None) -> Any:
        """Call a tool on the server"""
        if arguments is None:
            arguments = {}
        
        result = await self.session.call_tool(name, arguments)
        
        if result.content:
            # Extract text content
            text_content = ""
            for content in result.content:
                if hasattr(content, 'text'):
                    text_content += content.text
            
            try:
                return json.loads(text_content)
            except json.JSONDecodeError:
                return {"raw_content": text_content}
        
        return {"error": "No content returned"}
    
    def print_tools(self):
        """Print available tools"""
        print("\n🔧 Available Tools:")
        for i, tool in enumerate(self.tools, 1):
            print(f"  {i}. {tool.name}")
            print(f"     {tool.description}")
        print()
    
    def print_documents(self, documents: List[Dict[str, Any]]):
        """Print document list in a formatted way"""
        if not documents:
            print("📄 No documents found.")
            return
        
        print(f"\n📚 Documents ({len(documents)}):")
        for i, doc in enumerate(documents, 1):
            print(f"  {i}. {doc['filename']} ({doc['file_type']}, {doc['language']})")
            print(f"     Path: {doc['path']}")
            if 'size' in doc:
                size_kb = doc['size'] / 1024
                print(f"     Size: {size_kb:.1f} KB")
            if 'content_preview' in doc:
                preview = doc['content_preview'].replace('\n', ' ')[:100]
                print(f"     Preview: {preview}...")
            print()
    
    def print_search_results(self, results: List[Dict[str, Any]], query: str):
        """Print search results in a formatted way"""
        if not results:
            print(f"🔍 No results found for '{query}'")
            return
        
        print(f"\n🎯 Search Results for '{query}' ({len(results)} matches):")
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. {result['filename']} ({result['file_type']}, {result['language']})")
            print(f"     Path: {result['path']}")
            print(f"     Position: {result['position']}")
            if 'match_number' in result and 'total_matches' in result:
                print(f"     Match: {result['match_number']} of {result['total_matches']}")
            print(f"     Context: ...{result['context']}...")
            print()
    
    def print_stats(self, stats: Dict[str, Any]):
        """Print document statistics"""
        print("\n📊 Document Statistics:")
        print(f"  Total Documents: {stats.get('total_documents', 0)}")
        
        if stats.get('total_size_mb'):
            print(f"  Total Size: {stats['total_size_mb']} MB")
            print(f"  Average Size: {stats.get('avg_size_kb', 0)} KB")
        
        if stats.get('languages'):
            print("  Languages:")
            for lang, count in stats['languages'].items():
                print(f"    {lang}: {count} documents")
        
        if stats.get('file_types'):
            print("  File Types:")
            for file_type, count in stats['file_types'].items():
                print(f"    {file_type}: {count} documents")
        print()

def create_server_command(documents_dir: str = None, log_level: str = "INFO") -> List[str]:
    """Create the server command with arguments"""
    command = [sys.executable, "simple_mcp_server.py"]
    
    if documents_dir:
        command.extend(["--dir", documents_dir])
    
    if log_level != "INFO":
        command.extend(["--log-level", log_level])
    
    return command

def parse_client_arguments():
    """Parse client command line arguments"""
    parser = argparse.ArgumentParser(
        description="Simple Document MCP Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple_client.py                       # Use default settings
  python simple_client.py --dir /path/docs      # Use custom documents directory
  python simple_client.py demo --dir ~/docs     # Run demo with custom directory
  python simple_client.py --log-level DEBUG     # Enable debug logging
        """.strip()
    )
    
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["interactive", "demo"],
        default="interactive",
        help="Run in interactive mode or demo mode (default: interactive)"
    )
    
    parser.add_argument(
        "--dir", "-d",
        type=str,
        help="Directory containing documents to process (uses server default if not specified)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set server logging level (default: INFO)"
    )
    
    return parser.parse_args()

async def interactive_client(documents_dir: str = None, log_level: str = "INFO"):
    """Run an interactive client session"""
    print("🚀 Simple Document MCP Client")
    if documents_dir:
        print(f"📁 Documents directory: {documents_dir}")
    print("Connecting to server...")
    
    # Connect to the server
    server_command = create_server_command(documents_dir, log_level)
    
    try:
        async with SimpleMCPClient().connect(server_command) as client:
            print("✅ Connected successfully!")
            
            while True:
                print("\n" + "="*50)
                print("Available commands:")
                print("  scan           - Scan and index documents")
                print("  search <query> - Search for text in documents")
                print("  list           - List all documents")
                print("  stats          - Show document statistics")
                print("  content <file> - Get full content of a document")
                print("  tools          - Show available tools")
                print("  quit           - Exit the client")
                print("="*50)
                
                command = input("\n📝 Enter command: ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif command.lower() == 'scan':
                    print("🔍 Scanning documents...")
                    result = await client.call_tool("scan_documents")
                    
                    if result.get('status') == 'success':
                        print(f"✅ {result['message']}")
                        if result.get('documents'):
                            client.print_documents(result['documents'])
                    else:
                        print(f"❌ Error: {result}")
                
                elif command.lower().startswith('search '):
                    query = command[7:].strip()
                    if not query:
                        print("❌ Please provide a search query")
                        continue
                    
                    print(f"🔍 Searching for: '{query}'")
                    result = await client.call_tool("search_documents", {"query": query})
                    
                    if result.get('status') == 'success':
                        print(f"✅ Found {result['results_count']} results")
                        client.print_search_results(result['results'], query)
                    else:
                        print(f"❌ Error: {result}")
                
                elif command.lower() == 'list':
                    print("📋 Getting document list...")
                    result = await client.call_tool("list_documents")
                    
                    if result.get('status') == 'success':
                        print(f"✅ Found {result['total_documents']} documents")
                        client.print_documents(result['documents'])
                    else:
                        print(f"❌ Error: {result}")
                
                elif command.lower() == 'stats':
                    print("📊 Getting statistics...")
                    result = await client.call_tool("get_document_stats")
                    
                    if result.get('status') == 'success':
                        client.print_stats(result['stats'])
                    else:
                        print(f"❌ Error: {result}")
                
                elif command.lower().startswith('content '):
                    filename = command[8:].strip()
                    if not filename:
                        print("❌ Please provide a filename")
                        continue
                    
                    print(f"📄 Getting content for: {filename}")
                    result = await client.call_tool("get_document_content", {"filename": filename})
                    
                    if result.get('status') == 'success':
                        print(f"✅ Content of {result['filename']}:")
                        print(f"File Type: {result['file_type']}")
                        print(f"Language: {result['language']}")
                        print(f"Size: {result['size']} bytes")
                        print("\n" + "="*50)
                        print(result['content'])
                        print("="*50)
                    else:
                        print(f"❌ Error: {result.get('message', result)}")
                
                elif command.lower() == 'tools':
                    client.print_tools()
                
                else:
                    print("❌ Unknown command. Type 'quit' to exit.")
    
    except FileNotFoundError:
        print("❌ Server not found. Make sure simple_mcp_server.py is in the current directory.")
    except Exception as e:
        print(f"❌ Connection error: {e}")

async def demo_commands(documents_dir: str = None, log_level: str = "INFO"):
    """Run a demo with automatic commands"""
    print("🎬 Running Demo Commands...")
    if documents_dir:
        print(f"📁 Documents directory: {documents_dir}")
    
    server_command = create_server_command(documents_dir, log_level)
    
    try:
        async with SimpleMCPClient().connect(server_command) as client:
            print("✅ Connected to server")
            
            # Demo 1: List tools
            print("\n1️⃣ Listing available tools...")
            client.print_tools()
            
            # Demo 2: Scan documents
            print("2️⃣ Scanning documents...")
            result = await client.call_tool("scan_documents")
            if result.get('status') == 'success':
                print(f"✅ {result['message']}")
                client.print_documents(result['documents'])
            
            # Demo 3: Get stats
            print("3️⃣ Getting statistics...")
            result = await client.call_tool("get_document_stats")
            if result.get('status') == 'success':
                client.print_stats(result['stats'])
            
            # Demo 4: Search for something
            print("4️⃣ Searching for 'document'...")
            result = await client.call_tool("search_documents", {"query": "document"})
            if result.get('status') == 'success':
                client.print_search_results(result['results'], "document")
            
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    # Parse arguments
    args = parse_client_arguments()
    
    # Run the appropriate mode
    if args.mode == "demo":
        asyncio.run(demo_commands(args.dir, args.log_level))
    else:
        asyncio.run(interactive_client(args.dir, args.log_level))
"""Unit tests for document processing functionality"""

import pytest
import tempfile
import shutil
from pathlib import Path
from simple_mcp_server import SimpleDocumentProcessor, DocumentInfo


@pytest.fixture
def temp_docs_dir():
    """Create a temporary documents directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def doc_processor(temp_docs_dir):
    """Create a document processor instance"""
    return SimpleDocumentProcessor(documents_dir=temp_docs_dir)


class TestDocumentProcessor:
    """Test cases for SimpleDocumentProcessor"""
    
    def test_init_creates_directory(self, temp_docs_dir):
        """Test that initialization creates documents directory"""
        test_dir = Path(temp_docs_dir) / "new_docs"
        processor = SimpleDocumentProcessor(documents_dir=str(test_dir))
        assert test_dir.exists()
    
    def test_extract_text_from_txt(self, doc_processor, temp_docs_dir):
        """Test text extraction from plain text files"""
        test_file = Path(temp_docs_dir) / "test.txt"
        test_content = "Hello, World!\nThis is a test document."
        test_file.write_text(test_content, encoding='utf-8')
        
        extracted = doc_processor.extract_text_from_txt(test_file)
        assert extracted == test_content
    
    def test_detect_language_english(self, doc_processor):
        """Test language detection for English text"""
        text = "This is a sample English document with enough text for detection."
        lang = doc_processor.detect_language(text)
        assert lang == "en"
    
    def test_detect_language_short_text(self, doc_processor):
        """Test language detection with short text"""
        text = "Hi"
        lang = doc_processor.detect_language(text)
        assert lang == "unknown"
    
    def test_process_document_txt(self, doc_processor, temp_docs_dir):
        """Test processing a text document"""
        test_file = Path(temp_docs_dir) / "sample.txt"
        test_content = "This is a comprehensive sample document for testing purposes with sufficient length."
        test_file.write_text(test_content, encoding='utf-8')
        
        doc_info = doc_processor.process_document(test_file)
        
        assert doc_info is not None
        assert doc_info.filename == "sample.txt"
        assert doc_info.content == test_content
        assert doc_info.file_type == "Text File"
        assert doc_info.language == "en"
        assert doc_info.size > 0
    
    def test_process_document_unsupported_type(self, doc_processor, temp_docs_dir):
        """Test processing an unsupported file type"""
        test_file = Path(temp_docs_dir) / "test.xyz"
        test_file.write_text("test content")
        
        doc_info = doc_processor.process_document(test_file)
        assert doc_info is None
    
    def test_process_document_nonexistent(self, doc_processor, temp_docs_dir):
        """Test processing a non-existent file"""
        test_file = Path(temp_docs_dir) / "nonexistent.txt"
        doc_info = doc_processor.process_document(test_file)
        assert doc_info is None
    
    def test_scan_documents(self, doc_processor, temp_docs_dir):
        """Test scanning multiple documents"""
        # Create test files
        files = {
            "doc1.txt": "First English document with enough content for detection.",
            "doc2.txt": "Second English document with enough content for detection.",
        }
        
        for filename, content in files.items():
            file_path = Path(temp_docs_dir) / filename
            file_path.write_text(content, encoding='utf-8')
        
        documents = doc_processor.scan_documents()
        
        assert len(documents) == 2
        assert all(isinstance(doc, DocumentInfo) for doc in documents)
        filenames = [doc.filename for doc in documents]
        assert "doc1.txt" in filenames
        assert "doc2.txt" in filenames
    
    def test_search_documents_basic(self, doc_processor, temp_docs_dir):
        """Test basic document search"""
        test_file = Path(temp_docs_dir) / "searchable.txt"
        content = "This document contains the word searchterm in multiple places. Another searchterm here."
        test_file.write_text(content, encoding='utf-8')
        
        doc_processor.scan_documents()
        results = doc_processor.search_documents("searchterm")
        
        assert len(results) > 0
        assert results[0]["filename"] == "searchable.txt"
        assert "searchterm" in results[0]["context"].lower()
    
    def test_search_documents_case_insensitive(self, doc_processor, temp_docs_dir):
        """Test case-insensitive search"""
        test_file = Path(temp_docs_dir) / "case.txt"
        content = "This document contains SearchTerm in different cases."
        test_file.write_text(content, encoding='utf-8')
        
        doc_processor.scan_documents()
        results = doc_processor.search_documents("searchterm")
        
        assert len(results) > 0
    
    def test_search_documents_no_results(self, doc_processor, temp_docs_dir):
        """Test search with no matching results"""
        test_file = Path(temp_docs_dir) / "empty.txt"
        content = "This document does not contain the search term."
        test_file.write_text(content, encoding='utf-8')
        
        doc_processor.scan_documents()
        results = doc_processor.search_documents("nonexistent")
        
        assert len(results) == 0
    
    def test_search_documents_max_results(self, doc_processor, temp_docs_dir):
        """Test search result limiting"""
        test_file = Path(temp_docs_dir) / "many.txt"
        content = " ".join(["test"] * 100)  # Many occurrences
        test_file.write_text(content, encoding='utf-8')
        
        doc_processor.scan_documents()
        results = doc_processor.search_documents("test", max_results=3)
        
        assert len(results) <= 3
    
    def test_get_document_stats_empty(self, doc_processor):
        """Test statistics for empty document collection"""
        stats = doc_processor.get_document_stats()
        assert stats["total_documents"] == 0
    
    def test_get_document_stats_with_documents(self, doc_processor, temp_docs_dir):
        """Test statistics with documents"""
        files = {
            "doc1.txt": "English document with enough content for detection.",
            "doc2.txt": "Another English document with enough content for detection.",
        }
        
        for filename, content in files.items():
            file_path = Path(temp_docs_dir) / filename
            file_path.write_text(content, encoding='utf-8')
        
        doc_processor.scan_documents()
        stats = doc_processor.get_document_stats()
        
        assert stats["total_documents"] == 2
        assert stats["total_size_bytes"] > 0
        assert "languages" in stats
        assert "file_types" in stats
        assert "Text File" in stats["file_types"]

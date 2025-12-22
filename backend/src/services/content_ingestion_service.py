from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.models.content_models import BookContent, ContentChunk
import uuid


class ContentIngestionService:
    def __init__(self):
        # Initialize the text splitter with appropriate chunk size
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # 1000 characters per chunk
            chunk_overlap=100,  # 100 characters overlap between chunks
            separators=["\n\n", "\n", " ", ""]
        )
    
    def split_book_content(self, book_content: BookContent) -> List[ContentChunk]:
        """
        Split the book content into manageable chunks
        """
        chunks = self.text_splitter.split_text(book_content.content)
        
        content_chunks = []
        for idx, chunk_text in enumerate(chunks):
            chunk = ContentChunk(
                id=str(uuid.uuid4()),
                content=chunk_text,
                book_id=book_content.id,
                chunk_index=idx
            )
            content_chunks.append(chunk)
        
        return content_chunks
    
    def create_book_with_chunks(self, book_id: str, title: str, author: str, content: str) -> BookContent:
        """
        Create a BookContent object with properly split chunks
        """
        book = BookContent(
            id=book_id,
            title=title,
            author=author,
            content=content
        )
        
        # Split the content into chunks
        chunks = self.split_book_content(book)
        book.chunks = chunks
        
        return book
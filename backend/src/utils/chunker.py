import re
from typing import List
from src.models.chapter import ContentChunk

class TextChunker:
    """
    Utility class for splitting text into chunks suitable for embedding
    """

    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, chapter_id: str) -> List[ContentChunk]:
        """
        Split text into chunks of appropriate size
        """
        # Split by paragraphs first
        paragraphs = text.split('\n\n')

        chunks = []
        chunk_index = 0

        current_chunk = ""
        for paragraph in paragraphs:
            # If adding this paragraph would exceed the chunk size
            if len(current_chunk) + len(paragraph) > self.max_chunk_size:
                # Save the current chunk if it's not empty
                if current_chunk.strip():
                    chunk = ContentChunk(
                        id=f"{chapter_id}_chunk_{chunk_index}",
                        content=current_chunk.strip(),
                        chapterId=chapter_id,
                        chunkIndex=chunk_index,
                        embedding=None,  # Will be filled in later
                        metadata={"source": "paragraph_split"}
                    )
                    chunks.append(chunk)
                    chunk_index += 1

                # Start a new chunk with overlap from the previous chunk
                if len(paragraph) > self.max_chunk_size:
                    # If the paragraph itself is too long, split it
                    sub_chunks = self._split_large_paragraph(paragraph, chapter_id, chunk_index)
                    chunks.extend(sub_chunks)
                    chunk_index += len(sub_chunks)
                    current_chunk = ""
                else:
                    # Start new chunk with some overlap
                    if self.overlap > 0 and chunks:
                        # Add overlap from the last chunk
                        last_chunk_content = chunks[-1].content
                        overlap_text = last_chunk_content[-self.overlap:]
                        current_chunk = overlap_text + "\n\n" + paragraph
                    else:
                        current_chunk = paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add the final chunk if it has content
        if current_chunk.strip():
            chunk = ContentChunk(
                id=f"{chapter_id}_chunk_{chunk_index}",
                content=current_chunk.strip(),
                chapterId=chapter_id,
                chunkIndex=chunk_index,
                embedding=None,  # Will be filled in later
                metadata={"source": "paragraph_split"}
            )
            chunks.append(chunk)

        return chunks

    def _split_large_paragraph(self, paragraph: str, chapter_id: str, start_index: int) -> List[ContentChunk]:
        """
        Split a large paragraph into smaller chunks
        """
        chunks = []
        chunk_index = start_index

        # Split by sentences
        sentences = re.split(r'[.!?]+', paragraph)

        current_chunk = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) > self.max_chunk_size:
                # Save the current chunk
                if current_chunk.strip():
                    chunk = ContentChunk(
                        id=f"{chapter_id}_chunk_{chunk_index}",
                        content=current_chunk.strip(),
                        chapterId=chapter_id,
                        chunkIndex=chunk_index,
                        embedding=None,
                        metadata={"source": "sentence_split"}
                    )
                    chunks.append(chunk)
                    chunk_index += 1
                    current_chunk = sentence
                else:
                    current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += ". " + sentence
                else:
                    current_chunk = sentence

        # Add the final chunk
        if current_chunk.strip():
            chunk = ContentChunk(
                id=f"{chapter_id}_chunk_{chunk_index}",
                content=current_chunk.strip(),
                chapterId=chapter_id,
                chunkIndex=chunk_index,
                embedding=None,
                metadata={"source": "sentence_split"}
            )
            chunks.append(chunk)

        return chunks

# Global instance
chunker = TextChunker()
from typing import List
from src.services.cohere_service import CohereClient
from src.models.content_models import ContentChunk
import re


class GenerationService:
    def __init__(self):
        self.cohere_client = CohereClient()

    def generate_answer(self, question: str, context_chunks: List[ContentChunk]) -> str:
        """
        Generate an answer based on the question and context chunks
        """
        # Combine all context chunks into a single context string
        context = "\n\n".join([chunk.content for chunk in context_chunks])

        # Generate response using Cohere
        answer = self.cohere_client.generate_response(question, context)

        return answer

    def validate_answer_context(self, answer: str, context_chunks: List[ContentChunk]) -> bool:
        """
        Validate that the answer is grounded in the provided context
        """
        # This is a basic validation - in a real implementation,
        # you'd want more sophisticated validation
        answer_lower = answer.lower()

        # Check if key terms from context appear in the answer
        for chunk in context_chunks:
            chunk_lower = chunk.content.lower()
            # Check if at least part of the context appears to be referenced in the answer
            if len(chunk_lower) > 20:  # Only check reasonably sized chunks
                chunk_words = set(chunk_lower.split()[:10])  # Take first 10 words as representative
                answer_words = set(answer_lower.split())

                # If there's significant overlap in terms, consider it validated
                if len(chunk_words.intersection(answer_words)) > 0:
                    return True

        # If no context seems to be referenced, the answer may not be properly grounded
        return False

    def validate_selected_text_response(self, answer: str, selected_text: str) -> bool:
        """
        Validate that the response is based only on the selected text and doesn't
        incorporate external knowledge or context from the full book.
        """
        # Basic validation to ensure the response is grounded in the selected text
        answer_lower = answer.lower()
        selected_text_lower = selected_text.lower()

        # Extract key terms from the selected text
        selected_words = set(re.findall(r'\b\w+\b', selected_text_lower))

        # Extract key terms from the answer
        answer_words = set(re.findall(r'\b\w+\b', answer_lower))

        # Check if there's overlap between selected text and answer
        overlap = selected_words.intersection(answer_words)

        # If there's significant overlap, the answer is likely based on the selected text
        if len(overlap) > 0:
            return True

        # Additional check: ensure the answer doesn't contain information
        # that's clearly not in the selected text
        selected_sentences = selected_text_lower.split('.')
        answer_sentences = answer_lower.split('.')

        # Check if any sentence in the answer is similar to sentences in the selected text
        for ans_sent in answer_sentences:
            for sel_sent in selected_sentences:
                if len(ans_sent) > 10 and len(sel_sent) > 10:  # Only compare substantial sentences
                    if ans_sent.strip() in sel_sent or sel_sent in ans_sent.strip():
                        return True

        return False
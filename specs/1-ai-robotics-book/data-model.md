# Data Model: AI/Spec-Driven Book Creation + Integrated RAG Chatbot Deployment

## Entities

### Book Chapter
-   **Description**: A self-contained unit of technical content, written in MDX.
-   **Attributes (conceptual, not implementation specific)**:
    -   `id`: Unique identifier for the chapter.
    -   `title`: The title of the chapter.
    -   `content_mdx`: The full content of the chapter in MDX format.
    -   `objective_summary`: A brief overview of the chapter's learning goals.
    -   `step_by_step_instructions`: Detailed guidance for practical implementation.
    -   `verified_code_snippets`: Code blocks that have been validated for functionality.
    -   `outcome_validation_steps`: Instructions to verify the results of following the chapter.
    -   `troubleshooting_notes`: Common issues and their resolutions.
    -   `order`: Numerical order for chapter sequencing within the book.

### Docusaurus Site
-   **Description**: The static website generated from the collection of Book Chapters, providing navigation, search, and a themed user interface.
-   **Relationships**: Comprises multiple `Book Chapter` entities.

### RAG Chatbot
-   **Description**: An interactive, embedded UI component within the Docusaurus Site that provides natural language answers by retrieving information from the Book Chapters and generating responses.
-   **Relationships**: Interacts with the `Backend Service (FastAPI)` and `Vector Database (Qdrant)`. Consumes `User Selected Text` as context.

### Vector Database (Qdrant)
-   **Description**: A specialized database responsible for storing high-dimensional vector embeddings of Book Chapter content, enabling efficient semantic search and retrieval.
-   **Attributes (conceptual)**:
    -   `collection_name`: Identifier for the vector collection (e.g., `book_embeddings`).
    -   `vector_size`: Dimensionality of the vectors (must match embedding model output).
    -   `distance_metric`: Metric used for similarity search (e.g., Cosine).
    -   `points`: Individual entries, each containing:
        -   `id`: Unique identifier for the vector point (e.g., hash of chunk, chunk ID).
        -   `vector`: The high-dimensional embedding of a text chunk.
        -   `payload`: Metadata associated with the vector (e.g., `chapter_id`, `chunk_text`, `page_number`).
-   **Relationships**: Stores embeddings derived from `Book Chapter` content.

### Backend Service (FastAPI)
-   **Description**: A Python-based API server that acts as an intermediary, handling requests from the RAG Chatbot, interfacing with the Vector Database, and orchestrating response generation.
-   **Attributes (conceptual)**:
    -   `API Endpoints`:
        -   `/embed`: Accepts text, returns embeddings.
        -   `/retrieve`: Accepts query, returns relevant text chunks from Qdrant.
        -   `/chat`: Accepts user query and optional selected text, returns RAG-generated response.
    -   `Dependencies`: `Qdrant Client`, `OpenAI Agents SDK`.
-   **Relationships**: Communicates with `RAG Chatbot`, `Vector Database (Qdrant)`, and `OpenAI Agents SDK`.

### User Selected Text
-   **Description**: A specific segment of text highlighted by a user within a Book Chapter, used as a precise contextual constraint for RAG Chatbot queries.
-   **Attributes (conceptual)**:
    -   `text_content`: The actual string of text selected by the user.
    -   `source_chapter_id`: Identifier for the chapter from which the text was selected.
    -   `start_index`, `end_index`: (Optional) Positional information within the source content.
-   **Relationships**: Provided as input to the `RAG Chatbot` (via `Backend Service`).

"""
RAG (Retrieval-Augmented Generation) system for DocuBotAI.
"""
from pathlib import Path
from typing import List, Tuple

import chromadb
from anthropic import Anthropic
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger
from pydantic import BaseModel


class Document(BaseModel):
    """Model representing a document in the RAG system."""
    content: str
    metadata: dict


class RAGSystem:
    """RAG system for documentation retrieval and generation."""

    def __init__(
        self,
        data_dir: str | Path,
        claude_api_key: str | None = None,
        collection_name: str = "documentation",
    ):
        """Initialize the RAG system.

        Args:
            data_dir: Directory containing processed documentation.
            claude_api_key: Claude API key. If not provided, will try to get from environment.
            collection_name: Name of the ChromaDB collection to use.
        """
        self.data_dir = Path(data_dir)
        self.anthropic = Anthropic(api_key=claude_api_key)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=str(self.data_dir / ".chroma"))
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=HuggingFaceEmbeddings(),
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the RAG system.

        Args:
            documents: List of documents to add.
        """
        for doc in documents:
            # Split text into chunks
            chunks = self.text_splitter.split_text(doc.content)
            
            # Add chunks to ChromaDB
            self.collection.add(
                documents=chunks,
                metadatas=[doc.metadata for _ in chunks],
                ids=[f"chunk_{i}" for i in range(len(chunks))],
            )
        
        logger.info(f"Added {len(documents)} documents to RAG system")

    def query(
        self,
        question: str,
        context: str | None = None,
        num_chunks: int = 5,
    ) -> Tuple[str, List[str], float]:
        """Query the RAG system.

        Args:
            question: Question to answer.
            context: Optional additional context.
            num_chunks: Number of chunks to retrieve.

        Returns:
            Tuple of (answer, source_documents, confidence_score).
        """
        # Retrieve relevant chunks
        results = self.collection.query(
            query_texts=[question],
            n_results=num_chunks,
        )
        chunks = results["documents"][0]
        
        # Build prompt with retrieved chunks
        prompt = "You are a helpful AI assistant. Answer the following question based on the provided documentation:\n\n"
        prompt += f"Question: {question}\n\n"
        if context:
            prompt += f"Additional context: {context}\n\n"
        prompt += "Relevant documentation:\n"
        for i, chunk in enumerate(chunks, 1):
            prompt += f"{i}. {chunk}\n"
        prompt += "\nAnswer:"

        # Generate answer using Claude
        response = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.content[0].text

        # Calculate confidence score (placeholder implementation)
        confidence = 0.95  # TODO: Implement proper confidence scoring
        
        return answer, chunks, confidence
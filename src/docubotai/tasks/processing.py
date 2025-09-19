"""
Celery tasks for document processing.
"""
from typing import List

from celery import chain
from loguru import logger

from docubot.core.celery import celery_app
from docubot.core.database import db_session
from docubot.models.database import Document, DocumentChunk
from docubot.rag.system import RAGSystem


@celery_app.task(bind=True, name="processing.chunk_document")
def chunk_document(self, document_id: int) -> List[int]:
    """Split a document into chunks for the RAG system.

    Args:
        document_id: ID of the document to chunk.

    Returns:
        List of chunk IDs.
    """
    with db_session() as db:
        # Get document
        document = db.query(Document).get(document_id)
        if not document:
            raise ValueError(f"Document {document_id} not found")

        # Initialize RAG system
        rag = RAGSystem(data_dir="data/processed")
        
        # Split document into chunks
        chunks = rag.text_splitter.split_text(document.content)
        
        # Save chunks
        chunk_ids = []
        for chunk_text in chunks:
            chunk = DocumentChunk(
                document=document,
                content=chunk_text,
            )
            db.add(chunk)
            chunk_ids.append(chunk.id)
        
        db.commit()
        logger.info(f"Created {len(chunk_ids)} chunks for document {document_id}")
        return chunk_ids


@celery_app.task(bind=True, name="processing.embed_chunks")
def embed_chunks(self, chunk_ids: List[int]) -> List[int]:
    """Generate embeddings for document chunks.

    Args:
        chunk_ids: List of chunk IDs to embed.

    Returns:
        List of processed chunk IDs.
    """
    with db_session() as db:
        # Initialize RAG system
        rag = RAGSystem(data_dir="data/processed")
        
        # Process chunks in batches
        batch_size = 10
        for i in range(0, len(chunk_ids), batch_size):
            batch = chunk_ids[i:i + batch_size]
            chunks = db.query(DocumentChunk).filter(
                DocumentChunk.id.in_(batch)
            ).all()
            
            # Generate embeddings
            for chunk in chunks:
                # TODO: Implement proper embedding generation
                chunk.embedding_id = f"embedding_{chunk.id}"
            
            db.commit()
            logger.info(f"Embedded chunks {batch}")
        
        return chunk_ids


@celery_app.task(bind=True, name="processing.index_chunks")
def index_chunks(self, chunk_ids: List[int]) -> List[int]:
    """Index document chunks in the RAG system.

    Args:
        chunk_ids: List of chunk IDs to index.

    Returns:
        List of indexed chunk IDs.
    """
    with db_session() as db:
        # Initialize RAG system
        rag = RAGSystem(data_dir="data/processed")
        
        # Get chunks
        chunks = db.query(DocumentChunk).filter(
            DocumentChunk.id.in_(chunk_ids)
        ).all()
        
        # Index chunks
        for chunk in chunks:
            if not chunk.embedding_id:
                continue
            
            # TODO: Implement proper chunk indexing
            logger.info(f"Indexed chunk {chunk.id}")
        
        return chunk_ids


def process_document(document_id: int) -> chain:
    """Process a document through the complete pipeline.

    Args:
        document_id: ID of the document to process.

    Returns:
        Celery chain of tasks.
    """
    return chain(
        chunk_document.s(document_id),
        embed_chunks.s(),
        index_chunks.s(),
    )
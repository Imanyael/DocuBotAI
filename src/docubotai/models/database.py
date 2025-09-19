"""
Database models for DocuBotAI.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class Document(Base):
    """Model for storing scraped documents."""
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(1024))
    title: Mapped[str] = mapped_column(String(256))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    """Model for storing document chunks for RAG system."""
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    content: Mapped[str] = mapped_column(Text)
    embedding_id: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationships
    document: Mapped[Document] = relationship(back_populates="chunks")


class ScrapingJob(Base):
    """Model for tracking scraping jobs."""
    __tablename__ = "scraping_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_url: Mapped[str] = mapped_column(String(1024))
    status: Mapped[str] = mapped_column(String(32))  # pending, running, completed, failed
    error: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # Relationships
    documents: Mapped[list[Document]] = relationship(
        secondary="job_documents",
        back_populates="jobs"
    )


class JobDocument(Base):
    """Association table for jobs and documents."""
    __tablename__ = "job_documents"

    job_id: Mapped[int] = mapped_column(ForeignKey("scraping_jobs.id"), primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), primary_key=True)
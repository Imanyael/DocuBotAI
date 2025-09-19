"""
Celery tasks for scraping operations.
"""
from datetime import datetime

from celery import chain
from loguru import logger

from docubot.core.celery import celery_app
from docubot.core.database import db_session
from docubot.models.database import Document, ScrapingJob
from docubot.scrapers.apify import ApifyScraper


@celery_app.task(bind=True, name="scraping.start_job")
def start_scraping_job(self, source_url: str) -> int:
    """Start a new scraping job.

    Args:
        source_url: URL to scrape.

    Returns:
        ID of the created job.
    """
    with db_session() as db:
        # Create new job
        job = ScrapingJob(
            source_url=source_url,
            status="pending",
            started_at=datetime.utcnow(),
        )
        db.add(job)
        db.commit()
        
        logger.info(f"Created scraping job {job.id} for {source_url}")
        return job.id


@celery_app.task(bind=True, name="scraping.run_job")
def run_scraping_job(self, job_id: int) -> int:
    """Run a scraping job.

    Args:
        job_id: ID of the job to run.

    Returns:
        ID of the completed job.
    """
    with db_session() as db:
        # Get job
        job = db.query(ScrapingJob).get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        # Update job status
        job.status = "running"
        db.commit()

        try:
            # Initialize scraper
            scraper = ApifyScraper(output_dir="data/raw")
            
            # Run scraping
            documents = scraper.scrape(job.source_url)
            
            # Save documents
            for doc in documents:
                document = Document(
                    url=doc.url,
                    title=doc.title,
                    content=doc.content,
                )
                db.add(document)
                job.documents.append(document)
            
            # Update job status
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Completed scraping job {job_id}")
            return job_id
        
        except Exception as e:
            # Update job status on error
            job.status = "failed"
            job.error = str(e)
            job.completed_at = datetime.utcnow()
            db.commit()
            
            logger.error(f"Failed scraping job {job_id}: {e}")
            raise


@celery_app.task(bind=True, name="scraping.process_job")
def process_job_results(self, job_id: int) -> int:
    """Process the results of a scraping job.

    Args:
        job_id: ID of the completed job.

    Returns:
        ID of the processed job.
    """
    with db_session() as db:
        # Get job
        job = db.query(ScrapingJob).get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        if job.status != "completed":
            raise ValueError(f"Job {job_id} is not completed")
        
        # TODO: Implement processing logic
        # This could include:
        # - Text cleaning and normalization
        # - Metadata extraction
        # - Document classification
        # - etc.
        
        logger.info(f"Processed results for job {job_id}")
        return job_id


def start_scraping_pipeline(source_url: str) -> chain:
    """Start the complete scraping pipeline.

    Args:
        source_url: URL to scrape.

    Returns:
        Celery chain of tasks.
    """
    return chain(
        start_scraping_job.s(source_url),
        run_scraping_job.s(),
        process_job_results.s(),
    )
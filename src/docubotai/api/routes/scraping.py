"""
Documentation scraping endpoints for DocuBotAI.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from sqlalchemy.orm import Session

from docubotai.core.database import get_db
from docubotai.models.database import ScrapingTask
from docubotai.tasks.scraping import start_scraping_task

router = APIRouter(prefix="/scraping", tags=["scraping"])

class ScrapingRequest(BaseModel):
    """Scraping request model."""
    url: HttpUrl
    max_depth: int = 2
    include_patterns: Optional[List[str]] = None
    exclude_patterns: Optional[List[str]] = None

class ScrapingTaskResponse(BaseModel):
    """Scraping task response model."""
    id: int
    url: str
    status: str
    progress: float
    error: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

@router.post("/", response_model=ScrapingTaskResponse)
async def create_scraping_task(
    request: ScrapingRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new scraping task."""
    task = ScrapingTask(
        url=str(request.url),
        max_depth=request.max_depth,
        include_patterns=request.include_patterns,
        exclude_patterns=request.exclude_patterns,
        status="pending"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    background_tasks.add_task(start_scraping_task, task.id)
    return task

@router.get("/tasks", response_model=List[ScrapingTaskResponse])
async def list_scraping_tasks(db: Session = Depends(get_db)):
    """List all scraping tasks."""
    return db.query(ScrapingTask).all()

@router.get("/tasks/{task_id}", response_model=ScrapingTaskResponse)
async def get_scraping_task(task_id: int, db: Session = Depends(get_db)):
    """Get scraping task status."""
    task = db.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}")
async def cancel_scraping_task(task_id: int, db: Session = Depends(get_db)):
    """Cancel a scraping task."""
    task = db.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="Task already finished")
    
    task.status = "cancelled"
    db.commit()
    return {"status": "success", "message": "Task cancelled"}
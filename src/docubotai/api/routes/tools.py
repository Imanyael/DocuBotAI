"""
Tool management endpoints for DocuBotAI.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from docubotai.core.database import get_db
from docubotai.models.database import Tool

router = APIRouter(prefix="/tools", tags=["tools"])

class ToolBase(BaseModel):
    """Base tool model."""
    name: str
    description: str
    url: str
    category: str

class ToolCreate(ToolBase):
    """Tool creation model."""
    pass

class ToolUpdate(ToolBase):
    """Tool update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None

class ToolResponse(ToolBase):
    """Tool response model."""
    id: int
    active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ToolResponse])
async def list_tools(db: Session = Depends(get_db)):
    """List all registered tools."""
    return db.query(Tool).all()

@router.post("/", response_model=ToolResponse)
async def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    """Register a new tool."""
    db_tool = Tool(**tool.model_dump())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.get("/{tool_id}", response_model=ToolResponse)
async def get_tool(tool_id: int, db: Session = Depends(get_db)):
    """Get tool details by ID."""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@router.put("/{tool_id}", response_model=ToolResponse)
async def update_tool(tool_id: int, tool: ToolUpdate, db: Session = Depends(get_db)):
    """Update tool details."""
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    for field, value in tool.model_dump(exclude_unset=True).items():
        setattr(db_tool, field, value)
    
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.delete("/{tool_id}")
async def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    """Delete a tool."""
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    db.delete(db_tool)
    db.commit()
    return {"status": "success", "message": "Tool deleted"}
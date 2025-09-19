"""
DocuBotAI Integration Example

This example demonstrates how to integrate DocuBotAI with:
- FastAPI web application
- Redis for caching
- PostgreSQL for storage
- Celery for background tasks
- WebSocket for real-time updates
"""

import asyncio
import json
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from celery import Celery
from redis import Redis
from pydantic import BaseModel

from docubotai import DocuBot
from docubotai.api import create_api_router
from docubotai.tools import GitHubTool, JiraTool
from docubotai.db import get_db, init_db
from docubotai.models import Query, Response, Document

# Initialize FastAPI app
app = FastAPI(title="DocuBotAI Integration Example")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis
redis = Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# Initialize Celery
celery = Celery(
    "docubotai",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Initialize DocuBot
bot = DocuBot(
    model="gpt-4",
    embedding_model="text-embedding-3-large",
    chunk_size=1000,
    chunk_overlap=200,
    tools=[
        GitHubTool(token="your-github-token"),
        JiraTool(url="your-jira-url", token="your-jira-token")
    ]
)

# Add standard API routes
app.include_router(
    create_api_router(bot),
    prefix="/api",
    tags=["standard"]
)

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# API Models
class QueryRequest(BaseModel):
    text: str
    context_size: int = 3
    temperature: float = 0.7
    stream: bool = False

class QueryResponse(BaseModel):
    id: str
    answer: str
    sources: List[dict]
    status: str

# Celery task for processing queries
@celery.task
def process_query(query_id: str, text: str, context_size: int, temperature: float):
    try:
        # Get response from DocuBot
        response = bot.query(
            text,
            context_size=context_size,
            temperature=temperature
        )
        
        # Store result in Redis
        result = {
            "id": query_id,
            "answer": response.answer,
            "sources": [
                {
                    "file": src.file,
                    "relevance": src.relevance,
                    "content": src.content
                }
                for src in response.sources
            ],
            "status": "completed"
        }
        redis.set(f"query:{query_id}", json.dumps(result))
        
        return result
    except Exception as e:
        # Store error in Redis
        error_result = {
            "id": query_id,
            "error": str(e),
            "status": "error"
        }
        redis.set(f"query:{query_id}", json.dumps(error_result))
        return error_result

# API endpoints
@app.post("/api/query", response_model=QueryResponse)
async def create_query(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    try:
        # Generate query ID
        query_id = f"query_{asyncio.get_event_loop().time()}"
        
        if request.stream:
            # Store initial status
            redis.set(
                f"query:{query_id}",
                json.dumps({
                    "id": query_id,
                    "status": "pending"
                })
            )
            
            # Start Celery task
            process_query.delay(
                query_id,
                request.text,
                request.context_size,
                request.temperature
            )
            
            return QueryResponse(
                id=query_id,
                answer="",
                sources=[],
                status="pending"
            )
        else:
            # Process query synchronously
            response = bot.query(
                request.text,
                context_size=request.context_size,
                temperature=request.temperature
            )
            
            return QueryResponse(
                id=query_id,
                answer=response.answer,
                sources=[
                    {
                        "file": src.file,
                        "relevance": src.relevance,
                        "content": src.content
                    }
                    for src in response.sources
                ],
                status="completed"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/query/{query_id}", response_model=QueryResponse)
async def get_query(query_id: str):
    try:
        # Get result from Redis
        result = redis.get(f"query:{query_id}")
        if not result:
            raise HTTPException(status_code=404, detail="Query not found")
        
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/query/{query_id}")
async def websocket_endpoint(websocket: WebSocket, query_id: str):
    await manager.connect(websocket)
    try:
        while True:
            # Get result from Redis
            result = redis.get(f"query:{query_id}")
            if result:
                result = json.loads(result)
                await websocket.send_json(result)
                
                # If query is completed or errored, close connection
                if result["status"] in ["completed", "error"]:
                    break
            
            # Wait before checking again
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Database initialization
@app.on_event("startup")
async def startup_event():
    init_db()

# Main function for testing
async def main():
    # Add documentation
    print("Adding documentation...")
    
    # Local files
    bot.add_document("../docs/api.md")
    bot.add_document("../docs/installation.md")
    
    # Test query
    print("\nTesting query...")
    response = await bot.aquery(
        "How do I deploy the application?",
        context_size=3,
        temperature=0.7
    )
    print(f"Answer: {response.answer}\n")
    
    # Test streaming
    print("Testing streaming...")
    async for chunk in bot.astream(
        "What are the scaling options?",
        context_size=3,
        temperature=0.7
    ):
        if chunk.type == "token":
            print(chunk.content, end="", flush=True)
        elif chunk.type == "source":
            print(f"\nSource: {chunk.file}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
"""
DocuBotAI Advanced Usage Example

This example demonstrates advanced features of DocuBotAI including:
- Custom preprocessing
- Custom embedding
- API integration
- Custom tools
- Advanced querying
"""

import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from docubotai import DocuBot, Preprocessor, EmbeddingProvider, Tool
from docubotai.api import create_api_router
from docubotai.tools import GitHubTool, JiraTool

# Custom preprocessor example
class CodePreprocessor(Preprocessor):
    def process(self, text: str) -> str:
        # Remove code comments
        lines = []
        in_multiline = False
        for line in text.split("\n"):
            if line.strip().startswith("/*"):
                in_multiline = True
                continue
            if in_multiline:
                if line.strip().endswith("*/"):
                    in_multiline = False
                continue
            if not line.strip().startswith("//"):
                lines.append(line)
        return "\n".join(lines)

# Custom embedding provider example
class FastEmbedding(EmbeddingProvider):
    def embed(self, text: str) -> List[float]:
        # Implement your custom embedding logic
        # This is a placeholder that returns random embeddings
        import numpy as np
        return list(np.random.rand(384))  # 384-dim embedding

# Custom tool example
class SearchTool(Tool):
    def execute(self, query: str) -> str:
        # Implement custom search logic
        return f"Search results for: {query}"

# API models
class Query(BaseModel):
    text: str
    context_size: int = 3
    temperature: float = 0.7

class Source(BaseModel):
    file: str
    relevance: float
    content: str

class Response(BaseModel):
    answer: str
    sources: List[Source]

# Create FastAPI application
app = FastAPI(title="DocuBotAI Advanced API")

# Initialize DocuBot with custom components
bot = DocuBot(
    model="gpt-4",
    embedding_model="text-embedding-3-large",
    chunk_size=1000,
    chunk_overlap=200,
    preprocessor=CodePreprocessor(),
    embedding_provider=FastEmbedding(),
    tools=[
        GitHubTool(token="your-github-token"),
        JiraTool(url="your-jira-url", token="your-jira-token"),
        SearchTool()
    ]
)

# Add standard API routes
app.include_router(
    create_api_router(bot),
    prefix="/api",
    tags=["standard"]
)

# Custom endpoints
@app.post("/api/custom/query", response_model=Response, tags=["custom"])
async def custom_query(query: Query):
    try:
        # Process query with custom logic
        response = await bot.aquery(
            query.text,
            context_size=query.context_size,
            temperature=query.temperature
        )
        
        # Transform response
        return Response(
            answer=response.answer,
            sources=[
                Source(
                    file=src.file,
                    relevance=src.relevance,
                    content=src.content
                )
                for src in response.sources
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/custom/stream")
async def stream_response(query: Query):
    try:
        # Stream response with custom logic
        async def generate():
            async for chunk in bot.astream(
                query.text,
                context_size=query.context_size,
                temperature=query.temperature
            ):
                if chunk.type == "token":
                    yield {"type": "token", "content": chunk.content}
                elif chunk.type == "source":
                    yield {"type": "source", "file": chunk.file}
        
        return generate()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def main():
    # Add documentation
    print("Adding documentation...")
    
    # Local markdown files
    bot.add_document("../docs/api.md")
    bot.add_document("../docs/installation.md")
    bot.add_document("../docs/deployment.md")
    
    # GitHub repository
    await bot.add_github_repo(
        "yourusername/DocuBotAI",
        branch="main",
        path="docs/"
    )
    
    # Advanced query example
    print("\nAdvanced query example:")
    response = await bot.aquery(
        "How do I implement custom preprocessing?",
        context_size=5,
        temperature=0.8,
        tools=["github", "search"]  # Use specific tools
    )
    print(f"Answer: {response.answer}\n")
    
    # Print sources with metadata
    print("Sources with metadata:")
    for source in response.sources:
        print(f"\nSource: {source.file}")
        print(f"Relevance: {source.relevance}")
        print(f"Content: {source.content}")
        print(f"Metadata: {source.metadata}")
    
    # Streaming with custom processing
    print("\nStreaming with custom processing:")
    print("Answer: ", end="", flush=True)
    
    async for chunk in bot.astream(
        "What are the best practices for deployment?",
        context_size=3,
        temperature=0.7
    ):
        if chunk.type == "token":
            # Custom token processing
            token = chunk.content.upper()
            print(token, end="", flush=True)
        elif chunk.type == "source":
            # Custom source handling
            print(f"\nREFERENCE: {chunk.file}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
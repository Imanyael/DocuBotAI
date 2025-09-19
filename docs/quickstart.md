# Quickstart Guide

This guide will help you get started with DocuBotAI quickly. We'll cover basic setup and common use cases.

## Installation

```bash
pip install docubotai
```

## Basic Usage

### 1. Initialize DocuBotAI

```python
from docubotai import DocuBot

# Initialize with default settings
bot = DocuBot()

# Or with custom configuration
bot = DocuBot(
    model="gpt-4",
    embedding_model="text-embedding-3-large",
    chunk_size=1000,
    chunk_overlap=200
)
```

### 2. Add Documentation

```python
# Add a single document
bot.add_document("path/to/docs/api.md")

# Add multiple documents
bot.add_documents([
    "path/to/docs/installation.md",
    "path/to/docs/deployment.md"
])

# Add from URL
bot.add_url("https://docs.example.com/api")

# Add from GitHub repository
bot.add_github_repo("username/repo", branch="main", path="docs/")
```

### 3. Query Documentation

```python
# Simple query
response = bot.query("How do I install the package?")
print(response.answer)

# Query with context
response = bot.query(
    "What are the deployment options?",
    context_size=3,  # Number of relevant chunks to include
    temperature=0.7  # Response creativity (0.0-1.0)
)

# Get sources
for source in response.sources:
    print(f"Source: {source.file}")
    print(f"Relevance: {source.relevance}")
    print(f"Content: {source.content}\n")
```

## Advanced Features

### 1. Custom Preprocessing

```python
from docubotai import Preprocessor

class MyPreprocessor(Preprocessor):
    def process(self, text: str) -> str:
        # Custom text processing logic
        text = text.replace("oldterm", "newterm")
        return text.strip()

bot = DocuBot(preprocessor=MyPreprocessor())
```

### 2. Custom Embedding

```python
from docubotai import EmbeddingProvider

class MyEmbedding(EmbeddingProvider):
    def embed(self, text: str) -> list[float]:
        # Custom embedding logic
        return your_embedding_model(text)

bot = DocuBot(embedding_provider=MyEmbedding())
```

### 3. Streaming Responses

```python
# Stream response tokens
for token in bot.stream("How do I deploy using Docker?"):
    print(token, end="", flush=True)

# Stream with source attribution
async for chunk in bot.astream("What are the scaling options?"):
    if chunk.type == "token":
        print(chunk.content, end="", flush=True)
    elif chunk.type == "source":
        print(f"\nSource: {chunk.file}")
```

### 4. API Integration

```python
from fastapi import FastAPI
from docubotai.api import create_api_router

app = FastAPI()
bot = DocuBot()

# Add DocuBotAI routes
api_router = create_api_router(bot)
app.include_router(api_router, prefix="/api")
```

### 5. Custom Tools

```python
from docubotai import Tool

class SearchTool(Tool):
    def execute(self, query: str) -> str:
        # Implement custom search logic
        results = your_search_function(query)
        return format_results(results)

bot = DocuBot(tools=[SearchTool()])
```

## Example Applications

### 1. Documentation Assistant

```python
from docubotai import DocuBot
from docubotai.tools import GitHubTool, JiraTool

# Create bot with tools
bot = DocuBot(tools=[
    GitHubTool(token="your-github-token"),
    JiraTool(url="your-jira-url", token="your-jira-token")
])

# Add documentation
bot.add_github_repo("your-org/your-repo")

# Create assistant
async def handle_question(question: str):
    # Query documentation
    response = await bot.aquery(question)
    
    # Check if we need to create issues
    if "bug" in question.lower():
        issue = await bot.tools["github"].create_issue(
            title=f"Bug Report: {question[:50]}",
            body=response.answer
        )
        return f"Created issue: {issue.url}\n\n{response.answer}"
    
    return response.answer
```

### 2. API Documentation Server

```python
from fastapi import FastAPI
from docubotai import DocuBot
from docubotai.api import create_api_router
from docubotai.tools import OpenAPITool

# Create application
app = FastAPI()

# Initialize bot with OpenAPI tool
bot = DocuBot(tools=[OpenAPITool()])

# Add API documentation
bot.add_openapi_spec("openapi.json")
bot.add_markdown_docs("docs/")

# Add bot routes
app.include_router(
    create_api_router(bot),
    prefix="/api/docs",
    tags=["documentation"]
)

# Add custom endpoint
@app.post("/api/docs/search")
async def search_docs(query: str):
    response = await bot.aquery(query)
    return {
        "answer": response.answer,
        "sources": [
            {
                "file": src.file,
                "relevance": src.relevance,
                "content": src.content
            }
            for src in response.sources
        ]
    }
```

### 3. CLI Tool

```python
import click
from docubotai import DocuBot

@click.group()
def cli():
    """DocuBotAI CLI"""
    pass

@cli.command()
@click.argument('query')
@click.option('--docs', '-d', multiple=True, help='Documentation files/folders')
def ask(query, docs):
    """Query documentation"""
    # Initialize bot
    bot = DocuBot()
    
    # Add documentation
    for doc in docs:
        bot.add_document(doc)
    
    # Get response
    response = bot.query(query)
    
    # Print answer
    click.echo(response.answer)
    
    # Print sources
    if click.confirm('Show sources?'):
        for src in response.sources:
            click.echo(f"\nSource: {src.file}")
            click.echo(f"Content: {src.content}")

if __name__ == '__main__':
    cli()
```

## Best Practices

1. **Document Processing**
   - Use appropriate chunk sizes (500-1500 tokens)
   - Enable chunk overlap (10-20% of chunk size)
   - Preprocess documents to remove noise

2. **Query Optimization**
   - Be specific in queries
   - Use appropriate temperature settings
   - Leverage context size for accuracy

3. **Performance**
   - Cache embeddings
   - Use batch processing for large documents
   - Stream responses for better UX

4. **Integration**
   - Use async methods for web applications
   - Implement proper error handling
   - Set up monitoring and logging

## Next Steps

- Read the [full documentation](https://docs.docubotai.com)
- Join our [Discord community](https://discord.gg/docubotai)
- Contribute on [GitHub](https://github.com/yourusername/DocuBotAI)
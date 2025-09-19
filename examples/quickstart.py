"""
DocuBotAI Quickstart Example

This example demonstrates basic usage of DocuBotAI for documentation management
and querying. It covers initialization, adding documents, and querying.
"""

import asyncio
from docubotai import DocuBot
from docubotai.tools import GitHubTool

async def main():
    # Initialize DocuBot with custom settings
    bot = DocuBot(
        model="gpt-4",
        embedding_model="text-embedding-3-large",
        chunk_size=1000,
        chunk_overlap=200,
        tools=[GitHubTool(token="your-github-token")]
    )

    # Add documentation from different sources
    print("Adding documentation...")
    
    # Local files
    bot.add_document("../docs/api.md")
    bot.add_document("../docs/installation.md")
    
    # GitHub repository
    await bot.add_github_repo(
        "yourusername/DocuBotAI",
        branch="main",
        path="docs/"
    )
    
    # Web URL
    bot.add_url("https://docs.example.com/api")

    # Simple query
    print("\nBasic query example:")
    response = bot.query("How do I install the package?")
    print(f"Answer: {response.answer}\n")
    print("Sources:")
    for source in response.sources:
        print(f"- {source.file} (relevance: {source.relevance})")

    # Query with context
    print("\nQuery with context example:")
    response = bot.query(
        "What are the deployment options?",
        context_size=3,
        temperature=0.7
    )
    print(f"Answer: {response.answer}\n")
    print("Sources with content:")
    for source in response.sources:
        print(f"\nSource: {source.file}")
        print(f"Relevance: {source.relevance}")
        print(f"Content: {source.content}")

    # Streaming example
    print("\nStreaming example:")
    print("Answer: ", end="", flush=True)
    async for chunk in bot.astream("How do I deploy using Docker?"):
        if chunk.type == "token":
            print(chunk.content, end="", flush=True)
        elif chunk.type == "source":
            print(f"\nSource: {chunk.file}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
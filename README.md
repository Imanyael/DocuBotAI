# DocuBotAI

DocuBotAI is an intelligent documentation agent that automatically scrapes your entire toolstack using Apify, processes the documentation through Claude API, and creates a RAG (Retrieval-Augmented Generation) system. This enables coding agents to utilize your tools to their full potential.

## Features

- 🔍 Automated documentation scraping with Apify
- 🤖 Advanced processing using Claude API
- 📚 RAG system for intelligent documentation retrieval
- 🛠️ Full toolstack integration
- 🔄 Real-time documentation updates

## Prerequisites

- Python 3.9+
- Docker (optional)
- Apify API key
- Claude API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Imanyael/DocuBotAI.git
cd DocuBotAI
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Usage

1. Start the documentation scraping:
```bash
docubot scrape --source <documentation-url>
```

2. Process documentation:
```bash
docubot process
```

3. Run the RAG system:
```bash
docubot serve
```

## Project Structure

```
DocuBotAI/
├── docubot/
│   ├── api/           # API endpoints
│   ├── cli/           # Command line interface
│   ├── core/          # Core functionality
│   ├── models/        # Data models
│   ├── scrapers/      # Documentation scrapers
│   ├── rag/           # RAG system implementation
│   └── utils/         # Utility functions
├── tests/             # Test suite
├── docs/              # Documentation
└── examples/          # Usage examples
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# DocuBot AI

An intelligent document processing and chat interface powered by AI.

## Features

- Interactive document chat interface
- Real-time document processing
- Advanced RAG implementation
- Secure API integration
- Modern, responsive UI
- Multi-document support
- Custom document workflows

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DocuBotAI.git
cd DocuBotAI
```

2. Install dependencies:
```bash
# Frontend
cd frontend
npm install

# Backend (in a new terminal)
pip install -e ".[dev]"
```

3. Start development servers:
```bash
# Frontend
npm run dev

# Backend
uvicorn docubotai.api.main:app --reload
```

4. Open http://localhost:5173 in your browser

## Production Deployment

### Prerequisites

1. AWS Account with:
   - ECR (Elastic Container Registry)
   - ECS (Elastic Container Service)
   - CloudFront
   - Route 53
   - ACM (AWS Certificate Manager)

2. GitHub repository secrets configured for CI/CD

### Deployment Steps

1. Push to main branch to trigger deployment
2. Monitor deployment in GitHub Actions
3. Access the application at https://app.docubotai.com

For detailed deployment instructions, see [Deployment Guide](docs/deployment.md)

## Development

### Frontend

- React with TypeScript
- Vite for building
- Tailwind CSS for styling
- Radix UI components
- Real-time updates with WebSocket

### Backend

- FastAPI
- SQLAlchemy
- Alembic migrations
- Celery for tasks
- RAG implementation
- Document processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

See [Contributing Guide](CONTRIBUTING.md) for details.

## Security

- HTTPS everywhere
- Content Security Policy
- Rate limiting
- DDoS protection
- Input validation
- Secure headers

Report security issues to security@docubotai.com

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Support

- Documentation: https://docs.docubotai.com
- Issues: https://github.com/yourusername/DocuBotAI/issues
- Email: support@docubotai.com

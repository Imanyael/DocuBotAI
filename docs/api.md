# API Documentation

## Authentication

Most endpoints are public, but admin endpoints require API key authentication using the `X-API-Key` header.

## Endpoints

### Tools API

#### List Tools
```http
GET /tools/
```
Lists all registered tools.

#### Create Tool
```http
POST /tools/
```
Register a new tool.

Request body:
```json
{
    "name": "string",
    "description": "string",
    "url": "string",
    "category": "string"
}
```

#### Get Tool
```http
GET /tools/{tool_id}
```
Get tool details by ID.

#### Update Tool
```http
PUT /tools/{tool_id}
```
Update tool details.

Request body:
```json
{
    "name": "string",
    "description": "string",
    "url": "string",
    "category": "string"
}
```

#### Delete Tool
```http
DELETE /tools/{tool_id}
```
Delete a tool.

### Scraping API

#### Create Scraping Task
```http
POST /scraping/
```
Create a new scraping task.

Request body:
```json
{
    "url": "string",
    "max_depth": 2,
    "include_patterns": ["string"],
    "exclude_patterns": ["string"]
}
```

#### List Tasks
```http
GET /scraping/tasks/
```
List all scraping tasks.

#### Get Task Status
```http
GET /scraping/tasks/{task_id}
```
Get scraping task status.

#### Cancel Task
```http
DELETE /scraping/tasks/{task_id}
```
Cancel a scraping task.

### Query API

#### Query Documents
```http
POST /query/
```
Query the RAG system.

Request body:
```json
{
    "text": "string",
    "context": "string",
    "max_results": 5,
    "min_similarity": 0.7
}
```

Response:
```json
{
    "answer": "string",
    "sources": [
        {
            "url": "string",
            "title": "string",
            "relevance": 0.95
        }
    ],
    "confidence": 0.9,
    "execution_time": 0.5
}
```

#### Get Query History
```http
GET /query/history
```
Get recent query history.

#### Clear History
```http
DELETE /query/history
```
Clear query history.

### Admin API

All admin endpoints require the `X-API-Key` header.

#### System Status
```http
GET /admin/status
```
Get system status metrics.

Response:
```json
{
    "cpu_usage": 0.0,
    "memory_usage": 0.0,
    "disk_usage": 0.0,
    "active_tasks": 0,
    "queue_size": 0,
    "uptime": 0.0
}
```

#### Maintenance Mode
```http
POST /admin/maintenance
```
Enable/disable maintenance mode.

Request body:
```json
{
    "enabled": true,
    "message": "System is under maintenance"
}
```

#### Reload Configuration
```http
POST /admin/reload-config
```
Reload system configuration.

#### System Logs
```http
GET /admin/logs
```
Get system logs.

Query parameters:
- `limit`: Maximum number of logs (default: 100)
- `level`: Log level filter (default: "ERROR")

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
- 503: Service Unavailable (Maintenance Mode)

Error response format:
```json
{
    "detail": "Error message"
}
```

## Rate Limiting

- Public endpoints: 100 requests per minute
- Admin endpoints: 1000 requests per minute
- Scraping endpoints: 10 requests per minute

## Websocket Support

Real-time updates for scraping tasks and system metrics are available through WebSocket connections:

```javascript
ws://localhost:8000/ws/tasks/{task_id}
ws://localhost:8000/ws/metrics
```
# DietLogApp - Food Image Analysis API

DietLogApp is a FastAPI-based application that analyzes food images and provides nutritional feedback using AI models.

## Running with Docker

### Prerequisites

- Docker installed

### Environment Variables

The following environment variables must be configured:

- `ANTHROPIC_API_KEY`: token to interact with the LLM

### Quick Start

1. Build the Docker image:

```bash
docker build -t dietlogapp .
```

2. Run the container:

```bash
docker run -d --name dietlogapp -p 8000:8000 --env-file .env dietlogapp
```

3. Access the application:

- API Docs: http://localhost:8000/docs
- Web Interface: http://localhost:8000/static/index.html

### Stopping the Container

To stop the running container:

```bash
docker stop dietlogapp
```

To remove the container:

```bash
docker rm dietlogapp
```

### Viewing Logs

To view the application logs:

```bash
docker logs -f dietlogapp
```

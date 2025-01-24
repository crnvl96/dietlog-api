## Goal

- This project is an API for a frontend application that processes a JSON request containing an image URL and a description.
- It uses LangChain, powered by an AI model, to process the image and description and outputs a response to the frontend.
- The API is documented using Swagger and is containerized using Docker for easy deployment.

## Project Structure

```terminal
app/
├── main.py          # Entry point (minimal setup)
├── core/            # Configurations and shared components
│   └── config.py    # App configuration/settings
├── models/          # Database models (if added later)
├── schemas/         # Pydantic models (request/response schemas)
│   └── diet.py      # Diet-related schemas
├── api/             # API endpoints
│   ├── deps.py      # Dependency injections
│   └── endpoints/   # Route handlers
│       └── diet.py  # Diet-related routes
├── services/        # Business logic layer
│   └── diet.py      # Diet-related services
└── tests/           # Test suite
    └── test_api.py  # API endpoint tests
```

## Docker Setup

### Prerequisites

- Docker
- Docker Compose

### Building Images

```bash
docker-compose build
```

### Running Development Server

```bash
docker-compose up dev --watch
```

The development server will be available at `http://localhost:8000`

### Running Tests

```bash
docker-compose run test
```

### Development Workflow

- Changes to `pyproject.toml` will trigger a rebuild
- File changes are synced to the container in real-time

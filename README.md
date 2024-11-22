# Image Processing API

## Technologies Used

- Python 3.11+
- FastAPI for REST API
- SQLAlchemy for database ORM
- PostgreSQL for data storage
- NumPy and Pandas for data processing
- Matplotlib for Image normalization and color map
- Docker and Docker Compose for containerization
- Poetry for dependency management
- Pytest for testing
- Logging with Python's built-in logging module with multiple handlers

## Project Structure

```
├── src/                   # Source code
│   ├── api/               # API layer
│   ├── config/            # Configuration DB, Logging
│   ├── domain/            # Domain entities and interfaces
│   ├── infrastructure/    # Implementation of interfaces
│   └── core/              # Core utilities
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── data/                  # img.csv
└── docker/                # Docker configuration
```

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:MirzaBaig715/Image-Processor-FastAPI.git
   cd Image-Processor-FastAPI
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Create .env file in root folder:
   ```bash
   cp .env.example .env
   ```

## Running the Application

1. Build and Start the PostgreSQL database:
   ```bash
   docker-compose up -d db
   ```

2. Build and start all other services:
   ```bash
   docker-compose up --build
   ```

3. Populate initial data in Database:
   ```bash
   docker-compose exec api python /app/scripts/process_initial_data.py
   ```

## API Documentation

Once the application is running, access the API documentation at:
- ReDoc: http://localhost:8000/redoc
- Swagger UI: http://localhost:8000/docs

## Main Endpoints

### Retrieve Image Frames by Depth
- **POST** `/api/v1/frames/by-depth`
  ```json
  {
    "depth_min": 9000,
    "depth_max": 9000.3
  }
  ```

### Retrieve Frame by ID
- **GET** `/api/v1/frames/{frame_id}`

## Environment Configuration

The application supports three environments:
- Local development
- Development
- Production

Environment-specific settings are managed in `src/config/settings.py`

## Deployment

### Azure
- Azure DevOps with Azure Container Service + Webapp with Container

### AWS
- Elastic Container Service with Fargate
# Organization API

A FastAPI-based REST API for managing organizations and admin authentication with MongoDB backend.

## Features

- 🏢 **Organization Management**: Create and retrieve organizations
- 🔐 **Admin Authentication**: JWT-based authentication system
- 🍃 **MongoDB Integration**: Async MongoDB operations with Motor
- 🚀 **FastAPI**: Modern, fast web framework with automatic API documentation
- 📝 **Auto-generated Documentation**: Interactive API docs with Swagger UI
- 🔒 **Security**: Bcrypt password hashing and JWT tokens
- 🧪 **Testing**: Comprehensive Postman collection included

## Tech Stack

- **FastAPI** 0.111.0 - Modern Python web framework
- **Motor** 3.3.2 - Async MongoDB driver (compatible version)
- **PyMongo** 4.6.3 - MongoDB driver for Python
- **Pydantic** v2 - Data validation and settings
- **Pydantic-Settings** 2.2.1 - Configuration management
- **Python-JOSE** - JWT token handling
- **Passlib** with bcrypt - Password hashing
- **Python-Slugify** - URL-friendly slug generation

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration settings
│   │   ├── database.py            # MongoDB connection
│   │   └── security.py            # Authentication utilities
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── organization.py        # Organization models
│   │   ├── token.py               # Authentication models
│   │   └── user.py                # User models
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── organization.py        # Organization database operations
│   │   └── user.py                # User database operations
│   └── api/
│       ├── __init__.py
│       ├── deps.py                # Dependency injection
│       └── v1/
│           ├── __init__.py
│           ├── router.py          # API router
│           └── endpoints/
│               ├── __init__.py
│               ├── auth.py        # Authentication endpoints
│               └── organization.py # Organization endpoints
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
└── Organization_API.postman_collection.json  # Postman testing collection
```

## Quick Start

### Prerequisites

- Python 3.10+
- MongoDB 4.4+
- pip or poetry

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd organization-api
   ```

2. **Create virtual environment**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (Optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (optional - has defaults)
   ```

5. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Docker Deployment (Recommended)

The easiest way to run the application is using Docker:

```bash
# Clone and navigate to the project
git clone <repository-url>
cd organization-api

# Run with Docker Compose (includes MongoDB)
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

This will start:
- **API Server**: `http://localhost:8000`
- **MongoDB**: `localhost:27017`
- **API Documentation**: `http://localhost:8000/docs`

## Environment Configuration

The application includes fallback defaults for all configuration values, so it can run without a `.env` file. However, for production use, create a `.env` file with:

```bash
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=org_service
JWT_SECRET_KEY=your-secret-key-here-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

**Note:** The JWT secret key should be at least 32 characters long for security.

## API Endpoints

### Organizations

- `POST /api/v1/org/create` - Create a new organization
- `GET /api/v1/org/get` - Get organization by name

### Authentication

- `POST /api/v1/admin/login` - Admin login

### Health Check

- `GET /` - API health check

## API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Database Schema

### Collections

- **ORG**: Master organization records
  ```json
  {
    "_id": "ObjectId",
    "name": "Organization Name",
    "slug": "organization-name",
    "admin_email": "admin@example.com",
    "created_at": "2024-01-01T00:00:00Z"
  }
  ```

- **{slug}_admins**: Organization-specific admin collections
  ```json
  {
    "_id": "ObjectId",
    "email": "admin@example.com",
    "hashed_password": "$2b$12$..."
  }
  ```

## Testing

### Using Postman

1. Import `Organization_API.postman_collection.json` into Postman
2. Set up environment variables
3. Run the collection to test all endpoints

### Example Usage

1. **Create Organization**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/org/create" \
        -H "Content-Type: application/json" \
        -d '{
          "organization_name": "Acme Corp",
          "email": "admin@acme.com",
          "password": "securepassword"
        }'
   ```

2. **Get Organization**
   ```bash
   curl "http://localhost:8000/api/v1/org/get?organization_name=Acme Corp"
   ```

3. **Admin Login**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/admin/login" \
        -H "Content-Type: application/json" \
        -d '{
          "admin": "admin@acme.com",
          "password": "securepassword"
        }'
   ```

## Development

### Running in Development Mode

**Option 1: Local Python (requires MongoDB separately)**
```bash
# Install MongoDB locally first
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 2: Docker Development (recommended)**
```bash
docker-compose up --build
```

### Stopping Services

```bash
# Stop Docker services
docker-compose down

# Stop and remove volumes (removes database data)
docker-compose down -v
```

### Viewing Logs

```bash
# View API logs
docker-compose logs api

# View MongoDB logs
docker-compose logs mongodb

# Follow logs in real-time
docker-compose logs -f api
```








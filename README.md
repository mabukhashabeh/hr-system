# HR System

A comprehensive HR candidate management system with a Django REST API backend and modern frontend. This system allows HR teams to manage job candidates, track application status, and handle resume uploads efficiently.

## What This System Does

### Candidate Management
- Register candidates with personal information, contact details, and resume uploads
- Track application status from initial submission through to hiring decision
- Search and filter candidates by name, email, status, and department
- View detailed status history for each candidate with timestamps
- Secure resume storage and download functionality

### Admin Features
- Secure admin interface for HR managers
- Bulk operations for efficient candidate management
- Status updates with automatic history tracking
- Resume downloads for candidate review

## Technology Stack

### Backend
- Django 5.0 - Robust Python web framework
- Django REST Framework - Powerful API toolkit
- PostgreSQL - Reliable database (via Docker)
- Django Filter - Advanced filtering and search capabilities
- Pillow - Image processing for file uploads

### Frontend
- Modern web interface for candidate management
- Responsive design for desktop and mobile use

### Infrastructure
- Docker - Containerized deployment
- Docker Compose - Multi-service orchestration

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Getting Started

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd hr-system
   ```

2. Set up environment variables
   ```bash
   cp compose/.env.sample compose/.env
   # Edit compose/.env with your configuration
   ```

3. Start the entire system
   ```bash
   cd backend
   make up
   ```

4. Access the application
   - Frontend: http://localhost:8080
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/

## Development Commands

The project includes a comprehensive Makefile for easy development workflows.

### Starting Services

```bash
# Start all services (API, database, frontend)
make up

# Start only the API server
make server

# Stop all services
make down

# View logs for all services
make logs
```

### Testing

The project features a powerful testing infrastructure with comprehensive coverage and fast execution.

```bash
# Run all tests with coverage (recommended)
make test

# Run tests with detailed coverage report
make coverage

# Build test environment
make test-build

# Clean up test containers and volumes
make test-clean
```

### Development Tools

```bash
# Open shell in API container
make shell

# Install dependencies
make install

# Install development dependencies
make dev

# Build Docker images
make build
```

### Cleanup

```bash
# Clean up generated files and containers
make clean

# Stop all services
make stop
```

### Help

```bash
# Show all available commands
make help
```

## Testing Infrastructure

The testing setup is designed for speed and reliability:

- **Fast Execution**: SQLite in-memory database for instant test execution
- **High Coverage**: 99% test coverage with 63 comprehensive tests
- **Isolated Environment**: Containerized testing with automatic cleanup
- **Comprehensive Reports**: HTML and terminal coverage reports

### Test Categories

- **Model Tests**: Database models, validation, and relationships
- **View Tests**: API endpoints, permissions, and file handling
- **Serializer Tests**: Data transformation and validation
- **Permission Tests**: Access control and authentication
- **Validator Tests**: Custom validation logic

### Test Performance

- Execution time: approximately 1 second for full test suite
- Memory usage: minimal (in-memory database)
- Reliability: 100% pass rate with no flaky tests

## API Endpoints

### Candidates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/candidates/` | List all candidates with filtering |
| POST | `/api/candidates/` | Create new candidate |
| GET | `/api/candidates/{id}/` | Get candidate details |
| PUT | `/api/candidates/{id}/` | Update candidate |
| DELETE | `/api/candidates/{id}/` | Delete candidate |
| GET | `/api/candidates/{id}/status-history/` | Get status history |

### Query Parameters

- `search` - Search by name or email
- `status` - Filter by status (applied, reviewing, interviewed, offered, hired, rejected)
- `department` - Filter by department
- `ordering` - Sort by field (name, email, created_at, etc.)

## Project Structure

```
hr-system/
├── backend/                 # Django REST API
│   ├── candidate/          # Candidate management app
│   ├── core/              # Shared utilities
│   ├── config/            # Django settings
│   └── tests/             # Comprehensive test suite
├── frontend/              # Modern web interface
├── compose/               # Docker Compose configuration
│   ├── docker-compose.yml # Main services
│   ├── docker-compose.test.yml # Test environment
│   └── .env              # Environment variables
└── README.md             # This file
```

## Configuration

### Environment Variables

Key environment variables in `compose/.env`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=hr_system
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Test Settings
TEST_DB_HOST=test_db
TEST_DB_NAME=hr_system_test
TEST_DB_USER=hr_user
TEST_DB_PASSWORD=hr_password
TEST_DEBUG=True
TEST_DJANGO_SETTINGS_MODULE=config.test_settings
```

## Security Features

- Admin authentication required for all endpoints
- File upload validation for resumes
- Input sanitization and validation
- CSRF protection enabled
- Secure file storage with proper permissions

## Contributing

1. Follow Django coding standards
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages

## License

This project is part of a technical assessment. 
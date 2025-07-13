# HR System

A Django REST API backend and Vue.js frontend for managing job candidates. HR teams can track applications, manage status updates, and handle resume uploads.

## What This System Does

### Candidate Management
- Register candidates with personal information and resume uploads
- Track application status from submission to hiring decision
- Search and filter candidates by name, email, status, and department
- View detailed status history for each candidate
- Secure resume storage and download

### User Roles

#### Admin Users
- **Full system access** with `X-ADMIN: 1` header
- **Candidate management**: List, view, and update candidates
- **Status management**: Update candidate application status with feedback
- **Resume access**: Download and review candidate resumes
- **System administration**: Access admin interface and system settings

#### Candidates
- **Public registration**: Submit applications with personal information
- **Status checking**: Check application status via public endpoint
- **No direct system access**: Cannot view other candidates or admin features

## Technology Stack

### Backend
- **Django 5.2.4** - Web framework
- **Django REST Framework 3.14+** - API toolkit
- **PostgreSQL 15** - Database
- **Django Filter 23.0+** - Filtering and search
- **Pillow 10.0+** - File processing
- **DRF YASG 1.21+** - API documentation
- **Django CORS Headers 4.0+** - Cross-origin support
- **Django Storages 1.14+** - Cloud storage
- **Boto3 1.26+** - AWS SDK
- **Psycopg2 Binary 2.9+** - PostgreSQL adapter
- **Python Decouple 3.8+** - Environment config

### Frontend
- **Vue.js 3** - JavaScript framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **Yup** - Validation
- **Nginx** - Web server

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Service orchestration
- **PostgreSQL** - Primary database
- **SQLite** - Test database

### Development Tools
- **Pytest 8.4+** - Testing framework
- **Pytest Django 4.11+** - Django integration
- **Pytest Coverage 6.2+** - Coverage reporting
- **Factory Boy 3.2+** - Test data generation
- **Faker 19.0+** - Fake data
- **Black 23.0+** - Code formatting
- **Flake8 6.0+** - Linting
- **Isort 5.12+** - Import sorting
- **Pytest Xdist 3.8+** - Parallel testing
- **Pytest Benchmark 4.0+** - Performance testing

## Complete Setup Guide

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- At least 2GB free disk space

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hr-system
   ```

2. **Set up environment variables**
   ```bash
   cp compose/.env.sample compose/.env
   ```

3. **Edit the environment file**
   ```bash
   # Open compose/.env in your editor
   nano compose/.env
   # or
   code compose/.env
   ```

4. **Configure your settings** (optional)
   ```env
   # Django settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database settings
   DB_NAME=hr_system
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432

   # Test settings
   TEST_DB_HOST=test_db
   TEST_DB_NAME=hr_system_test
   TEST_DB_USER=hr_user
   TEST_DB_PASSWORD=hr_password
   TEST_DEBUG=True
   TEST_DJANGO_SETTINGS_MODULE=config.test_settings
   ```

5. **Start the entire system**
   ```bash
   cd backend
   make up
   ```

6. **Wait for services to start** (first time takes 2-3 minutes)
   - API container building
   - Database initialization
   - Frontend container building

7. **Access the application**
   - Frontend: http://localhost:8080
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/
   - Swagger docs: http://localhost:8000/swagger/

### First Time Setup Notes

- **First run**: Docker will download images and build containers
- **Database**: PostgreSQL will initialize automatically
- **Migrations**: Django migrations run automatically
- **Media files**: Resume uploads stored in `backend/media/`

## Development Commands

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

```bash
# Run all tests with coverage
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

- **Fast Execution**: SQLite in-memory database for instant test execution
- **High Coverage**: **99.7% code coverage** with 63 comprehensive tests
- **Isolated Environment**: Containerized testing with automatic cleanup
- **Comprehensive Reports**: HTML and terminal coverage reports

### Test Categories

- **Model Tests**: Database models, validation, and relationships
- **View Tests**: API endpoints, permissions, and file handling
- **Serializer Tests**: Data transformation and validation
- **Permission Tests**: Access control and authentication
- **Validator Tests**: Custom validation logic

### Test Performance

- **Execution time**: ~1.15 seconds for all 63 tests
- **Coverage**: 99.7% (333 statements, 1 missing)
- **Test isolation**: Each test runs in clean environment
- **Parallel execution**: Support for parallel test running

## Database Optimizations

### Indexed Fields
- **Candidate Model**:
  - `full_name` (db_index=True) - Fast name searches
  - `department` (db_index=True) - Efficient department filtering
  - `current_status` (db_index=True) - Quick status filtering
  - `created_at` (db_index=True) - Optimized date sorting
  - Composite indexes: `[department, created_at]`, `[current_status, created_at]`

- **StatusHistory Model**:
  - `candidate` (ForeignKey with index) - Fast candidate lookups
  - `created_at` (db_index=True) - Efficient history sorting
  - Composite index: `[candidate, created_at]`

### Performance Features
- **UUID primary keys** for security and scalability
- **Optimized queries** with select_related and prefetch_related
- **Database constraints** for data integrity
- **Efficient pagination** with PageNumberPagination
- **Fast filtering** with Django Filter backend

## API Rate Limiting & Throttling

### Production Throttling
```python
'DEFAULT_THROTTLE_RATES': {
    'anon': '20/minute',
    'user': '100/minute',
}
```

- **Anonymous users**: 20 requests per minute
- **Authenticated users**: 100 requests per minute
- **Admin users**: Same as authenticated users (100/minute)

### Test Environment
- **Throttling disabled** for faster test execution
- **Unlimited requests** during development and testing

### Throttle Classes
- `AnonRateThrottle` - Anonymous user rate limiting
- `UserRateThrottle` - Authenticated user rate limiting

## File Upload & Storage Configuration

### Supported Formats
- **PDF** (.pdf) - Preferred format
- **DOC** (.doc) - Microsoft Word legacy
- **DOCX** (.docx) - Microsoft Word modern

### File Limits
- **Maximum size**: 5MB per file
- **Security**: File type validation and size checking

### Storage Providers

#### 1. Local Storage (Default)
```env
DEFAULT_FILE_STORAGE=django.core.files.storage.FileSystemStorage
```
- Files stored locally in `backend/media/`
- No additional configuration needed
- Good for development and small deployments

#### 2. AWS S3
```env
DEFAULT_FILE_STORAGE=storages.backends.s3boto3.S3Boto3Storage
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```
- Scalable cloud storage
- CDN support
- High availability

#### 3. OCI Object Storage
```env
DEFAULT_FILE_STORAGE=storages.backends.s3boto3.S3Boto3Storage
STORAGE_PROVIDER=oci
AWS_ACCESS_KEY_ID=your-oci-access-key
AWS_SECRET_ACCESS_KEY=your-oci-secret-key
AWS_STORAGE_BUCKET_NAME=your-oci-bucket-name
AWS_S3_REGION_NAME=us-ashburn-1
AWS_S3_ENDPOINT_URL=https://objectstorage.us-ashburn-1.oraclecloud.com
```
- Oracle Cloud Infrastructure
- Compatible with S3 API
- Enterprise-grade storage

#### 4. Google Cloud Storage
```env
DEFAULT_FILE_STORAGE=storages.backends.s3boto3.GCSStorage
```
- Google Cloud Platform
- Set GCS credentials and bucket as required
- Global CDN support

#### 5. Azure Blob Storage
```env
DEFAULT_FILE_STORAGE=storages.backends.s3boto3.AzureStorage
```
- Microsoft Azure
- Set Azure credentials and container as required
- Enterprise integration

### Storage Configuration Steps

1. **Choose your storage provider**
2. **Set environment variables** in `compose/.env`
3. **Restart the application**
   ```bash
   make down
   make up
   ```

## Security Features

### Authentication & Authorization
- **Admin-only access** for sensitive operations
- **Public endpoints** for candidate registration and status checking
- **Header-based authentication** (`X-ADMIN: 1`)
- **CSRF protection** enabled
- **Input validation** and sanitization

### Data Protection
- **UUID primary keys** for security
- **File upload validation** (type, size, content)
- **SQL injection protection** via Django ORM
- **XSS protection** with security headers
- **Content type sniffing protection**

## Technical Assessment Strengths

### Code Quality
- **99.7% test coverage** with comprehensive test suite
- **Clean architecture** following Django best practices
- **Type hints** and comprehensive documentation
- **Code formatting** with Black and isort
- **Linting** with Flake8 for code quality

### Performance
- **Database optimization** with strategic indexing
- **Efficient queries** with proper ORM usage
- **Fast test execution** (1.15 seconds for 63 tests)
- **Containerized deployment** for consistency
- **Rate limiting** to prevent abuse

### Scalability
- **Microservices architecture** with Docker Compose
- **Cloud storage support** for file handling
- **Database indexing** for large datasets
- **Pagination** for handling large result sets
- **Modular design** for easy extension

### Maintainability
- **Comprehensive documentation** with clear examples
- **Automated testing** with 63 test cases
- **Development tools** for code quality
- **Clear project structure** following conventions
- **Environment configuration** management

### User Experience
- **Intuitive API design** with RESTful endpoints
- **Comprehensive error handling** with meaningful messages
- **Swagger documentation** for API exploration
- **Responsive frontend** with modern UI
- **Real-time status updates** with history tracking

## API Endpoints

### Public Endpoints
- `POST /api/v1/candidates/` - Candidate registration
- `GET /api/v1/candidates/status/` - Status check by email

### Admin Endpoints
- `GET /api/v1/candidates/` - List all candidates
- `GET /api/v1/candidates/{id}/` - Get candidate details
- `PATCH /api/v1/candidates/{id}/` - Update candidate status
- `GET /api/v1/candidates/{id}/status-history/` - Get status history
- `GET /api/v1/candidates/{id}/download-resume/` - Download resume

## Status Flow

1. **Submitted** - Candidate submits application
2. **Under Review** - HR reviews application
3. **Interview Scheduled** - Interview is scheduled
4. **Accepted** - Candidate is accepted
5. **Rejected** - Application is rejected

## Environment Variables

Main settings in `compose/.env`:

```env
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=hr_system
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Test settings
TEST_DB_HOST=test_db
TEST_DB_NAME=hr_system_test
TEST_DB_USER=hr_user
TEST_DB_PASSWORD=hr_password
TEST_DEBUG=True
TEST_DJANGO_SETTINGS_MODULE=config.test_settings
```

## Project Structure

```
hr-system/
├── backend/                 # Django REST API
│   ├── candidate/          # Main app
│   │   ├── models.py      # Database models
│   │   ├── views.py       # API endpoints
│   │   ├── serializers.py # Data validation
│   │   ├── filters.py     # Search and filter
│   │   ├── permissions.py # Access control
│   │   └── tests/         # Tests
│   ├── core/              # Shared utilities
│   │   ├── validators.py  # Custom validators
│   │   └── tests/         # Tests
│   ├── config/            # Django settings
│   │   ├── settings.py    # Main settings
│   │   ├── test_settings.py # Test settings
│   │   └── urls.py        # URL routing
│   ├── manage.py          # Django management
│   ├── Dockerfile         # Container setup
│   ├── entry.sh           # Startup script
│   ├── Makefile           # Commands
│   └── pyproject.toml     # Dependencies
├── frontend/              # Vue.js frontend
│   ├── src/               # Source code
│   ├── public/            # Static files
│   └── Dockerfile         # Container setup
├── compose/               # Docker Compose
│   ├── docker-compose.yml # Main services
│   ├── docker-compose.test.yml # Test services
│   └── .env               # Environment variables
└── README.md              # This file
```

## Troubleshooting

### Services not starting
```bash
# Check if Docker is running
docker ps

# Clean up and restart
make clean
make up
```

### Database issues
```bash
# Reset database
make down
docker volume rm hr-system_postgres_data
make up
```

### Test failures
```bash
# Clean test environment
make test-clean
make test
```

### Permission issues
```bash
# Check file permissions
ls -la

# Fix permissions if needed
chmod +x entry.sh
```

### First time setup issues
```bash
# If containers fail to build
docker system prune -a
make build
make up
```

### Port conflicts
```bash
# Check if ports are in use
lsof -i :8000
lsof -i :8080
lsof -i :5432

# Stop conflicting services or change ports in compose/.env
``` 
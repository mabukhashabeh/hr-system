# Backend API

A Django REST API for managing job candidates. This handles all the data, business logic, and provides endpoints for the frontend.

## What it does

- Store candidate information (name, email, phone, resume)
- Track application status (applied, reviewing, interviewed, hired, etc.)
- Handle file uploads (resumes)
- Provide search and filtering
- Manage user permissions
- Generate status history
- Send email notifications asynchronously
- Process background tasks with Celery

## User Roles

### Admin Users
- **Full system access** with `X-ADMIN: 1` header
- **Candidate management**: List, view, and update candidates
- **Status management**: Update candidate application status with feedback
- **Resume access**: Download and review candidate resumes
- **System administration**: Access admin interface and system settings

### Candidates
- **Public registration**: Submit applications with personal information
- **Status checking**: Check application status via public endpoint
- **Email notifications**: Receive confirmation and status update emails
- **No direct system access**: Cannot view other candidates or admin features

## Features

### Candidate Management
- Add new candidates with all their details
- Upload and store resume files
- Update candidate information
- View candidate details and history

### Status Tracking
- Track application progress through different stages
- Automatic status history logging
- Status validation (can't skip steps)
- Timestamps for all changes

### Email Notifications
- **Registration confirmation**: Welcome email when candidate registers
- **Status updates**: Notify candidates when their status changes
- **Asynchronous processing**: Emails sent in background using Celery
- **Template-based**: HTML and plain text email templates
- **Configurable**: Support for multiple email providers (SMTP, AWS SES, etc.)

### Background Tasks
- **Celery integration**: Process tasks asynchronously
- **RabbitMQ message queue**: Reliable task processing
- **Email queuing**: Non-blocking email sending
- **Task monitoring**: Track task status and failures

### Search and Filter
- Search by name or email
- Filter by application status
- Filter by department
- Sort by any field
- Pagination for large lists

### File Handling
- Resume upload with validation
- File type checking (PDF, DOC, DOCX)
- File size limits (5MB max)
- Secure file storage
- Resume download for admins

### Security
- Admin-only access for most features
- Public status checking endpoint
- File upload validation
- Input sanitization
- CSRF protection

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

   # Email settings (for notifications)
   EMAIL_BACKEND=django.core.mail.backends.dummy.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password

   # Celery settings
   CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

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
   - RabbitMQ message queue starting
   - Celery worker starting

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
- **Message queue**: RabbitMQ starts automatically
- **Background workers**: Celery workers start automatically

## How to run

### Prerequisites
- Docker and Docker Compose
- Git

### Quick start

1. Go to backend folder
   ```bash
   cd backend
   ```

2. Start all services
   ```bash
   make up
   ```

3. Access the API
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/
   - Swagger docs: http://localhost:8000/swagger/

## Commands

### Start and stop
```bash
# Start everything (API, database, frontend, RabbitMQ, Celery)
make up

# Start only the API
make server

# Stop everything
make down

# See logs
make logs

# See Celery logs
make celery-logs
```

### Testing
```bash
# Run all tests
make test

# Run tests with detailed report
make coverage

# Clean up test containers
make test-clean
```

### Development
```bash
# Open shell in container
make shell

# Install dependencies
make install

# Install dev dependencies
make dev

# Start Celery worker
make celery

# Monitor Celery tasks
make celery-monitor
```

### Background tasks
```bash
# Start Celery worker
make celery

# Monitor Celery tasks
make celery-monitor

# Check Celery status
make celery-status

# Restart Celery worker
make celery-restart
```

### Cleanup
```bash
# Clean everything
make clean

# Stop services
make stop

# Show all commands
make help
```

## API Endpoints

### Candidates

| Method | Endpoint | What it does |
|--------|----------|-------------|
| GET | `/api/v1/candidates/` | List all candidates |
| POST | `/api/v1/candidates/` | Add new candidate |
| GET | `/api/v1/candidates/{id}/` | Get one candidate |
| PATCH | `/api/v1/candidates/{id}/` | Update candidate status |
| GET | `/api/v1/candidates/{id}/status-history/` | Get status history |
| GET | `/api/v1/candidates/{id}/resume/` | Download resume |

### Status Check (Public)
| Method | Endpoint | What it does |
|--------|----------|-------------|
| GET | `/api/v1/candidates/status/` | Check status by email (public) |

### Search and filter parameters

- `search` - Search by name or email
- `status` - Filter by status (submitted, under_review, interview_scheduled, accepted, rejected)
- `department` - Filter by department
- `ordering` - Sort results (name, email, created_at, etc.)

## Use Cases

### HR Manager
- Add new candidates through admin interface
- Upload resumes during application process
- Track application progress
- Search and filter candidates
- Download resumes for review
- Update candidate status
- Send status update emails automatically

### Recruiter
- View all candidates in the system
- Filter by department or status
- Search for specific candidates
- Check application progress
- Generate reports
- Receive email notifications for new applications

### Candidate
- Check application status (public endpoint)
- Receive confirmation email upon registration
- Get status update notifications
- No direct access to system

## Data Models

### Candidate
- **id** - Unique identifier
- **full_name** - Candidate's full name
- **email** - Email address (unique)
- **phone** - Phone number (unique)
- **date_of_birth** - Birth date
- **years_of_experience** - Work experience
- **department** - Department applying for
- **resume** - Uploaded resume file
- **current_status** - Current application status
- **created_at** - When candidate was added
- **updated_at** - Last update time

### StatusHistory
- **candidate** - Link to candidate
- **previous_status** - Previous status
- **new_status** - New status
- **feedback** - Admin feedback
- **admin_name** - Admin who made the change
- **admin_email** - Admin email
- **created_at** - When change happened

## Status Flow

1. **Submitted** - Candidate submits application
2. **Under Review** - HR reviews application
3. **Interview Scheduled** - Interview is scheduled
4. **Accepted** - Candidate is accepted
5. **Rejected** - Application is rejected

## Email Notifications

### Registration Confirmation
- **Trigger**: When candidate registers
- **Content**: Welcome message with application details
- **Template**: `templates/emails/registration_confirmation.html`
- **Async**: Sent in background using Celery

### Status Updates
- **Trigger**: When admin updates candidate status
- **Content**: Status change notification with feedback
- **Template**: `templates/emails/status_update.html`
- **Async**: Sent in background using Celery

### Email Configuration
- **SMTP**: Default for development
- **AWS SES**: For production
- **Dummy backend**: For testing (no actual emails sent)
- **Templates**: HTML and plain text versions

## Background Tasks

### Celery Integration
- **Task queue**: RabbitMQ for reliable message processing
- **Worker processes**: Handle email sending and other tasks
- **Task monitoring**: Track success/failure of background jobs
- **Scalable**: Multiple workers can be added for high load

### Available Tasks
- **send_email_task**: Send email notifications asynchronously
- **debug_task**: Test task for monitoring

### Task Configuration
- **Broker**: RabbitMQ (amqp://guest:guest@rabbitmq:5672//)
- **Result backend**: Disabled (not needed for email tasks)
- **Concurrency**: 12 workers per container
- **Task routing**: Automatic routing to appropriate queues

## File Upload

### Supported formats
- PDF files
- DOC files
- DOCX files

### Limits
- Maximum file size: 5MB
- One resume per candidate

## Testing

The backend has comprehensive tests:

- **50 tests** covering all features
- **89% code coverage**
- **Fast execution** (2.4 seconds for all tests)
- **Isolated environment** (SQLite in-memory)

### Test categories
- Model tests (database operations)
- View tests (API endpoints)
- Serializer tests (data validation)
- Permission tests (access control)
- Validator tests (custom validation)
- Email notification tests
- Background task tests

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

## Rate Limiting

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

## File Storage Configuration

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

## Tools & Libraries Used

### Backend Framework
- **Django 5.2.4** - Web framework
- **Django REST Framework 3.14+** - API toolkit
- **PostgreSQL 15** - Database
- **SQLite** - Test database

### API & Documentation
- **DRF YASG 1.21+** - Swagger documentation
- **Django CORS Headers 4.0+** - Cross-origin support
- **Django Filter 23.0+** - Advanced filtering

### File Handling
- **Pillow 10.0+** - Image processing
- **Django Storages 1.14+** - Cloud storage
- **Boto3 1.26+** - AWS SDK

### Database
- **Psycopg2 Binary 2.9+** - PostgreSQL adapter
- **Python Decouple 3.8+** - Environment config

### Background Tasks & Messaging
- **Celery 5.3+** - Task queue and background processing
- **Kombu 5.3+** - Message transport
- **AMQP 5.1+** - Message protocol
- **RabbitMQ** - Message broker

### Email & Notifications
- **Django SES 4.4+** - AWS SES integration
- **Email templates** - HTML and plain text
- **Async processing** - Non-blocking email sending

### Testing
- **Pytest 8.4+** - Testing framework
- **Pytest Django 4.11+** - Django integration
- **Pytest Coverage 6.2+** - Coverage reporting
- **Factory Boy 3.2+** - Test data generation
- **Faker 19.0+** - Fake data
- **Pytest Xdist 3.8+** - Parallel testing
- **Pytest Benchmark 4.0+** - Performance testing

### Code Quality
- **Black 23.0+** - Code formatting
- **Flake8 6.0+** - Linting
- **Isort 5.12+** - Import sorting

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

# Email settings (for notifications)
EMAIL_BACKEND=django.core.mail.backends.dummy.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery settings
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

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
backend/
├── candidate/              # Main app
│   ├── models.py          # Database models
│   ├── views.py           # API endpoints
│   ├── serializers.py     # Data validation
│   ├── filters.py         # Search and filter
│   ├── permissions.py     # Access control
│   └── tests/             # Tests
├── core/                  # Shared utilities
│   ├── validators.py      # Custom validators
│   ├── notification_service.py  # Email notification service
│   ├── tasks.py           # Celery background tasks
│   └── tests/             # Tests
├── config/                # Django settings
│   ├── settings.py        # Main settings
│   ├── test_settings.py   # Test settings
│   ├── celery.py          # Celery configuration
│   └── urls.py           # URL routing
├── templates/             # Email templates
│   └── emails/           # Email HTML templates
├── manage.py             # Django management
├── Dockerfile            # Container setup
├── entry.sh              # Startup script
├── Makefile              # Commands
└── pyproject.toml        # Dependencies
```

## Technical Assessment Strengths

### Code Quality
- **89% test coverage** with detailed test suite
- **Clean architecture** following Django best practices
- **Type hints** and comprehensive documentation
- **Code formatting** with Black and isort
- **Linting** with Flake8 for code quality

### Performance
- **Database optimization** with strategic indexing
- **Efficient queries** with proper ORM usage
- **Fast test execution** (2.4 seconds for 50 tests)
- **Containerized deployment** for consistency
- **Rate limiting** to prevent abuse
- **Asynchronous processing** for non-blocking operations

### Scalability
- **Microservices architecture** with Docker Compose
- **Cloud storage support** for file handling
- **Database indexing** for large datasets
- **Pagination** for handling large result sets
- **Modular design** for easy extension
- **Background task processing** with Celery and RabbitMQ

### Maintainability
- **Comprehensive documentation** with clear examples
- **Automated testing** with 50 test cases
- **Development tools** for code quality
- **Clear project structure** following conventions
- **Environment configuration** management

### User Experience
- **Intuitive API design** with RESTful endpoints
- **Comprehensive error handling** with meaningful messages
- **Swagger documentation** for API exploration
- **Responsive frontend** with modern UI
- **Real-time status updates** with history tracking
- **Email notifications** for better user engagement

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
lsof -i :5672

# Stop conflicting services or change ports in compose/.env
```

### Celery/RabbitMQ issues
```bash
# Check Celery worker status
make celery-status

# Restart Celery worker
make celery-restart

# Check RabbitMQ logs
docker logs hr_system_rabbitmq

# Restart message queue
make down
make up
```

### Email issues
```bash
# Check email configuration
grep EMAIL compose/.env

# Test email sending
make shell
python manage.py shell
# Test email sending in shell
``` 
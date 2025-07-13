# HR System Backend

A Django REST API backend for managing job candidates and their application status. Built for technical assessment with clean, maintainable code.

## 🎯 What This Backend Does

### **Candidate Management**
- **Register candidates** with personal info, contact details, and resume
- **Track application status** from "Applied" to "Hired" with timestamps
- **Upload and store resumes** securely with file validation
- **Search and filter** candidates by name, email, status, department
- **View status history** for each candidate with detailed timeline

### **Admin Features**
- **Secure admin interface** at `/admin` for HR managers
- **Bulk operations** for efficient candidate management
- **Status updates** with automatic history tracking
- **Resume downloads** for candidate review

## 🛠️ Tech Stack

- **Django 5.0** - Robust Python web framework
- **Django REST Framework** - Powerful API toolkit
- **PostgreSQL** - Reliable database (via Docker)
- **Django Filter** - Advanced filtering and search
- **Pillow** - Image processing for file uploads
- **Docker** - Containerized deployment

## 📁 Project Structure

```
backend/
├── config/                 # Django settings & URLs
│   ├── settings.py        # Main configuration
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI entry point
│   └── asgi.py           # ASGI entry point
├── candidate/             # Candidate management app
│   ├── models.py         # Database models
│   ├── views.py          # API endpoints
│   ├── serializers.py    # Data transformation
│   ├── filters.py        # Search & filtering
│   ├── permissions.py    # Access control
│   └── migrations/       # Database migrations
├── core/                 # Shared utilities
│   └── validators.py     # Custom validators
├── manage.py             # Django management
├── Dockerfile            # Container configuration
├── entry.sh              # Startup script
├── pyproject.toml        # Dependencies
└── uv.lock              # Locked versions
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized setup)
- PostgreSQL (or use Docker)

### Local Development

1. **Clone and navigate**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp ../.env.sample .env
   # Edit .env with your database settings
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the server**
   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/

### Docker Setup

```bash
# From project root
docker-compose up backend
```

## 📚 API Endpoints

### Candidates

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/candidates/` | List all candidates with filtering |
| `POST` | `/api/candidates/` | Create new candidate |
| `GET` | `/api/candidates/{id}/` | Get candidate details |
| `PUT` | `/api/candidates/{id}/` | Update candidate |
| `DELETE` | `/api/candidates/{id}/` | Delete candidate |
| `GET` | `/api/candidates/{id}/status-history/` | Get status history |

### Query Parameters

- `search` - Search by name or email
- `status` - Filter by status (applied, reviewing, interviewed, offered, hired, rejected)
- `department` - Filter by department
- `ordering` - Sort by field (name, email, created_at, etc.)

### Example Requests

```bash
# Get all candidates
curl http://localhost:8000/api/candidates/

# Search candidates
curl http://localhost:8000/api/candidates/?search=john

# Filter by status
curl http://localhost:8000/api/candidates/?status=interviewed

# Create candidate
curl -X POST http://localhost:8000/api/candidates/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "department": "Engineering",
    "status": "applied"
  }'
```

## 🗄️ Database Models

### Candidate
- **name** - Full name (required)
- **email** - Email address (unique, required)
- **phone** - Phone number (optional)
- **department** - Department applying for
- **status** - Current application status
- **resume** - Uploaded resume file
- **created_at** - Application timestamp
- **updated_at** - Last update timestamp

### StatusHistory
- **candidate** - Reference to candidate
- **status** - Status change
- **notes** - Optional notes
- **created_at** - Change timestamp

## 🔐 Security & Permissions

- **Admin authentication** required for all endpoints
- **File upload validation** for resumes
- **Input sanitization** and validation
- **CSRF protection** enabled
- **Secure file storage** with proper permissions

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test candidate

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔧 Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/hr_system

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# File Storage
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

### Settings Highlights

- **CORS enabled** for frontend integration
- **File uploads** configured for resumes
- **Pagination** for large datasets
- **Filtering** with Django Filter
- **Admin interface** customized

## 🐳 Docker

### Build Image
```bash
docker build -t hr-backend .
```

### Run Container
```bash
docker run -p 8000:8000 hr-backend
```

### With Docker Compose
```bash
# From project root
docker-compose up backend
```

## 📊 Features for Technical Assessment

### ✅ **Completed Requirements**

1. **RESTful API** - Full CRUD operations for candidates
2. **Database Design** - Proper models with relationships
3. **File Upload** - Resume handling with validation
4. **Search & Filter** - Advanced querying capabilities
5. **Status Tracking** - Complete status history
6. **Admin Interface** - Django admin customization
7. **Documentation** - Clear API documentation
8. **Docker Support** - Containerized deployment
9. **Clean Code** - Well-structured, maintainable code
10. **Security** - Proper authentication and validation

### 🎯 **Technical Highlights**

- **Modular Design** - Separate apps for different features
- **Custom Validators** - Email and phone validation
- **Advanced Filtering** - Django Filter integration
- **File Management** - Secure resume upload/download
- **Status Workflow** - Complete application lifecycle
- **API Documentation** - Self-documenting endpoints
- **Error Handling** - Proper HTTP status codes
- **Performance** - Optimized queries and pagination

## 🚀 Deployment

### Production Setup
```bash
# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate

# Start with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/db
```

## 🤝 Contributing

1. Follow Django coding standards
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages

## 📝 License

This project is part of a technical assessment.

---

**Ready to manage candidates efficiently?** This backend provides everything you need for a modern HR system with clean, maintainable code that's ready for production use. 
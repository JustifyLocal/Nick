# Ted Sink Law Voice Receptionist AI - Project Structure

## Overview

This document provides a comprehensive overview of the project structure for the Ted Sink Law Voice Receptionist AI system. The project is organized to support scalability, maintainability, and clear separation of concerns.

## Root Directory Structure

```
ted-sink-law-voice-ai/
├── README.md                           # Project overview and quick start
├── requirements.txt                    # Python dependencies
├── main.py                            # Application entry point
├── demo.py                            # Demo script for showcasing features
├── Dockerfile                         # Docker container configuration
├── docker-compose.yml                 # Multi-service deployment
├── .env.example                       # Environment variables template
├── PROJECT_STRUCTURE.md               # This file
│
├── config/                            # Configuration management
│   └── settings.py                    # Application settings and constants
│
├── ai_engine/                         # Core AI conversation logic
│   ├── conversation_manager.py        # Conversation state management
│   └── ai_handler.py                  # OpenAI GPT-4 integration
│
├── voice_processing/                  # Voice input/output handling
│   └── voice_handler.py               # Whisper + ElevenLabs integration
│
├── backend/                           # FastAPI backend application
│   └── main.py                        # API endpoints and server logic
│
├── database/                          # Database models and migrations
│   └── models.py                      # SQLAlchemy models
│
├── tests/                             # Test suite
│   └── test_conversation.py           # Conversation functionality tests
│
├── docs/                              # Documentation
│   ├── API_DOCUMENTATION.md           # Complete API reference
│   └── DEPLOYMENT_GUIDE.md            # Deployment instructions
│
├── monitoring/                        # Monitoring and observability
│   ├── prometheus.yml                 # Prometheus configuration
│   └── grafana/                       # Grafana dashboards
│       ├── dashboards/
│       └── datasources/
│
├── nginx/                             # Web server configuration
│   ├── nginx.conf                     # Nginx main configuration
│   └── ssl/                           # SSL certificates
│
└── logs/                              # Application logs (created at runtime)
```

## Detailed Component Breakdown

### 1. Configuration (`config/`)

**Purpose**: Centralized configuration management for the entire application.

**Key Files**:
- `settings.py`: Contains all application settings, firm information, API configurations, and operational parameters.

**Features**:
- Environment-based configuration
- Firm-specific data (offices, practice areas, service standards)
- AI model settings
- Voice processing parameters
- Brand voice keywords and messaging

### 2. AI Engine (`ai_engine/`)

**Purpose**: Core artificial intelligence functionality for conversation management and response generation.

**Key Components**:

#### `conversation_manager.py`
- **ConversationState**: Enum defining conversation flow states
- **CaseType**: Enum for case classification
- **LeadData**: Data structure for client information
- **ConversationManager**: Main class for conversation orchestration

**Features**:
- Brand voice prompt generation
- Case type analysis and classification
- Jurisdiction verification
- Emergency situation detection
- Lead data management
- Conversation state transitions

#### `ai_handler.py`
- **AIHandler**: OpenAI GPT-4 integration class
- **Response generation**: Context-aware AI responses
- **Data extraction**: Automatic information extraction from conversations
- **Confidence scoring**: Response quality assessment

**Features**:
- OpenAI GPT-4 integration
- Structured data extraction
- Conversation context management
- Error handling and fallback responses
- Performance metrics tracking

### 3. Voice Processing (`voice_processing/`)

**Purpose**: Handle speech-to-text and text-to-speech conversion.

**Key Components**:

#### `voice_handler.py`
- **VoiceHandler**: Main voice processing class
- **Whisper integration**: Speech-to-text conversion
- **ElevenLabs integration**: Text-to-speech with brand voice
- **Audio file management**: Temporary file handling

**Features**:
- OpenAI Whisper for speech recognition
- ElevenLabs for natural-sounding speech synthesis
- Voice optimization for brand consistency
- Audio file format handling
- Performance monitoring

### 4. Backend (`backend/`)

**Purpose**: FastAPI web server providing REST API endpoints.

**Key Components**:

#### `main.py`
- **FastAPI application**: Main web server
- **API endpoints**: RESTful API for all functionality
- **Middleware**: CORS, logging, error handling
- **Request/Response models**: Pydantic data validation

**API Endpoints**:
- `/health`: System health check
- `/conversation/text`: Text-based conversations
- `/conversation/voice`: Voice-based conversations
- `/tts`: Text-to-speech conversion
- `/stt`: Speech-to-text conversion
- `/leads`: Lead management
- `/firm/*`: Firm information endpoints
- `/voice/*`: Voice optimization endpoints

### 5. Database (`database/`)

**Purpose**: Data persistence and management.

**Key Components**:

#### `models.py`
- **Lead**: Client lead information
- **Conversation**: Conversation history and metadata
- **ConversationTurn**: Individual conversation turns
- **Consultation**: Appointment scheduling
- **VoiceGeneration**: Voice processing history
- **FirmSettings**: Configuration management
- **Office**: Office location data
- **PracticeArea**: Practice area definitions
- **SystemMetrics**: Performance monitoring

**Features**:
- SQLAlchemy ORM models
- Relationship management
- Data validation
- Audit trails
- Performance metrics

### 6. Tests (`tests/`)

**Purpose**: Comprehensive testing suite for quality assurance.

**Key Components**:

#### `test_conversation.py`
- **TestConversationManager**: Conversation logic testing
- **TestAIHandler**: AI integration testing
- **TestIntegration**: End-to-end testing

**Features**:
- Unit tests for all components
- Integration tests for complete workflows
- Mock testing for external APIs
- Performance testing
- Error scenario testing

### 7. Documentation (`docs/`)

**Purpose**: Comprehensive documentation for users and developers.

**Key Documents**:

#### `API_DOCUMENTATION.md`
- Complete API reference
- Request/response examples
- Error handling documentation
- SDK examples
- Rate limiting information

#### `DEPLOYMENT_GUIDE.md`
- Local development setup
- Docker deployment
- Production deployment
- Monitoring and logging
- Security considerations
- Troubleshooting guide

### 8. Monitoring (`monitoring/`)

**Purpose**: System observability and performance monitoring.

**Key Components**:

#### `prometheus.yml`
- Metrics collection configuration
- Alert rules
- Service discovery

#### `grafana/`
- **dashboards/**: Pre-configured dashboards
- **datasources/**: Data source configurations

**Features**:
- Real-time performance monitoring
- Custom dashboards for business metrics
- Alert notifications
- Historical data analysis

### 9. Nginx (`nginx/`)

**Purpose**: Web server configuration and SSL management.

**Key Components**:

#### `nginx.conf`
- Reverse proxy configuration
- Load balancing setup
- SSL termination
- Static file serving

#### `ssl/`
- SSL certificate storage
- Certificate renewal automation

### 10. Runtime Directories

**Purpose**: Dynamic content and logs generated during operation.

**Key Directories**:
- `logs/`: Application logs
- `audio_files/`: Generated audio files
- `tmp/`: Temporary processing files

## Data Flow Architecture

```
Client Request
    ↓
Nginx (Load Balancer/SSL)
    ↓
FastAPI Backend
    ↓
AI Engine (Conversation Manager + AI Handler)
    ↓
Voice Processing (STT/TTS)
    ↓
Database (PostgreSQL)
    ↓
Monitoring (Prometheus/Grafana)
```

## Technology Stack

### Backend
- **Python 3.11+**: Core programming language
- **FastAPI**: Modern web framework
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### AI & ML
- **OpenAI GPT-4**: Conversation intelligence
- **OpenAI Whisper**: Speech-to-text
- **ElevenLabs**: Text-to-speech
- **PyTorch**: Machine learning framework

### Database
- **PostgreSQL**: Primary database
- **Redis**: Caching and sessions
- **Alembic**: Database migrations

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Reverse proxy and load balancing
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and monitoring

### Development
- **pytest**: Testing framework
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting

## Security Considerations

### Data Protection
- API key management
- Secure environment variables
- Database encryption
- SSL/TLS encryption
- Input validation and sanitization

### Access Control
- Rate limiting
- CORS configuration
- Authentication (future enhancement)
- Authorization (future enhancement)

### Monitoring
- Security event logging
- Intrusion detection
- Regular security audits
- Vulnerability scanning

## Scalability Features

### Horizontal Scaling
- Stateless application design
- Load balancer support
- Database connection pooling
- Redis caching layer

### Performance Optimization
- Async/await patterns
- Database query optimization
- Audio file compression
- Response caching

### Monitoring and Alerting
- Real-time performance metrics
- Automated alerting
- Capacity planning
- Performance trending

## Deployment Options

### Local Development
- Python virtual environment
- Local PostgreSQL database
- Mock external services

### Docker Development
- Containerized services
- Local volume mounts
- Hot reloading

### Production Deployment
- Multi-container orchestration
- Load balancing
- SSL termination
- Monitoring stack
- Backup and recovery

## Maintenance and Operations

### Regular Tasks
- Log rotation and cleanup
- Database backups
- Security updates
- Performance monitoring
- Capacity planning

### Emergency Procedures
- Incident response
- Rollback procedures
- Disaster recovery
- Communication protocols

This project structure provides a solid foundation for a production-ready voice receptionist AI system that can scale with Ted Sink Law's growing needs while maintaining high quality, security, and performance standards.
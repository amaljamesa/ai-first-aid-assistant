# LIFELINE AI - Backend API

AI-powered emergency detection and first aid assistance backend built with FastAPI.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip or poetry
- OpenAI API key (optional, for AI features)

### Installation

```bash
# Navigate to backend directory
cd ai-first-aid-assistant/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your settings:
   ```env
   OPENAI_API_KEY=your_api_key_here
   DEBUG=True
   PORT=8000
   ```

### Running the Server

```bash
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── app/
│   ├── __init__.py
│   ├── core/              # Core configuration
│   │   ├── config.py      # Settings and environment
│   │   └── logging.py     # Logging configuration
│   ├── api/               # API routes
│   │   └── v1/
│   │       ├── router.py  # Main API router
│   │       └── endpoints/
│   │           ├── emergency.py
│   │           ├── hospital.py
│   │           ├── voice.py
│   │           └── image.py
│   ├── models/            # Data models
│   │   └── schemas.py    # Pydantic schemas
│   └── services/          # Business logic
│       ├── ai/           # AI services
│       │   ├── emergency_classifier.py
│       │   ├── severity_scorer.py
│       │   ├── first_aid_generator.py
│       │   ├── voice_processor.py
│       │   └── image_processor.py
│       └── location/      # Location services
│           └── hospital_finder.py
├── requirements.txt       # Python dependencies
└── .env.example          # Environment template
```

## 🔌 API Endpoints

### Emergency Detection

**POST** `/api/v1/emergency/detect`
- Analyze emergency input and detect type/severity
- Request body: `EmergencyRequest`
- Response: `EmergencyResponse`

**POST** `/api/v1/emergency/first-aid`
- Get first aid instructions for emergency type
- Request body: `FirstAidRequest`
- Response: `EmergencyResponse`

### Hospital Finder

**POST** `/api/v1/hospitals/nearby`
- Find nearby hospitals
- Request body: `HospitalSearchRequest`
- Response: List of `Hospital`

### Voice Processing

**POST** `/api/v1/voice/process`
- Process voice/audio input
- Request body: `VoiceInputRequest`
- Response: `EmergencyResponse`

### Image Processing

**POST** `/api/v1/image/process`
- Process image input
- Request body: `ImageInputRequest`
- Response: `EmergencyResponse`

### Health Check

**GET** `/health`
- Server health status

## 🤖 AI Integration

The backend supports AI-powered features using OpenAI:

- **Emergency Classification**: GPT-4 for emergency type detection
- **Severity Scoring**: AI-based severity assessment
- **First Aid Generation**: Dynamic instruction generation
- **Voice Transcription**: Whisper API for speech-to-text
- **Image Analysis**: GPT-4 Vision for image understanding

### AI Configuration

Set `AI_ENABLED=True` and provide `OPENAI_API_KEY` in `.env` to enable AI features.

Without AI, the system falls back to rule-based classification and template-based instructions.

## 🏗️ Architecture

### Clean Architecture Principles

- **Separation of Concerns**: Routes, services, and models are separated
- **Dependency Injection**: Services are injected into routes
- **Error Handling**: Centralized exception handling
- **Type Safety**: Full Pydantic validation

### Service Layer

- **AI Services**: Modular AI integration (LLM-ready)
- **Location Services**: Hospital finding and geocoding
- **Business Logic**: Separated from API routes

### Scalability

- Async/await for I/O operations
- Modular service architecture
- Easy to add new AI models
- Database-ready structure

## 🔧 Configuration

All configuration is managed through environment variables:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: False)
- `OPENAI_API_KEY`: OpenAI API key
- `AI_ENABLED`: Enable AI features (default: True)
- `CORS_ORIGINS`: Allowed CORS origins

## 📝 Development

### Code Style

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Use async/await for I/O

### Testing

```bash
# Run tests (when implemented)
pytest

# With coverage
pytest --cov=app
```

## 🚀 Deployment

### Production Considerations

1. Set `DEBUG=False`
2. Configure proper CORS origins
3. Use environment variables for secrets
4. Set up proper logging
5. Use production ASGI server (Gunicorn + Uvicorn)

### Docker (Future)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📚 API Documentation

Interactive API documentation is available at `/docs` when `DEBUG=True`.

## 🔐 Security

- Input validation via Pydantic
- CORS configuration
- Error message sanitization in production
- API key management via environment variables

## 🤝 Contributing

1. Follow clean architecture principles
2. Add type hints
3. Write docstrings
4. Handle errors gracefully
5. Test your changes

## 📄 License

[Your License Here]

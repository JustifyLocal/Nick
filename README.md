# Ted Sink Law Firm - Voice Receptionist AI

A sophisticated voice receptionist AI system designed for Ted Sink Law Firm, a next-generation personal injury law firm serving South Carolina and Georgia.

## Features

- **Brand-Authentic Voice**: Embodies Ted Sink Law's confident, empathetic, and modern personality
- **Intelligent Lead Qualification**: Screens for personal injury cases in SC/GA jurisdictions
- **Multi-Format Consultation Booking**: Phone, in-person, virtual, and home/hospital visits
- **24/7 Availability**: Round-the-clock client support with same-day response guarantee
- **Advanced Case Screening**: Automatic disqualification of non-personal injury matters
- **Modern Technology Integration**: Seamless integration with existing firm systems

## Technology Stack

- **Backend**: Python with FastAPI
- **Voice Processing**: OpenAI Whisper + ElevenLabs
- **AI Conversation**: OpenAI GPT-4 with custom prompts
- **Database**: PostgreSQL for client data and case management
- **Frontend**: React with modern UI components
- **Deployment**: Docker containers with Kubernetes orchestration

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run the application
python main.py
```

## Project Structure

```
ted-sink-law-ai/
├── backend/                 # FastAPI backend
├── frontend/               # React frontend
├── ai_engine/              # Core AI conversation logic
├── voice_processing/       # Voice input/output handling
├── database/              # Database models and migrations
├── config/                # Configuration files
└── docs/                  # Documentation
```

## License

Proprietary - Ted Sink Law Firm, LLC
# Ted Sink Law Voice Receptionist AI - API Documentation

## Overview

The Ted Sink Law Voice Receptionist AI provides a comprehensive API for handling voice and text-based conversations with potential clients. The system is designed to qualify leads, collect essential information, and schedule consultations while maintaining Ted Sink Law's brand voice and service standards.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication for basic endpoints. For production deployment, implement appropriate authentication mechanisms.

## API Endpoints

### Health Check

#### GET /health

Check the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-15T10:30:00",
  "version": "1.0.0",
  "firm_name": "Ted Law: Accident & Injury Law Firm, LLC"
}
```

### Conversation Endpoints

#### POST /conversation/text

Handle text-based conversations with the AI receptionist.

**Request Body:**
```json
{
  "text_input": "I was in a car accident and need help",
  "conversation_context": {
    "previous_turns": 2,
    "current_state": "case_screening"
  }
}
```

**Response:**
```json
{
  "response": "Thank you for calling Ted Law, the next-generation personal injury law firm. I understand you were in a car accident. Could you tell me when this happened and where?",
  "conversation_state": "case_screening",
  "extracted_data": {
    "case_type": "Car Accident",
    "urgency_level": "medium"
  },
  "next_actions": ["Verify jurisdiction", "Collect incident details"],
  "confidence_score": 0.85
}
```

#### POST /conversation/voice

Handle voice-based conversations with the AI receptionist.

**Request:**
- `audio_file`: Audio file (WAV, MP3, M4A)
- `conversation_context`: Optional JSON string with conversation context

**Response:**
```json
{
  "transcribed_text": "I was in a car accident and need help",
  "response": "Thank you for calling Ted Law...",
  "conversation_state": "case_screening",
  "extracted_data": {
    "case_type": "Car Accident",
    "urgency_level": "medium"
  },
  "next_actions": ["Verify jurisdiction", "Collect incident details"],
  "confidence_score": 0.85,
  "audio_url": "/audio/response_12345.mp3",
  "stt_metadata": {
    "language": "en",
    "confidence": 0.95,
    "duration": 3.2
  },
  "tts_metadata": {
    "text_length": 150,
    "word_count": 25,
    "file_size": 45000
  }
}
```

#### GET /conversation/summary

Get the current conversation summary.

**Response:**
```json
{
  "conversation_id": "conv_20231215_103000",
  "start_time": "2023-12-15T10:30:00",
  "duration_minutes": 5.2,
  "turns": 8,
  "final_state": "consultation_booking",
  "lead_data": {
    "name": "John Doe",
    "phone": "(555) 123-4567",
    "incident_date": "12/10/2023",
    "case_type": "Car Accident"
  },
  "qualification_status": "qualified"
}
```

#### POST /conversation/reset

Reset the conversation for a new caller.

**Response:**
```json
{
  "message": "Conversation reset successfully"
}
```

### Voice Processing Endpoints

#### POST /tts

Convert text to speech using Ted Sink Law's brand voice.

**Request Body:**
```json
{
  "text": "Thank you for calling Ted Law, the next-generation personal injury law firm.",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

**Response:**
```json
{
  "audio_url": "/audio/tts_12345.mp3",
  "metadata": {
    "text_length": 85,
    "word_count": 15,
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "model": "eleven_monolingual_v1",
    "file_size": 25000
  }
}
```

#### POST /stt

Convert speech to text.

**Request:**
- `audio_file`: Audio file (WAV, MP3, M4A)

**Response:**
```json
{
  "transcribed_text": "I was in a car accident and need help",
  "metadata": {
    "language": "en",
    "confidence": 0.95,
    "segments": 1,
    "duration": 3.2
  }
}
```

#### GET /audio/{filename}

Serve generated audio files.

**Response:** Audio file (MP3 format)

### Lead Management Endpoints

#### POST /leads

Create a new lead from collected data.

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "(555) 123-4567",
  "email": "john.doe@email.com",
  "incident_date": "2023-12-10",
  "incident_location": "Charleston, SC",
  "case_type": "Car Accident",
  "injury_details": "Back and neck pain",
  "medical_treatment": "Emergency room visit",
  "urgency_level": "medium",
  "preferred_consultation": "phone",
  "office_preference": "north_charleston"
}
```

**Response:**
```json
{
  "lead_id": "lead_20231215_103000",
  "lead_data": {
    "name": "John Doe",
    "phone": "(555) 123-4567",
    "email": "john.doe@email.com",
    "incident_date": "2023-12-10",
    "incident_location": "Charleston, SC",
    "case_type": "Car Accident",
    "injury_details": "Back and neck pain",
    "medical_treatment": "Emergency room visit",
    "urgency_level": "medium",
    "preferred_consultation": "phone",
    "office_preference": "north_charleston"
  },
  "created_at": "2023-12-15T10:30:00",
  "status": "created"
}
```

### Voice Optimization Endpoints

#### POST /voice/optimize

Optimize voice settings for Ted Sink Law's brand voice.

**Request Body:**
```json
{
  "sample_text": "Thank you for calling Ted Law, the next-generation personal injury law firm."
}
```

**Response:**
```json
{
  "success": true,
  "test_results": [
    {
      "setting_index": 0,
      "settings": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.0
      },
      "output_path": "/tmp/voice_test_0.mp3",
      "success": true
    }
  ],
  "recommended_setting": {
    "setting_index": 0,
    "settings": {
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.0
    },
    "output_path": "/tmp/voice_test_0.mp3",
    "success": true
  }
}
```

#### GET /voice/history

Get recent voice generation history.

**Query Parameters:**
- `limit`: Number of recent items (default: 10)

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "id": "history_12345",
      "text": "Thank you for calling Ted Law...",
      "voice_id": "21m00Tcm4TlvDq8ikWAM",
      "created_at": "2023-12-15T10:30:00",
      "duration": 3.2,
      "file_size": 25000
    }
  ]
}
```

### Firm Information Endpoints

#### GET /firm/info

Get comprehensive firm information.

**Response:**
```json
{
  "firm_name": "Ted Law: Accident & Injury Law Firm, LLC",
  "founded": 2019,
  "founder": "Ted Sink",
  "service_states": ["South Carolina", "Georgia"],
  "offices": {
    "north_charleston": {
      "name": "North Charleston",
      "address": "1075-A E Montague Ave",
      "phone": "(843) 800-0000",
      "primary": true
    }
  },
  "practice_areas": [
    "Car Accidents",
    "Truck Accidents",
    "Motorcycle Accidents",
    "Workers' Compensation",
    "Wrongful Death",
    "Premises Liability",
    "Ride-share Accidents",
    "Medical Malpractice",
    "Nursing Home Abuse",
    "Slip and Fall",
    "Construction Accidents"
  ],
  "service_standards": {
    "consultation_free": true,
    "contingency_fee": true,
    "satisfaction_guarantee_days": 30,
    "same_day_response": true,
    "availability_24_7": true
  }
}
```

#### GET /firm/offices

Get office locations and contact information.

**Response:**
```json
{
  "offices": {
    "north_charleston": {
      "name": "North Charleston",
      "address": "1075-A E Montague Ave",
      "phone": "(843) 800-0000",
      "primary": true
    },
    "greenville": {
      "name": "Greenville",
      "address": "Greenville Office",
      "phone": "(864) 800-0000"
    }
  },
  "primary_office": {
    "name": "North Charleston",
    "address": "1075-A E Montague Ave",
    "phone": "(843) 800-0000",
    "primary": true
  }
}
```

#### GET /firm/practice-areas

Get practice areas and disqualifying case types.

**Response:**
```json
{
  "practice_areas": [
    "Car Accidents",
    "Truck Accidents",
    "Motorcycle Accidents",
    "Workers' Compensation",
    "Wrongful Death",
    "Premises Liability",
    "Ride-share Accidents",
    "Medical Malpractice",
    "Nursing Home Abuse",
    "Slip and Fall",
    "Construction Accidents"
  ],
  "disqualifying_cases": [
    "Criminal Law",
    "Family Law",
    "Business Law",
    "Real Estate",
    "Estate Planning",
    "Bankruptcy",
    "Immigration"
  ]
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Text input is required"
}
```

### 404 Not Found
```json
{
  "detail": "Audio file not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Conversation States

The AI system operates through the following conversation states:

1. **greeting**: Initial welcome and brand introduction
2. **case_screening**: Determine case type and assess eligibility
3. **jurisdiction_check**: Verify geographic coverage
4. **intake_collection**: Gather essential client information
5. **consultation_booking**: Schedule consultation appointment
6. **emergency_handling**: Handle urgent situations
7. **disqualification**: Professionally decline non-qualifying cases
8. **follow_up**: Confirm details and provide next steps

## Lead Qualification Criteria

### Qualifying Cases
- Personal injury cases in South Carolina or Georgia
- Clear liability and significant damages
- Within statute of limitations
- Requiring legal representation

### Disqualifying Factors
- Cases outside SC/GA jurisdiction
- Non-personal injury matters
- Minimal damages
- Unclear liability
- Outside statute of limitations

## Brand Voice Guidelines

The AI maintains Ted Sink Law's brand voice through:

- **Confident and empathetic tone**
- **Technology-forward messaging**
- **"Next-generation law firm" positioning**
- **"No fee unless we win" emphasis**
- **David vs. Goliath narrative**
- **Personal attention focus**

## Rate Limits

- Text conversations: 100 requests per minute
- Voice conversations: 50 requests per minute
- TTS/STT: 200 requests per minute

## File Upload Limits

- Audio files: Maximum 50MB
- Supported formats: WAV, MP3, M4A
- Maximum duration: 10 minutes

## WebSocket Support

For real-time voice conversations, WebSocket endpoints are available:

```
ws://localhost:8000/ws/conversation
```

## SDK Examples

### Python Client Example

```python
import requests
import json

# Text conversation
response = requests.post(
    "http://localhost:8000/conversation/text",
    json={
        "text_input": "I was in a car accident and need help",
        "conversation_context": {}
    }
)
print(response.json())

# Voice conversation
with open("audio_input.wav", "rb") as audio_file:
    files = {"audio_file": audio_file}
    data = {"conversation_context": "{}"}
    response = requests.post(
        "http://localhost:8000/conversation/voice",
        files=files,
        data=data
    )
print(response.json())
```

### JavaScript Client Example

```javascript
// Text conversation
const response = await fetch('/conversation/text', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text_input: 'I was in a car accident and need help',
    conversation_context: {}
  })
});

const data = await response.json();
console.log(data);

// Voice conversation
const formData = new FormData();
formData.append('audio_file', audioBlob);
formData.append('conversation_context', '{}');

const voiceResponse = await fetch('/conversation/voice', {
  method: 'POST',
  body: formData
});

const voiceData = await voiceResponse.json();
console.log(voiceData);
```

## Support

For technical support or questions about the API, please contact the development team or refer to the system logs for detailed error information.
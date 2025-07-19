"""
Main FastAPI application for Ted Sink Law Voice Receptionist AI
"""
import logging
import os
from typing import Dict, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from config.settings import settings
from ai_engine.ai_handler import AIHandler
from voice_processing.voice_handler import VoiceHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Voice Receptionist AI for Ted Sink Law Firm"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize handlers
ai_handler = AIHandler()
voice_handler = VoiceHandler()


# Pydantic models for API requests/responses
class ConversationRequest(BaseModel):
    text_input: Optional[str] = None
    conversation_context: Optional[Dict] = None


class ConversationResponse(BaseModel):
    response: str
    conversation_state: str
    extracted_data: Dict
    next_actions: list
    confidence_score: float
    audio_url: Optional[str] = None


class VoiceRequest(BaseModel):
    text: str
    voice_settings: Optional[Dict] = None


class LeadData(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    incident_date: Optional[str] = None
    incident_location: Optional[str] = None
    case_type: Optional[str] = None
    injury_details: Optional[str] = None
    medical_treatment: Optional[str] = None
    insurance_info: Optional[str] = None
    urgency_level: Optional[str] = None
    preferred_consultation: Optional[str] = None
    office_preference: Optional[str] = None


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version,
        "firm_name": settings.firm_name
    }


# Text-based conversation endpoint
@app.post("/conversation/text", response_model=ConversationResponse)
async def text_conversation(request: ConversationRequest):
    """
    Handle text-based conversation with the AI receptionist
    """
    try:
        if not request.text_input:
            raise HTTPException(status_code=400, detail="Text input is required")
        
        # Generate AI response
        response_data = ai_handler.generate_response(
            request.text_input, 
            request.conversation_context
        )
        
        return ConversationResponse(
            response=response_data["response"],
            conversation_state=response_data["conversation_state"],
            extracted_data=response_data["extracted_data"],
            next_actions=response_data["next_actions"],
            confidence_score=response_data["confidence_score"]
        )
        
    except Exception as e:
        logger.error(f"Error in text conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Voice-based conversation endpoint
@app.post("/conversation/voice")
async def voice_conversation(
    audio_file: UploadFile = File(...),
    conversation_context: Optional[str] = Form(None)
):
    """
    Handle voice-based conversation with the AI receptionist
    """
    try:
        # Save uploaded audio file
        temp_audio_path = f"/tmp/input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(temp_audio_path, "wb") as buffer:
            buffer.write(await audio_file.read())
        
        # Convert speech to text
        transcribed_text, stt_metadata = voice_handler.speech_to_text(temp_audio_path)
        
        if not transcribed_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")
        
        # Parse conversation context
        context = None
        if conversation_context:
            import json
            try:
                context = json.loads(conversation_context)
            except json.JSONDecodeError:
                logger.warning("Invalid conversation context JSON")
        
        # Generate AI response
        response_data = ai_handler.generate_response(transcribed_text, context)
        
        # Convert response to speech
        audio_output_path, tts_metadata = voice_handler.text_to_speech(
            response_data["response"]
        )
        
        if not audio_output_path:
            raise HTTPException(status_code=500, detail="Could not generate speech response")
        
        # Return response with audio file
        return {
            "transcribed_text": transcribed_text,
            "response": response_data["response"],
            "conversation_state": response_data["conversation_state"],
            "extracted_data": response_data["extracted_data"],
            "next_actions": response_data["next_actions"],
            "confidence_score": response_data["confidence_score"],
            "audio_url": f"/audio/{os.path.basename(audio_output_path)}",
            "stt_metadata": stt_metadata,
            "tts_metadata": tts_metadata
        }
        
    except Exception as e:
        logger.error(f"Error in voice conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Audio file serving endpoint
@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    """Serve generated audio files"""
    try:
        audio_path = f"/tmp/{filename}"
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Error serving audio file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Text-to-speech endpoint
@app.post("/tts")
async def text_to_speech(request: VoiceRequest):
    """
    Convert text to speech using Ted Sink Law's brand voice
    """
    try:
        audio_path, metadata = voice_handler.text_to_speech(request.text)
        
        if not audio_path:
            raise HTTPException(status_code=500, detail="Could not generate speech")
        
        return {
            "audio_url": f"/audio/{os.path.basename(audio_path)}",
            "metadata": metadata
        }
        
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Speech-to-text endpoint
@app.post("/stt")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """
    Convert speech to text
    """
    try:
        # Save uploaded audio file
        temp_audio_path = f"/tmp/stt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(temp_audio_path, "wb") as buffer:
            buffer.write(await audio_file.read())
        
        # Convert speech to text
        transcribed_text, metadata = voice_handler.speech_to_text(temp_audio_path)
        
        return {
            "transcribed_text": transcribed_text,
            "metadata": metadata
        }
        
    except Exception as e:
        logger.error(f"Error in speech-to-text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Conversation management endpoints
@app.get("/conversation/summary")
async def get_conversation_summary():
    """Get current conversation summary"""
    try:
        return ai_handler.get_conversation_summary()
    except Exception as e:
        logger.error(f"Error getting conversation summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/conversation/reset")
async def reset_conversation():
    """Reset conversation for new caller"""
    try:
        ai_handler.reset_conversation()
        return {"message": "Conversation reset successfully"}
    except Exception as e:
        logger.error(f"Error resetting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Lead data management endpoints
@app.post("/leads")
async def create_lead(lead_data: LeadData):
    """Create a new lead from collected data"""
    try:
        # Here you would typically save to database
        # For now, we'll just return the data
        return {
            "lead_id": f"lead_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "lead_data": lead_data.dict(),
            "created_at": datetime.now().isoformat(),
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Error creating lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Voice optimization endpoints
@app.post("/voice/optimize")
async def optimize_voice_settings(sample_text: Optional[str] = None):
    """Optimize voice settings for Ted Sink Law's brand voice"""
    try:
        result = voice_handler.optimize_voice_settings(sample_text)
        return result
    except Exception as e:
        logger.error(f"Error optimizing voice settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/voice/history")
async def get_voice_history(limit: int = 10):
    """Get recent voice generation history"""
    try:
        return voice_handler.get_voice_history(limit)
    except Exception as e:
        logger.error(f"Error getting voice history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Firm information endpoints
@app.get("/firm/info")
async def get_firm_info():
    """Get Ted Sink Law firm information"""
    return {
        "firm_name": settings.firm_name,
        "founded": settings.firm_founded,
        "founder": settings.founder,
        "service_states": settings.service_states,
        "offices": settings.offices,
        "practice_areas": settings.practice_areas,
        "service_standards": {
            "consultation_free": settings.consultation_free,
            "contingency_fee": settings.contingency_fee,
            "satisfaction_guarantee_days": settings.satisfaction_guarantee_days,
            "same_day_response": settings.same_day_response,
            "availability_24_7": settings.availability_24_7
        }
    }


@app.get("/firm/offices")
async def get_offices():
    """Get office locations and contact information"""
    return {
        "offices": settings.offices,
        "primary_office": next(
            (office for office in settings.offices.values() if office.get("primary")), 
            None
        )
    }


@app.get("/firm/practice-areas")
async def get_practice_areas():
    """Get practice areas and disqualifying case types"""
    return {
        "practice_areas": settings.practice_areas,
        "disqualifying_cases": settings.disqualifying_cases
    }


# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Firm: {settings.firm_name}")
    logger.info(f"Service states: {', '.join(settings.service_states)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down voice receptionist AI")
    voice_handler.cleanup_temp_files()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
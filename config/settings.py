"""
Configuration settings for Ted Sink Law Firm Voice Receptionist AI
"""
from pydantic_settings import BaseSettings
from typing import List, Dict, Optional
import os


class Settings(BaseSettings):
    # Application Settings
    app_name: str = "Ted Sink Law Voice Receptionist AI"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API Keys
    openai_api_key: str
    elevenlabs_api_key: str
    
    # Database
    database_url: str = "postgresql://user:password@localhost/ted_sink_law"
    
    # Voice Settings
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs voice ID
    voice_stability: float = 0.5
    voice_similarity_boost: float = 0.75
    
    # Firm Information
    firm_name: str = "Ted Law: Accident & Injury Law Firm, LLC"
    firm_founded: int = 2019
    founder: str = "Ted Sink"
    
    # Geographic Coverage
    service_states: List[str] = ["South Carolina", "Georgia"]
    timezone: str = "America/New_York"
    
    # Office Locations
    offices: Dict[str, Dict[str, str]] = {
        "north_charleston": {
            "name": "North Charleston",
            "address": "1075-A E Montague Ave",
            "phone": "(843) 800-0000",
            "primary": True
        },
        "greenville": {
            "name": "Greenville",
            "address": "Greenville Office",
            "phone": "(864) 800-0000"
        },
        "myrtle_beach": {
            "name": "Myrtle Beach",
            "address": "Myrtle Beach Office",
            "phone": "(843) 800-0000"
        },
        "columbia": {
            "name": "Columbia",
            "address": "Columbia Office",
            "phone": "(803) 800-0000"
        },
        "aiken": {
            "name": "Aiken",
            "address": "Aiken Office",
            "phone": "(803) 800-0000"
        },
        "atlanta": {
            "name": "Atlanta",
            "address": "Atlanta Office",
            "phone": "(404) 800-0000"
        }
    }
    
    # Practice Areas
    practice_areas: List[str] = [
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
    ]
    
    # Disqualifying Case Types
    disqualifying_cases: List[str] = [
        "Criminal Law",
        "Family Law",
        "Business Law",
        "Real Estate",
        "Estate Planning",
        "Bankruptcy",
        "Immigration"
    ]
    
    # Service Standards
    consultation_free: bool = True
    contingency_fee: bool = True
    satisfaction_guarantee_days: int = 30
    same_day_response: bool = True
    availability_24_7: bool = True
    
    # AI Conversation Settings
    max_conversation_turns: int = 20
    conversation_timeout_minutes: int = 30
    
    # Lead Qualification Thresholds
    min_damages_threshold: float = 5000.0
    statute_of_limitations_years: int = 3
    
    # Brand Voice Keywords
    brand_keywords: List[str] = [
        "next-generation law firm",
        "21st century technology",
        "we won't back down from a fight",
        "no fee unless we win",
        "David vs. Goliath",
        "personal attention",
        "rapid response",
        "modern tools"
    ]
    
    # Emergency Keywords
    emergency_keywords: List[str] = [
        "emergency",
        "urgent",
        "hospital",
        "severe injury",
        "life-threatening",
        "immediate",
        "critical"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
"""
Database models for Ted Sink Law Voice Receptionist AI
"""
from datetime import datetime
from typing import Optional, Dict, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Lead(Base):
    """Lead data model for potential clients"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Contact Information
    name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Case Information
    incident_date = Column(DateTime, nullable=True)
    incident_location = Column(String(255), nullable=True)
    case_type = Column(String(100), nullable=True)
    injury_details = Column(Text, nullable=True)
    medical_treatment = Column(Text, nullable=True)
    insurance_info = Column(Text, nullable=True)
    
    # Lead Classification
    urgency_level = Column(String(20), default="low")  # low, medium, high
    qualification_status = Column(String(20), default="pending")  # qualified, disqualified, pending
    office_preference = Column(String(50), nullable=True)
    preferred_consultation = Column(String(50), nullable=True)  # phone, in-person, virtual, home
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    source = Column(String(50), default="voice_ai")
    notes = Column(Text, nullable=True)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="lead")
    consultations = relationship("Consultation", back_populates="lead")


class Conversation(Base):
    """Conversation history model"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(50), unique=True, index=True, nullable=False)
    lead_id = Column(Integer, nullable=True)  # Can be null for anonymous conversations
    
    # Conversation Details
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Float, nullable=True)
    turn_count = Column(Integer, default=0)
    
    # Conversation State
    initial_state = Column(String(50), default="greeting")
    final_state = Column(String(50), nullable=True)
    qualification_status = Column(String(20), default="pending")
    
    # AI Performance Metrics
    confidence_scores = Column(JSON, nullable=True)  # Array of confidence scores
    extracted_data = Column(JSON, nullable=True)  # Structured data extracted during conversation
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="conversations")
    conversation_turns = relationship("ConversationTurn", back_populates="conversation")


class ConversationTurn(Base):
    """Individual conversation turn model"""
    __tablename__ = "conversation_turns"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, nullable=False)
    turn_number = Column(Integer, nullable=False)
    
    # Turn Content
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    conversation_state = Column(String(50), nullable=False)
    
    # Voice Processing Data
    audio_input_path = Column(String(255), nullable=True)
    audio_output_path = Column(String(255), nullable=True)
    stt_metadata = Column(JSON, nullable=True)
    tts_metadata = Column(JSON, nullable=True)
    
    # AI Performance
    confidence_score = Column(Float, nullable=True)
    extracted_data = Column(JSON, nullable=True)
    next_actions = Column(JSON, nullable=True)  # Array of next actions
    
    # Metadata
    timestamp = Column(DateTime, default=func.now())
    processing_time_ms = Column(Integer, nullable=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="conversation_turns")


class Consultation(Base):
    """Consultation booking model"""
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(String(50), unique=True, index=True, nullable=False)
    lead_id = Column(Integer, nullable=False)
    
    # Consultation Details
    consultation_type = Column(String(50), nullable=False)  # phone, in-person, virtual, home
    scheduled_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    
    # Location Information
    office_location = Column(String(100), nullable=True)
    virtual_meeting_url = Column(String(255), nullable=True)
    home_address = Column(Text, nullable=True)
    
    # Status
    status = Column(String(20), default="scheduled")  # scheduled, completed, cancelled, no-show
    attorney_assigned = Column(String(100), nullable=True)
    case_manager_assigned = Column(String(100), nullable=True)
    
    # Follow-up
    follow_up_required = Column(Boolean, default=True)
    follow_up_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="consultations")


class VoiceGeneration(Base):
    """Voice generation history model"""
    __tablename__ = "voice_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Generation Details
    text_input = Column(Text, nullable=False)
    audio_output_path = Column(String(255), nullable=True)
    voice_id = Column(String(50), nullable=False)
    
    # Voice Settings
    voice_settings = Column(JSON, nullable=True)
    model_used = Column(String(50), default="eleven_monolingual_v1")
    
    # Performance Metrics
    generation_time_ms = Column(Integer, nullable=True)
    file_size_bytes = Column(Integer, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    
    # Quality Metrics
    confidence_score = Column(Float, nullable=True)
    brand_voice_alignment = Column(Float, nullable=True)  # How well it matches Ted Sink Law's brand
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    conversation_turn_id = Column(Integer, nullable=True)  # Link to conversation turn if applicable


class FirmSettings(Base):
    """Firm settings and configuration model"""
    __tablename__ = "firm_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, index=True, nullable=False)
    setting_value = Column(Text, nullable=False)
    setting_type = Column(String(20), default="string")  # string, integer, float, boolean, json
    description = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String(100), nullable=True)


class Office(Base):
    """Office locations model"""
    __tablename__ = "offices"
    
    id = Column(Integer, primary_key=True, index=True)
    office_key = Column(String(50), unique=True, index=True, nullable=False)
    
    # Office Details
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    
    # Location
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Office Status
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    hours_of_operation = Column(JSON, nullable=True)  # JSON object with hours
    
    # Staff Information
    attorneys = Column(JSON, nullable=True)  # Array of attorney names
    support_staff = Column(JSON, nullable=True)  # Array of support staff names
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class PracticeArea(Base):
    """Practice areas model"""
    __tablename__ = "practice_areas"
    
    id = Column(Integer, primary_key=True, index=True)
    practice_key = Column(String(50), unique=True, index=True, nullable=False)
    
    # Practice Details
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Classification
    category = Column(String(50), nullable=True)  # motor_vehicle, workplace, medical, etc.
    complexity_level = Column(String(20), default="medium")  # low, medium, high
    
    # Success Metrics
    average_settlement = Column(Float, nullable=True)
    success_rate = Column(Float, nullable=True)
    typical_duration_days = Column(Integer, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class SystemMetrics(Base):
    """System performance and usage metrics"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_date = Column(DateTime, nullable=False)
    metric_type = Column(String(50), nullable=False)  # conversation_count, lead_count, etc.
    
    # Metric Values
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)
    
    # Breakdown
    breakdown = Column(JSON, nullable=True)  # Detailed breakdown of the metric
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    
    class Meta:
        unique_together = ('metric_date', 'metric_type')
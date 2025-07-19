"""
Main Voice Receptionist AI for Ted Sink Law

The core AI system that handles client interactions, lead qualification,
appointment scheduling, and maintains Ted Sink Law's brand voice and standards.
"""

import asyncio
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import logging

from .brand_personality import TedSinkLawBrandPersonality
from .conversation_flow import ConversationFlow
from ..qualification.lead_qualifier import TedSinkLawLeadQualifier, LeadInfo, QualificationResult
from ..scheduling.appointment_scheduler import AppointmentScheduler
from ..scheduling.emergency_handler import EmergencyHandler
from ..data.firm_info import TedSinkLawInfo
from ..data.practice_areas import TedSinkLawPracticeAreas
from ..data.client_standards import TedSinkLawClientStandards
from ..utils.call_logger import CallLogger

@dataclass
class CallSession:
    """Represents an active call session"""
    session_id: str
    start_time: datetime
    client_info: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    qualification_result: Optional[QualificationResult] = None
    appointment_scheduled: bool = False
    emergency_handled: bool = False

class TedSinkLawVoiceReceptionist:
    """
    Main voice receptionist AI for Ted Sink Law
    
    Handles client interactions with brand-authentic voice, intelligent
    lead qualification, and exceptional client service standards.
    """
    
    def __init__(self):
        """Initialize the voice receptionist AI"""
        self.brand_personality = TedSinkLawBrandPersonality()
        self.lead_qualifier = TedSinkLawLeadQualifier()
        self.appointment_scheduler = AppointmentScheduler()
        self.emergency_handler = EmergencyHandler()
        self.conversation_flow = ConversationFlow()
        self.call_logger = CallLogger()
        
        # Firm information
        self.firm_info = TedSinkLawInfo()
        self.practice_areas = TedSinkLawPracticeAreas()
        self.client_standards = TedSinkLawClientStandards()
        
        # Active sessions
        self.active_sessions: Dict[str, CallSession] = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def handle_call(self, session_id: str = None) -> str:
        """
        Main entry point for handling incoming calls
        
        Args:
            session_id: Unique identifier for the call session
            
        Returns:
            Initial greeting and conversation starter
        """
        if not session_id:
            session_id = self._generate_session_id()
        
        # Initialize call session
        session = CallSession(
            session_id=session_id,
            start_time=datetime.now(),
            client_info={},
            conversation_history=[]
        )
        self.active_sessions[session_id] = session
        
        # Log call start
        self.call_logger.log_call_start(session_id)
        
        # Generate opening greeting
        opening_greeting = self._generate_opening_greeting()
        
        # Add to conversation history
        session.conversation_history.append({
            "speaker": "AI",
            "message": opening_greeting,
            "timestamp": datetime.now().isoformat()
        })
        
        self.logger.info(f"Call session {session_id} started")
        return opening_greeting
    
    async def process_client_response(self, session_id: str, client_message: str) -> str:
        """
        Process client response and generate appropriate AI response
        
        Args:
            session_id: Call session identifier
            client_message: Client's spoken or typed message
            
        Returns:
            AI response to the client
        """
        if session_id not in self.active_sessions:
            return "I'm sorry, I don't recognize this call session. Let me start fresh."
        
        session = self.active_sessions[session_id]
        
        # Add client message to history
        session.conversation_history.append({
            "speaker": "Client",
            "message": client_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Check for emergency indicators
        if self._is_emergency_indicated(client_message):
            return await self._handle_emergency(session, client_message)
        
        # Extract lead information
        lead_info = self._extract_lead_info(client_message, session)
        
        # Qualify the lead
        qualification_result = self.lead_qualifier.qualify_lead(lead_info)
        session.qualification_result = qualification_result
        
        # Generate appropriate response based on qualification
        ai_response = await self._generate_qualified_response(session, qualification_result, client_message)
        
        # Add AI response to history
        session.conversation_history.append({
            "speaker": "AI",
            "message": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Log interaction
        self.call_logger.log_interaction(session_id, client_message, ai_response)
        
        return ai_response
    
    async def schedule_appointment(self, session_id: str, appointment_preferences: Dict[str, Any]) -> str:
        """
        Schedule appointment for qualified client
        
        Args:
            session_id: Call session identifier
            appointment_preferences: Client's appointment preferences
            
        Returns:
            Confirmation message
        """
        if session_id not in self.active_sessions:
            return "I'm sorry, I don't recognize this call session."
        
        session = self.active_sessions[session_id]
        
        if not session.qualification_result or session.qualification_result.status.value != "qualified":
            return "I need to complete your case evaluation before scheduling an appointment."
        
        # Schedule appointment
        appointment_result = await self.appointment_scheduler.schedule_appointment(
            session_id, appointment_preferences, session.qualification_result
        )
        
        session.appointment_scheduled = True
        
        # Generate confirmation message
        confirmation = self._generate_appointment_confirmation(appointment_result)
        
        # Add to conversation history
        session.conversation_history.append({
            "speaker": "AI",
            "message": confirmation,
            "timestamp": datetime.now().isoformat()
        })
        
        return confirmation
    
    async def end_call(self, session_id: str) -> str:
        """
        End the call session and provide summary
        
        Args:
            session_id: Call session identifier
            
        Returns:
            Call ending message
        """
        if session_id not in self.active_sessions:
            return "Call session not found."
        
        session = self.active_sessions[session_id]
        
        # Generate ending message
        ending_message = self._generate_ending_message(session)
        
        # Log call end
        self.call_logger.log_call_end(session_id, session)
        
        # Clean up session
        del self.active_sessions[session_id]
        
        return ending_message
    
    def _generate_opening_greeting(self) -> str:
        """Generate the opening greeting based on brand personality"""
        personality = self.brand_personality.get_personality_profile()
        return personality.conversation_starters[0]
    
    def _is_emergency_indicated(self, message: str) -> bool:
        """Check if client message indicates emergency situation"""
        emergency_keywords = [
            "emergency", "urgent", "hospital", "ambulance", "serious injury",
            "critical", "immediate", "right now", "asap", "severe"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in emergency_keywords)
    
    async def _handle_emergency(self, session: CallSession, client_message: str) -> str:
        """Handle emergency situations"""
        session.emergency_handled = True
        
        # Use emergency handler
        emergency_response = await self.emergency_handler.handle_emergency(
            session.session_id, client_message
        )
        
        # Update session with emergency status
        session.qualification_result = self.lead_qualifier.qualify_lead(
            self._extract_lead_info(client_message, session)
        )
        
        return emergency_response
    
    def _extract_lead_info(self, message: str, session: CallSession) -> LeadInfo:
        """Extract lead information from client message"""
        # Use lead qualifier's extraction method
        lead_info = self.lead_qualifier.collect_lead_info(message)
        
        # Update session client info
        session.client_info.update({
            "phone": lead_info.phone,
            "email": lead_info.email,
            "location": lead_info.location
        })
        
        return lead_info
    
    async def _generate_qualified_response(self, session: CallSession, 
                                         qualification_result: QualificationResult, 
                                         client_message: str) -> str:
        """Generate response based on qualification result"""
        
        if qualification_result.status.value == "emergency":
            return await self._handle_emergency(session, client_message)
        
        elif qualification_result.status.value == "qualified":
            return self._generate_qualified_client_response(qualification_result, client_message)
        
        elif qualification_result.status.value == "not_qualified":
            return self._generate_disqualified_response(qualification_result, client_message)
        
        else:  # needs_more_info
            return self._generate_info_request_response(client_message)
    
    def _generate_qualified_client_response(self, qualification_result: QualificationResult, 
                                          client_message: str) -> str:
        """Generate response for qualified clients"""
        
        # Get brand personality elements
        personality = self.brand_personality.get_personality_profile()
        
        # Build response based on priority
        if qualification_result.priority.value == "emergency":
            response = "I understand this is urgent and we need to act quickly. "
        elif qualification_result.priority.value == "high":
            response = "This sounds like a serious case that needs immediate attention. "
        else:
            response = "Thank you for sharing your situation with me. "
        
        # Add empathy
        response += self.brand_personality.get_empathy_response("general") + " "
        
        # Add firm capabilities
        response += "We handle cases like yours and have helped many people in similar situations. "
        
        # Add key guarantees
        response += "Our consultation is completely free with no obligation, and we don't charge any fees unless we win your case. "
        
        # Add next steps
        response += "I can schedule you for a consultation today - we guarantee you'll speak with an attorney or case manager the same day. "
        
        # Add practice area specific information
        if qualification_result.practice_area:
            response += f"We have extensive experience with {qualification_result.practice_area.name.lower()} cases. "
        
        # Add call to action
        response += "Would you like me to schedule your free consultation now?"
        
        return response
    
    def _generate_disqualified_response(self, qualification_result: QualificationResult, 
                                      client_message: str) -> str:
        """Generate response for disqualified clients"""
        
        response = "I appreciate you reaching out to us. "
        
        if qualification_result.disqualification_reason:
            if "geographic" in qualification_result.disqualification_reason.lower():
                response += "Unfortunately, we only handle cases in South Carolina and Georgia. "
                response += "I'd be happy to help you find a qualified personal injury attorney in your area. "
            
            elif "case type" in qualification_result.disqualification_reason.lower():
                response += "I understand you're looking for legal help, but we specialize exclusively in personal injury cases. "
                response += "For your type of case, I'd recommend contacting a specialist in that area of law. "
            
            elif "timeline" in qualification_result.disqualification_reason.lower():
                response += "I understand this has been a difficult situation, but there are time limits for filing legal claims. "
                response += "I'd recommend speaking with an attorney who can explain the statute of limitations in your case. "
            
            else:
                response += "After reviewing your situation, I don't believe we're the right fit for your case. "
                response += "I'd be happy to provide you with some resources to help you find appropriate legal assistance. "
        
        # Add referral suggestions
        if qualification_result.referral_suggestions:
            response += "I can suggest some resources to help you find the right attorney for your situation. "
        
        response += "Thank you for considering Ted Law, and I wish you the best with your legal matter."
        
        return response
    
    def _generate_info_request_response(self, client_message: str) -> str:
        """Generate response when more information is needed"""
        
        response = "I'd like to help you with your case, but I need a bit more information to better assist you. "
        
        # Ask for specific information based on what's missing
        if "car accident" in client_message.lower() or "accident" in client_message.lower():
            response += "Could you tell me when the accident occurred and what injuries you sustained? "
        elif "injury" in client_message.lower():
            response += "Could you tell me more about how the injury occurred and what medical treatment you've received? "
        else:
            response += "Could you tell me more about your situation and what type of legal help you're seeking? "
        
        response += "This will help me determine how we can best assist you."
        
        return response
    
    def _generate_appointment_confirmation(self, appointment_result: Dict[str, Any]) -> str:
        """Generate appointment confirmation message"""
        
        response = "Perfect! I've scheduled your free consultation. "
        
        if appointment_result.get("format"):
            response += f"Your {appointment_result['format']} is scheduled for "
        
        if appointment_result.get("date") and appointment_result.get("time"):
            response += f"{appointment_result['date']} at {appointment_result['time']}. "
        
        if appointment_result.get("attorney"):
            response += f"You'll be meeting with {appointment_result['attorney']}. "
        
        response += "You'll receive a confirmation email and text message with all the details. "
        response += "Remember, this consultation is completely free with no obligation. "
        response += "We look forward to helping you with your case!"
        
        return response
    
    def _generate_ending_message(self, session: CallSession) -> str:
        """Generate call ending message"""
        
        if session.emergency_handled:
            response = "I've arranged for immediate assistance with your emergency situation. "
            response += "An attorney will be contacting you right away. "
            response += "Thank you for calling Ted Law, and we're here to help you through this difficult time."
        
        elif session.appointment_scheduled:
            response = "Thank you for choosing Ted Law for your legal needs. "
            response += "We look forward to meeting with you and helping you with your case. "
            response += "If you have any questions before your consultation, please don't hesitate to call us back."
        
        elif session.qualification_result and session.qualification_result.status.value == "qualified":
            response = "Thank you for sharing your situation with me. "
            response += "I hope you'll consider scheduling a free consultation with us. "
            response += "We're here to help when you're ready to take the next step."
        
        else:
            response = "Thank you for calling Ted Law. "
            response += "I appreciate you taking the time to speak with me today. "
            response += "Have a great day!"
        
        return response
    
    def _generate_session_id(self) -> str:
        """Generate unique session identifier"""
        return f"call_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(self)}"
    
    def get_session_info(self, session_id: str) -> Optional[CallSession]:
        """Get information about a specific call session"""
        return self.active_sessions.get(session_id)
    
    def get_active_sessions(self) -> Dict[str, CallSession]:
        """Get all active call sessions"""
        return self.active_sessions.copy()
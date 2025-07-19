"""
Emergency Handler Module for Ted Sink Law

Handles emergency situations and provides immediate assistance
for urgent legal matters requiring immediate attention.
"""

import asyncio
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

from ..data.firm_info import TedSinkLawInfo
from ..data.client_standards import TedSinkLawClientStandards
from ..core.brand_personality import TedSinkLawBrandPersonality

class EmergencyLevel(Enum):
    """Emergency severity levels"""
    CRITICAL = "critical"
    URGENT = "urgent"
    HIGH_PRIORITY = "high_priority"

@dataclass
class EmergencyCase:
    """Emergency case information"""
    session_id: str
    emergency_level: EmergencyLevel
    case_type: str
    client_name: Optional[str]
    contact_phone: Optional[str]
    location: Optional[str]
    description: str
    immediate_needs: List[str]
    timestamp: datetime

class EmergencyHandler:
    """Handles emergency situations for Ted Sink Law"""
    
    def __init__(self):
        """Initialize the emergency handler"""
        self.firm_info = TedSinkLawInfo()
        self.client_standards = TedSinkLawClientStandards()
        self.brand_personality = TedSinkLawBrandPersonality()
        
        # Emergency protocols
        self.emergency_protocols = {
            EmergencyLevel.CRITICAL: {
                "response_time": "Immediate",
                "attorney_contact": "Ted Sink",
                "consultation_format": "Phone or Hospital Visit",
                "follow_up": "Same day",
                "priority": "Highest"
            },
            EmergencyLevel.URGENT: {
                "response_time": "Within 1 hour",
                "attorney_contact": "Ted Sink or Laura",
                "consultation_format": "Phone, Virtual, or Home Visit",
                "follow_up": "Same day",
                "priority": "High"
            },
            EmergencyLevel.HIGH_PRIORITY: {
                "response_time": "Within 4 hours",
                "attorney_contact": "Any available attorney",
                "consultation_format": "Phone or Virtual",
                "follow_up": "Same day",
                "priority": "Medium"
            }
        }
        
        # Active emergency cases
        self.active_emergencies: Dict[str, EmergencyCase] = {}
    
    async def handle_emergency(self, session_id: str, client_message: str) -> str:
        """
        Handle emergency situation
        
        Args:
            session_id: Call session identifier
            client_message: Client's emergency message
            
        Returns:
            Emergency response message
        """
        
        # Assess emergency level
        emergency_level = self._assess_emergency_level(client_message)
        
        # Extract emergency information
        emergency_info = self._extract_emergency_info(client_message)
        
        # Create emergency case
        emergency_case = EmergencyCase(
            session_id=session_id,
            emergency_level=emergency_level,
            case_type=emergency_info.get("case_type", "personal injury"),
            client_name=emergency_info.get("client_name"),
            contact_phone=emergency_info.get("contact_phone"),
            location=emergency_info.get("location"),
            description=client_message,
            immediate_needs=emergency_info.get("immediate_needs", []),
            timestamp=datetime.now()
        )
        
        # Register emergency case
        self.active_emergencies[session_id] = emergency_case
        
        # Generate emergency response
        response = await self._generate_emergency_response(emergency_case)
        
        # Initiate emergency protocols
        await self._initiate_emergency_protocols(emergency_case)
        
        return response
    
    def _assess_emergency_level(self, message: str) -> EmergencyLevel:
        """Assess the level of emergency based on client message"""
        message_lower = message.lower()
        
        # Critical indicators
        critical_indicators = [
            "life-threatening", "critical condition", "emergency room",
            "ambulance", "severe bleeding", "unconscious", "not breathing",
            "heart attack", "stroke", "major trauma"
        ]
        
        if any(indicator in message_lower for indicator in critical_indicators):
            return EmergencyLevel.CRITICAL
        
        # Urgent indicators
        urgent_indicators = [
            "serious injury", "broken bones", "head injury", "hospital",
            "surgery", "immediate", "right now", "asap", "urgent"
        ]
        
        if any(indicator in message_lower for indicator in urgent_indicators):
            return EmergencyLevel.URGENT
        
        # High priority indicators
        high_priority_indicators = [
            "severe pain", "significant injury", "medical bills",
            "lost wages", "serious accident", "major damages"
        ]
        
        if any(indicator in message_lower for indicator in high_priority_indicators):
            return EmergencyLevel.HIGH_PRIORITY
        
        return EmergencyLevel.HIGH_PRIORITY  # Default to high priority for safety
    
    def _extract_emergency_info(self, message: str) -> Dict[str, Any]:
        """Extract relevant information from emergency message"""
        info = {}
        message_lower = message.lower()
        
        # Extract case type
        case_types = [
            "car accident", "truck accident", "motorcycle accident",
            "slip and fall", "workplace injury", "medical malpractice",
            "wrongful death", "construction accident"
        ]
        
        for case_type in case_types:
            if case_type in message_lower:
                info["case_type"] = case_type
                break
        
        # Extract location
        location_indicators = ["in", "at", "from", "near", "around"]
        words = message.split()
        for i, word in enumerate(words):
            if word.lower() in location_indicators and i + 1 < len(words):
                potential_location = words[i + 1]
                if any(state in potential_location.lower() for state in ["south carolina", "georgia", "sc", "ga"]):
                    info["location"] = potential_location
                    break
        
        # Extract immediate needs
        immediate_needs = []
        if "hospital" in message_lower or "emergency room" in message_lower:
            immediate_needs.append("hospital visit")
        if "home" in message_lower and "visit" in message_lower:
            immediate_needs.append("home visit")
        if "phone" in message_lower and "call" in message_lower:
            immediate_needs.append("phone consultation")
        
        info["immediate_needs"] = immediate_needs
        
        # Extract contact information (simplified)
        import re
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phone_match = re.search(phone_pattern, message)
        if phone_match:
            info["contact_phone"] = phone_match.group()
        
        return info
    
    async def _generate_emergency_response(self, emergency_case: EmergencyCase) -> str:
        """Generate appropriate emergency response"""
        
        protocol = self.emergency_protocols[emergency_case.emergency_level]
        
        # Start with empathy and urgency acknowledgment
        response = self.brand_personality.get_empathy_response("severe_injury") + " "
        
        # Add emergency acknowledgment
        if emergency_case.emergency_level == EmergencyLevel.CRITICAL:
            response += "I understand this is a critical situation requiring immediate attention. "
        elif emergency_case.emergency_level == EmergencyLevel.URGENT:
            response += "I understand this is urgent and we need to act quickly. "
        else:
            response += "I understand this is a serious situation that needs immediate attention. "
        
        # Add immediate action
        response += f"I'm connecting you immediately with {protocol['attorney_contact']} who will call you within {protocol['response_time'].lower()}. "
        
        # Add consultation options
        if "hospital visit" in emergency_case.immediate_needs:
            response += "We can arrange for an attorney to visit you at the hospital if needed. "
        elif "home visit" in emergency_case.immediate_needs:
            response += "We can arrange for an attorney to visit you at home if you're unable to travel. "
        else:
            response += "We can conduct an immediate phone consultation to assess your situation. "
        
        # Add reassurance
        response += "You're not alone in this - we're here to help you through this difficult time. "
        
        # Add next steps
        response += f"An attorney will contact you {protocol['response_time'].lower()} to discuss your case and provide immediate guidance. "
        
        # Add contact information
        primary_office = self.firm_info.get_primary_office()
        response += f"If you need to reach us immediately, you can call {primary_office.phone}. "
        
        return response
    
    async def _initiate_emergency_protocols(self, emergency_case: EmergencyCase) -> None:
        """Initiate emergency protocols based on emergency level"""
        
        protocol = self.emergency_protocols[emergency_case.emergency_level]
        
        # Log emergency
        await self._log_emergency(emergency_case)
        
        # Notify appropriate attorney
        await self._notify_attorney(emergency_case, protocol)
        
        # Schedule immediate consultation
        await self._schedule_emergency_consultation(emergency_case, protocol)
        
        # Set up follow-up
        await self._setup_follow_up(emergency_case, protocol)
    
    async def _log_emergency(self, emergency_case: EmergencyCase) -> None:
        """Log emergency case for record keeping"""
        # In production, this would save to database and alert management
        print(f"EMERGENCY LOGGED: {emergency_case.emergency_level.value} - {emergency_case.case_type}")
        print(f"Session: {emergency_case.session_id}")
        print(f"Description: {emergency_case.description}")
        print(f"Timestamp: {emergency_case.timestamp}")
    
    async def _notify_attorney(self, emergency_case: EmergencyCase, protocol: Dict[str, str]) -> None:
        """Notify appropriate attorney of emergency"""
        attorney = protocol["attorney_contact"]
        
        # In production, this would send immediate notification
        print(f"NOTIFYING ATTORNEY: {attorney}")
        print(f"Emergency Level: {emergency_case.emergency_level.value}")
        print(f"Case Type: {emergency_case.case_type}")
        print(f"Client Contact: {emergency_case.contact_phone}")
        print(f"Response Time Required: {protocol['response_time']}")
    
    async def _schedule_emergency_consultation(self, emergency_case: EmergencyCase, 
                                            protocol: Dict[str, str]) -> None:
        """Schedule emergency consultation"""
        
        # Determine consultation format
        if "hospital visit" in emergency_case.immediate_needs:
            format_type = "hospital_visit"
        elif "home visit" in emergency_case.immediate_needs:
            format_type = "home_visit"
        else:
            format_type = "phone"
        
        # Create emergency appointment
        appointment = {
            "session_id": emergency_case.session_id,
            "format": format_type,
            "attorney": protocol["attorney_contact"],
            "urgency": emergency_case.emergency_level.value,
            "case_type": emergency_case.case_type,
            "client_name": emergency_case.client_name,
            "contact_phone": emergency_case.contact_phone,
            "location": emergency_case.location,
            "response_time": protocol["response_time"]
        }
        
        # In production, this would create immediate appointment
        print(f"EMERGENCY APPOINTMENT SCHEDULED: {appointment}")
    
    async def _setup_follow_up(self, emergency_case: EmergencyCase, protocol: Dict[str, str]) -> None:
        """Set up follow-up for emergency case"""
        
        follow_up = {
            "session_id": emergency_case.session_id,
            "emergency_level": emergency_case.emergency_level.value,
            "follow_up_time": protocol["follow_up"],
            "attorney": protocol["attorney_contact"],
            "case_type": emergency_case.case_type,
            "client_contact": emergency_case.contact_phone
        }
        
        # In production, this would schedule follow-up
        print(f"FOLLOW-UP SCHEDULED: {follow_up}")
    
    def get_emergency_protocol(self, emergency_level: EmergencyLevel) -> Dict[str, str]:
        """Get emergency protocol for specific level"""
        return self.emergency_protocols.get(emergency_level, {})
    
    def get_active_emergencies(self) -> Dict[str, EmergencyCase]:
        """Get all active emergency cases"""
        return self.active_emergencies.copy()
    
    def resolve_emergency(self, session_id: str) -> None:
        """Mark emergency as resolved"""
        if session_id in self.active_emergencies:
            del self.active_emergencies[session_id]
    
    def is_emergency_active(self, session_id: str) -> bool:
        """Check if emergency is active for session"""
        return session_id in self.active_emergencies
    
    def get_emergency_case(self, session_id: str) -> Optional[EmergencyCase]:
        """Get emergency case for session"""
        return self.active_emergencies.get(session_id)
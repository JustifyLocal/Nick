"""
Conversation Flow Module for Ted Sink Law Voice Receptionist AI

Manages conversation state, flow, and context to ensure smooth
client interactions and appropriate response generation.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime

class ConversationState(Enum):
    """Conversation states"""
    GREETING = "greeting"
    INFORMATION_GATHERING = "information_gathering"
    QUALIFICATION = "qualification"
    APPOINTMENT_SCHEDULING = "appointment_scheduling"
    CONFIRMATION = "confirmation"
    REFERRAL = "referral"
    EMERGENCY = "emergency"
    ENDING = "ending"

class ConversationIntent(Enum):
    """Client conversation intents"""
    SCHEDULE_CONSULTATION = "schedule_consultation"
    GET_INFORMATION = "get_information"
    EMERGENCY_HELP = "emergency_help"
    CASE_UPDATE = "case_update"
    GENERAL_INQUIRY = "general_inquiry"
    COMPLAINT = "complaint"
    REFERRAL_REQUEST = "referral_request"

@dataclass
class ConversationContext:
    """Context information for the conversation"""
    state: ConversationState
    intent: Optional[ConversationIntent]
    client_name: Optional[str]
    case_type: Optional[str]
    urgency_level: Optional[str]
    previous_topics: List[str]
    information_needed: List[str]
    last_response: Optional[str]

class ConversationFlow:
    """Manages conversation flow and state"""
    
    def __init__(self):
        """Initialize conversation flow manager"""
        self.conversation_contexts: Dict[str, ConversationContext] = {}
    
    def initialize_conversation(self, session_id: str) -> ConversationContext:
        """Initialize a new conversation context"""
        context = ConversationContext(
            state=ConversationState.GREETING,
            intent=None,
            client_name=None,
            case_type=None,
            urgency_level=None,
            previous_topics=[],
            information_needed=[
                "case_type",
                "location",
                "incident_date",
                "injuries",
                "contact_information"
            ],
            last_response=None
        )
        
        self.conversation_contexts[session_id] = context
        return context
    
    def update_conversation_state(self, session_id: str, new_state: ConversationState) -> None:
        """Update the conversation state"""
        if session_id in self.conversation_contexts:
            self.conversation_contexts[session_id].state = new_state
    
    def detect_intent(self, client_message: str) -> ConversationIntent:
        """Detect client's conversation intent"""
        message_lower = client_message.lower()
        
        # Emergency indicators
        if any(word in message_lower for word in ["emergency", "urgent", "immediate", "right now"]):
            return ConversationIntent.EMERGENCY_HELP
        
        # Scheduling indicators
        if any(word in message_lower for word in ["schedule", "appointment", "meeting", "consultation", "yes"]):
            return ConversationIntent.SCHEDULE_CONSULTATION
        
        # Information request indicators
        if any(word in message_lower for word in ["what", "how", "tell me", "explain", "information"]):
            return ConversationIntent.GET_INFORMATION
        
        # Case update indicators
        if any(word in message_lower for word in ["update", "status", "progress", "my case"]):
            return ConversationIntent.CASE_UPDATE
        
        # Complaint indicators
        if any(word in message_lower for word in ["problem", "issue", "complaint", "unhappy", "dissatisfied"]):
            return ConversationIntent.COMPLAINT
        
        # Referral indicators
        if any(word in message_lower for word in ["refer", "other attorney", "different lawyer"]):
            return ConversationIntent.REFERRAL_REQUEST
        
        return ConversationIntent.GENERAL_INQUIRY
    
    def extract_information(self, client_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Extract relevant information from client message"""
        extracted_info = {}
        message_lower = client_message.lower()
        
        # Extract case type
        case_types = [
            "car accident", "truck accident", "motorcycle accident", "slip and fall",
            "workers compensation", "medical malpractice", "wrongful death",
            "premises liability", "dog bite", "construction accident"
        ]
        
        for case_type in case_types:
            if case_type in message_lower:
                extracted_info["case_type"] = case_type
                context.case_type = case_type
                break
        
        # Extract location
        location_indicators = ["in", "at", "from", "near", "around"]
        words = client_message.split()
        for i, word in enumerate(words):
            if word.lower() in location_indicators and i + 1 < len(words):
                potential_location = words[i + 1]
                if any(state in potential_location.lower() for state in ["south carolina", "georgia", "sc", "ga"]):
                    extracted_info["location"] = potential_location
                    break
        
        # Extract urgency
        urgency_indicators = ["urgent", "emergency", "immediate", "asap", "right now"]
        if any(indicator in message_lower for indicator in urgency_indicators):
            extracted_info["urgency_level"] = "high"
            context.urgency_level = "high"
        
        # Extract name (simplified)
        if "my name is" in message_lower:
            name_start = message_lower.find("my name is") + 10
            name_end = message_lower.find(" ", name_start)
            if name_end == -1:
                name_end = len(message_lower)
            extracted_info["client_name"] = client_message[name_start:name_end].strip()
            context.client_name = extracted_info["client_name"]
        
        return extracted_info
    
    def determine_next_state(self, current_state: ConversationState, intent: ConversationIntent, 
                           qualification_status: str) -> ConversationState:
        """Determine the next conversation state based on current state and intent"""
        
        if intent == ConversationIntent.EMERGENCY_HELP:
            return ConversationState.EMERGENCY
        
        if current_state == ConversationState.GREETING:
            if intent == ConversationIntent.SCHEDULE_CONSULTATION:
                return ConversationState.APPOINTMENT_SCHEDULING
            else:
                return ConversationState.INFORMATION_GATHERING
        
        elif current_state == ConversationState.INFORMATION_GATHERING:
            if qualification_status == "qualified":
                return ConversationState.QUALIFICATION
            elif qualification_status == "not_qualified":
                return ConversationState.REFERRAL
            else:
                return ConversationState.INFORMATION_GATHERING
        
        elif current_state == ConversationState.QUALIFICATION:
            if intent == ConversationIntent.SCHEDULE_CONSULTATION:
                return ConversationState.APPOINTMENT_SCHEDULING
            else:
                return ConversationState.INFORMATION_GATHERING
        
        elif current_state == ConversationState.APPOINTMENT_SCHEDULING:
            return ConversationState.CONFIRMATION
        
        elif current_state == ConversationState.CONFIRMATION:
            return ConversationState.ENDING
        
        elif current_state == ConversationState.REFERRAL:
            return ConversationState.ENDING
        
        elif current_state == ConversationState.EMERGENCY:
            return ConversationState.APPOINTMENT_SCHEDULING
        
        return ConversationState.INFORMATION_GATHERING
    
    def get_state_appropriate_response(self, state: ConversationState, context: ConversationContext) -> str:
        """Get response appropriate for current conversation state"""
        
        if state == ConversationState.GREETING:
            return "Thank you for calling Ted Law, the next-generation personal injury law firm. This is Alex. How can I help you today?"
        
        elif state == ConversationState.INFORMATION_GATHERING:
            if not context.case_type:
                return "I'd like to help you with your case. Could you tell me what type of accident or injury you're dealing with?"
            elif not context.client_name:
                return "Thank you for sharing that information. Could you tell me your name?"
            else:
                return "I'm gathering information about your case to better assist you. Could you tell me when this incident occurred?"
        
        elif state == ConversationState.QUALIFICATION:
            return "Based on what you've told me, I believe we can help you with your case. We offer completely free consultations with no obligation."
        
        elif state == ConversationState.APPOINTMENT_SCHEDULING:
            return "I'd be happy to schedule your free consultation. We can meet in person, over the phone, or virtually - whatever works best for you."
        
        elif state == ConversationState.CONFIRMATION:
            return "Perfect! I've scheduled your consultation. You'll receive confirmation details shortly. Is there anything else you'd like to know?"
        
        elif state == ConversationState.REFERRAL:
            return "I understand you're looking for legal help, but we specialize in personal injury cases. I'd be happy to suggest some resources to help you find the right attorney."
        
        elif state == ConversationState.EMERGENCY:
            return "I understand this is urgent. Let me connect you immediately with an attorney who can help you right away."
        
        elif state == ConversationState.ENDING:
            return "Thank you for calling Ted Law. We appreciate you considering us for your legal needs. Have a great day!"
        
        return "How can I help you with your case today?"
    
    def update_context(self, session_id: str, updates: Dict[str, Any]) -> None:
        """Update conversation context with new information"""
        if session_id in self.conversation_contexts:
            context = self.conversation_contexts[session_id]
            
            for key, value in updates.items():
                if hasattr(context, key):
                    setattr(context, key, value)
    
    def get_context(self, session_id: str) -> Optional[ConversationContext]:
        """Get conversation context for a session"""
        return self.conversation_contexts.get(session_id)
    
    def end_conversation(self, session_id: str) -> None:
        """End conversation and clean up context"""
        if session_id in self.conversation_contexts:
            del self.conversation_contexts[session_id]
    
    def track_topic(self, session_id: str, topic: str) -> None:
        """Track topics discussed in conversation"""
        if session_id in self.conversation_contexts:
            self.conversation_contexts[session_id].previous_topics.append(topic)
    
    def get_missing_information(self, session_id: str) -> List[str]:
        """Get list of information still needed from client"""
        if session_id in self.conversation_contexts:
            context = self.conversation_contexts[session_id]
            missing = []
            
            if not context.case_type:
                missing.append("case_type")
            if not context.client_name:
                missing.append("client_name")
            if not context.urgency_level:
                missing.append("urgency_level")
            
            return missing
        
        return []
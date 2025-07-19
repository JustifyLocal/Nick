"""
AI Handler for Ted Sink Law Voice Receptionist
Integrates with OpenAI GPT-4 for intelligent conversation responses
"""
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

import openai
from openai import OpenAI

from config.settings import settings
from ai_engine.conversation_manager import ConversationManager, ConversationState, CaseType


class AIHandler:
    """
    Handles AI interactions using OpenAI GPT-4 with Ted Sink Law's brand voice
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.conversation_manager = ConversationManager()
        self.logger = logging.getLogger(__name__)
        
    def generate_response(self, user_input: str, conversation_context: Optional[Dict] = None) -> Dict:
        """
        Generate AI response based on user input and conversation context
        """
        try:
            # Update conversation state based on user input
            self._update_conversation_state(user_input)
            
            # Build the complete prompt
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(user_input, conversation_context)
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Extract structured data from response
            extracted_data = self._extract_structured_data(user_input, ai_response)
            
            # Update lead data with extracted information
            self._update_lead_data(extracted_data)
            
            # Prepare response with metadata
            response_data = {
                "response": ai_response,
                "conversation_state": self.conversation_manager.current_state.value,
                "extracted_data": extracted_data,
                "next_actions": self._determine_next_actions(),
                "confidence_score": self._calculate_confidence_score(user_input, ai_response)
            }
            
            # Log conversation turn
            self._log_conversation_turn(user_input, ai_response, response_data)
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"Error generating AI response: {str(e)}")
            return self._generate_fallback_response(user_input)
    
    def _build_system_prompt(self) -> str:
        """Build the complete system prompt for the AI"""
        brand_prompt = self.conversation_manager.get_brand_prompt()
        state_prompt = self.conversation_manager.get_state_prompt(self.conversation_manager.current_state)
        
        return f"""
{brand_prompt}

{state_prompt}

CURRENT CONVERSATION STATE: {self.conversation_manager.current_state.value}

CONVERSATION HISTORY:
{self._format_conversation_history()}

LEAD DATA COLLECTED SO FAR:
{self._format_lead_data()}

RESPONSE GUIDELINES:
1. Always maintain Ted Sink Law's confident, empathetic brand voice
2. Use brand keywords naturally in conversation
3. Be proactive in offering solutions and next steps
4. Collect information conversationally without being intrusive
5. Emphasize free consultation and same-day response guarantee
6. Handle emergencies with immediate attention and urgency
7. Professionally disqualify cases that don't meet criteria
8. Keep responses concise but comprehensive
9. Always end with a clear next step or question

STRUCTURED DATA EXTRACTION:
After your response, include a JSON block with any extracted information:
{{
    "name": "extracted name if mentioned",
    "phone": "extracted phone if mentioned", 
    "email": "extracted email if mentioned",
    "incident_date": "extracted date if mentioned",
    "incident_location": "extracted location if mentioned",
    "case_type": "extracted case type if mentioned",
    "injury_details": "extracted injury details if mentioned",
    "medical_treatment": "extracted medical info if mentioned",
    "urgency_level": "low/medium/high based on context",
    "office_preference": "extracted office preference if mentioned"
}}
"""
    
    def _build_user_prompt(self, user_input: str, conversation_context: Optional[Dict]) -> str:
        """Build the user prompt with context"""
        prompt = f"Caller says: {user_input}"
        
        if conversation_context:
            prompt += f"\n\nAdditional context: {json.dumps(conversation_context)}"
        
        return prompt
    
    def _update_conversation_state(self, user_input: str):
        """Update conversation state based on user input and current state"""
        current_state = self.conversation_manager.current_state
        
        # Detect emergency situations
        if self.conversation_manager.detect_emergency(user_input):
            self.conversation_manager.current_state = ConversationState.EMERGENCY_HANDLING
            return
        
        # State transition logic
        if current_state == ConversationState.GREETING:
            case_type, _ = self.conversation_manager.analyze_case_type(user_input)
            if case_type == CaseType.DISQUALIFIED:
                self.conversation_manager.current_state = ConversationState.DISQUALIFICATION
            elif case_type == CaseType.PERSONAL_INJURY:
                self.conversation_manager.current_state = ConversationState.CASE_SCREENING
            else:
                self.conversation_manager.current_state = ConversationState.CASE_SCREENING
                
        elif current_state == ConversationState.CASE_SCREENING:
            # Check for jurisdiction information
            if any(location_indicator in user_input.lower() for location_indicator in 
                   ["south carolina", "georgia", "charleston", "atlanta", "columbia", "greenville"]):
                self.conversation_manager.current_state = ConversationState.JURISDICTION_CHECK
            else:
                self.conversation_manager.current_state = ConversationState.INTAKE_COLLECTION
                
        elif current_state == ConversationState.JURISDICTION_CHECK:
            if self.conversation_manager.check_jurisdiction(user_input):
                self.conversation_manager.current_state = ConversationState.INTAKE_COLLECTION
            else:
                self.conversation_manager.current_state = ConversationState.DISQUALIFICATION
                
        elif current_state == ConversationState.INTAKE_COLLECTION:
            # Check if we have enough information to proceed to booking
            if self._has_sufficient_intake_data():
                self.conversation_manager.current_state = ConversationState.CONSULTATION_BOOKING
                
        elif current_state == ConversationState.CONSULTATION_BOOKING:
            if "confirm" in user_input.lower() or "yes" in user_input.lower():
                self.conversation_manager.current_state = ConversationState.FOLLOW_UP
    
    def _extract_structured_data(self, user_input: str, ai_response: str) -> Dict:
        """Extract structured data from user input and AI response"""
        extracted_data = {}
        
        # Extract contact information
        extracted_data.update(self._extract_contact_info(user_input))
        
        # Extract incident information
        extracted_data.update(self._extract_incident_info(user_input))
        
        # Extract case type and urgency
        case_type, case_info = self.conversation_manager.analyze_case_type(user_input)
        if case_type == CaseType.PERSONAL_INJURY:
            extracted_data["case_type"] = case_info
            extracted_data["urgency_level"] = self._assess_urgency_level(user_input)
        
        # Extract office preference
        office_pref = self._extract_office_preference(user_input)
        if office_pref:
            extracted_data["office_preference"] = office_pref
        
        return extracted_data
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information from text"""
        import re
        
        contact_info = {}
        
        # Extract phone numbers
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info["phone"] = phones[0]
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info["email"] = emails[0]
        
        # Extract names (simple pattern)
        name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        names = re.findall(name_pattern, text)
        if names:
            contact_info["name"] = names[0]
        
        return contact_info
    
    def _extract_incident_info(self, text: str) -> Dict:
        """Extract incident information from text"""
        import re
        
        incident_info = {}
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',
            r'\b(?:yesterday|today|last week|last month)\b'
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, text, re.IGNORECASE)
            if dates:
                incident_info["incident_date"] = dates[0]
                break
        
        # Extract locations
        location_indicators = ["in", "at", "near", "around", "on"]
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in location_indicators and i + 1 < len(words):
                location = " ".join(words[i+1:i+3])
                if any(city in location.lower() for city in ["charleston", "atlanta", "columbia", "greenville", "myrtle beach", "aiken"]):
                    incident_info["incident_location"] = location
                    break
        
        return incident_info
    
    def _extract_office_preference(self, text: str) -> Optional[str]:
        """Extract office preference from text"""
        text_lower = text.lower()
        
        office_mapping = {
            "north charleston": "north_charleston",
            "charleston": "north_charleston",
            "greenville": "greenville", 
            "myrtle beach": "myrtle_beach",
            "columbia": "columbia",
            "aiken": "aiken",
            "atlanta": "atlanta"
        }
        
        for office_name, office_key in office_mapping.items():
            if office_name in text_lower:
                return office_key
        
        return None
    
    def _assess_urgency_level(self, text: str) -> str:
        """Assess urgency level based on text content"""
        text_lower = text.lower()
        
        high_urgency_indicators = [
            "emergency", "urgent", "severe", "critical", "immediate",
            "hospital", "ambulance", "life-threatening", "serious injury"
        ]
        
        medium_urgency_indicators = [
            "pain", "hurt", "injury", "accident", "broken", "fracture",
            "medical treatment", "doctor", "emergency room"
        ]
        
        if any(indicator in text_lower for indicator in high_urgency_indicators):
            return "high"
        elif any(indicator in text_lower for indicator in medium_urgency_indicators):
            return "medium"
        else:
            return "low"
    
    def _has_sufficient_intake_data(self) -> bool:
        """Check if we have sufficient intake data to proceed to booking"""
        lead_data = self.conversation_manager.lead_data
        
        # Minimum required fields
        required_fields = ["name", "phone", "incident_date", "case_type"]
        
        return all(getattr(lead_data, field) is not None for field in required_fields)
    
    def _update_lead_data(self, extracted_data: Dict):
        """Update lead data with extracted information"""
        for field, value in extracted_data.items():
            if value and hasattr(self.conversation_manager.lead_data, field):
                self.conversation_manager.update_lead_data("", field, value)
    
    def _determine_next_actions(self) -> List[str]:
        """Determine next actions based on current state"""
        current_state = self.conversation_manager.current_state
        
        action_mapping = {
            ConversationState.GREETING: ["Collect case type", "Assess urgency"],
            ConversationState.CASE_SCREENING: ["Verify jurisdiction", "Collect incident details"],
            ConversationState.JURISDICTION_CHECK: ["Confirm location", "Check timeline"],
            ConversationState.INTAKE_COLLECTION: ["Collect contact info", "Gather injury details"],
            ConversationState.CONSULTATION_BOOKING: ["Schedule consultation", "Confirm details"],
            ConversationState.EMERGENCY_HANDLING: ["Immediate scheduling", "Urgent follow-up"],
            ConversationState.DISQUALIFICATION: ["Provide referrals", "End conversation"],
            ConversationState.FOLLOW_UP: ["Confirm booking", "Provide next steps"]
        }
        
        return action_mapping.get(current_state, [])
    
    def _calculate_confidence_score(self, user_input: str, ai_response: str) -> float:
        """Calculate confidence score for the response"""
        # Simple confidence scoring based on response length and content
        base_score = 0.5
        
        # Boost for comprehensive responses
        if len(ai_response) > 100:
            base_score += 0.2
        
        # Boost for brand keywords
        brand_keywords_found = sum(1 for keyword in settings.brand_keywords if keyword.lower() in ai_response.lower())
        base_score += min(brand_keywords_found * 0.1, 0.3)
        
        # Boost for clear next steps
        if any(phrase in ai_response.lower() for phrase in ["can schedule", "free consultation", "same day", "next step"]):
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for prompt"""
        if not self.conversation_manager.conversation_history:
            return "No previous conversation turns."
        
        history = []
        for turn in self.conversation_manager.conversation_history[-5:]:  # Last 5 turns
            history.append(f"Caller: {turn.get('user_input', '')}")
            history.append(f"AI: {turn.get('ai_response', '')}")
        
        return "\n".join(history)
    
    def _format_lead_data(self) -> str:
        """Format lead data for prompt"""
        lead_data = self.conversation_manager.lead_data
        formatted_data = []
        
        for field, value in lead_data.__dict__.items():
            if value is not None:
                formatted_data.append(f"{field}: {value}")
        
        return "\n".join(formatted_data) if formatted_data else "No data collected yet."
    
    def _log_conversation_turn(self, user_input: str, ai_response: str, response_data: Dict):
        """Log conversation turn for analysis"""
        turn_data = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response,
            "state": self.conversation_manager.current_state.value,
            "confidence": response_data["confidence_score"]
        }
        
        self.conversation_manager.conversation_history.append(turn_data)
        self.conversation_manager.turn_count += 1
        
        self.logger.info(f"Conversation turn {self.conversation_manager.turn_count}: {turn_data}")
    
    def _generate_fallback_response(self, user_input: str) -> Dict:
        """Generate fallback response when AI fails"""
        fallback_response = (
            "I apologize for the technical difficulty. Let me help you with your personal injury case. "
            "We offer completely free consultations with no obligation. Could you tell me a bit about "
            "what happened and where the incident occurred?"
        )
        
        return {
            "response": fallback_response,
            "conversation_state": "fallback",
            "extracted_data": {},
            "next_actions": ["Collect basic information", "Assess case type"],
            "confidence_score": 0.3
        }
    
    def get_conversation_summary(self) -> Dict:
        """Get complete conversation summary"""
        return self.conversation_manager.get_conversation_summary()
    
    def reset_conversation(self):
        """Reset conversation for new caller"""
        self.conversation_manager.reset_conversation()
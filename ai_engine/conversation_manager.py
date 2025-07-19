"""
Core conversation manager for Ted Sink Law Voice Receptionist AI
Handles brand voice, lead qualification, and operational procedures
"""
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from config.settings import settings


class ConversationState(Enum):
    GREETING = "greeting"
    CASE_SCREENING = "case_screening"
    JURISDICTION_CHECK = "jurisdiction_check"
    INTAKE_COLLECTION = "intake_collection"
    CONSULTATION_BOOKING = "consultation_booking"
    EMERGENCY_HANDLING = "emergency_handling"
    DISQUALIFICATION = "disqualification"
    FOLLOW_UP = "follow_up"


class CaseType(Enum):
    PERSONAL_INJURY = "personal_injury"
    DISQUALIFIED = "disqualified"
    UNCLEAR = "unclear"


@dataclass
class LeadData:
    """Data structure for lead information"""
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


class ConversationManager:
    """
    Manages AI conversations with Ted Sink Law's brand voice and procedures
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conversation_history: List[Dict] = []
        self.current_state = ConversationState.GREETING
        self.lead_data = LeadData()
        self.turn_count = 0
        self.start_time = datetime.now()
        
    def get_brand_prompt(self) -> str:
        """Generate the core brand prompt for Ted Sink Law"""
        return f"""
You are the voice receptionist for {settings.firm_name}, a next-generation personal injury law firm founded in {settings.firm_founded} by {settings.founder}.

BRAND PERSONALITY:
- Confident, empathetic, and results-oriented
- Technology-forward with personal connection
- "iPhone of law firms" - sleek, modern, user-friendly
- David vs. Goliath positioning against large corporations

CORE MESSAGING:
- "Next-generation law firm with 21st century technology"
- "We won't back down from a fight"
- "No fee unless we win"
- "Helping take people from one of the worst days of their lives to one of the best days"

SERVICE STANDARDS:
- Completely free consultations with no obligation
- Same-day attorney or case manager response guaranteed
- 30-day satisfaction guarantee
- 24/7 availability
- Multiple consultation formats: phone, in-person, virtual, home/hospital visits

GEOGRAPHIC COVERAGE:
- South Carolina and Georgia only
- Offices in: {', '.join([office['name'] for office in settings.offices.values()])}

PRACTICE AREAS (Personal Injury Only):
{', '.join(settings.practice_areas)}

DISQUALIFYING CASES:
{', '.join(settings.disqualifying_cases)}

CONVERSATION STYLE:
- Warm, professional, and confident
- Use brand keywords naturally
- Emphasize technology and personal attention
- Be empathetic to injury situations
- Clear and direct communication
- Proactive in offering solutions

ESSENTIAL SCRIPTS:
- "Thank you for calling Ted Law, the next-generation personal injury law firm. This is [AI name]. How can I help you today?"
- "We offer completely free consultations with no obligation, and we don't charge any fees unless we win your case."
- "I can schedule you for a free consultation today - we guarantee you'll speak with an attorney or case manager the same day."
- "We handle all types of personal injury cases throughout South Carolina and Georgia."

Your goal is to efficiently qualify leads, collect essential information, and schedule consultations while maintaining Ted Sink Law's exceptional client service standards.
"""
    
    def get_state_prompt(self, state: ConversationState) -> str:
        """Get specific prompts for each conversation state"""
        state_prompts = {
            ConversationState.GREETING: """
GREETING PHASE:
- Welcome caller warmly with brand introduction
- Establish personal injury focus immediately
- Offer free consultation availability
- Ask how you can help them today
- Use confident, empathetic tone
""",
            
            ConversationState.CASE_SCREENING: """
CASE SCREENING PHASE:
- Determine if this is a personal injury case
- Identify specific case type from practice areas
- Assess urgency and severity
- Screen for disqualifying factors
- Collect basic incident information
- Be empathetic to injury situations
""",
            
            ConversationState.JURISDICTION_CHECK: """
JURISDICTION CHECK PHASE:
- Confirm incident occurred in South Carolina or Georgia
- Verify timeline (within statute of limitations)
- If outside jurisdiction, explain coverage limitations
- Offer referrals if appropriate
- Maintain professional, helpful tone
""",
            
            ConversationState.INTAKE_COLLECTION: """
INTAKE COLLECTION PHASE:
- Collect essential contact information
- Gather detailed incident circumstances
- Document injury details and medical treatment
- Record insurance information
- Assess damages and liability
- Maintain conversational, non-intrusive approach
""",
            
            ConversationState.CONSULTATION_BOOKING: """
CONSULTATION BOOKING PHASE:
- Offer multiple consultation formats
- Suggest optimal timing (same-day availability)
- Confirm office preference or virtual option
- Emphasize free consultation with no obligation
- Explain same-day response guarantee
- Provide clear next steps
""",
            
            ConversationState.EMERGENCY_HANDLING: """
EMERGENCY HANDLING PHASE:
- Recognize urgent situations immediately
- Offer immediate consultation scheduling
- Suggest home or hospital visits if needed
- Emphasize 24/7 availability
- Provide immediate contact options
- Maintain calm, reassuring tone
""",
            
            ConversationState.DISQUALIFICATION: """
DISQUALIFICATION PHASE:
- Professionally explain why case doesn't qualify
- Provide honest assessment with empathy
- Offer appropriate referrals if possible
- Maintain positive firm representation
- Thank caller for considering Ted Sink Law
""",
            
            ConversationState.FOLLOW_UP: """
FOLLOW-UP PHASE:
- Confirm all collected information
- Reiterate consultation details
- Explain next steps and timeline
- Emphasize same-day response guarantee
- Provide contact information for questions
- End conversation warmly and professionally
"""
        }
        return state_prompts.get(state, "")
    
    def analyze_case_type(self, user_input: str) -> Tuple[CaseType, str]:
        """Analyze user input to determine case type and extract key information"""
        input_lower = user_input.lower()
        
        # Check for disqualifying cases
        for disqualifying in settings.disqualifying_cases:
            if disqualifying.lower() in input_lower:
                return CaseType.DISQUALIFIED, f"Case involves {disqualifying}"
        
        # Check for personal injury cases
        injury_indicators = [
            "accident", "injury", "hurt", "damaged", "collision", "crash",
            "slip", "fall", "medical malpractice", "wrongful death",
            "workers comp", "workers compensation", "premises liability"
        ]
        
        case_matches = []
        for indicator in injury_indicators:
            if indicator in input_lower:
                case_matches.append(indicator)
        
        if case_matches:
            return CaseType.PERSONAL_INJURY, f"Personal injury case detected: {', '.join(case_matches)}"
        
        return CaseType.UNCLEAR, "Case type unclear, need more information"
    
    def check_jurisdiction(self, location: str) -> bool:
        """Check if location is within service area"""
        location_lower = location.lower()
        service_states_lower = [state.lower() for state in settings.service_states]
        
        for state in service_states_lower:
            if state in location_lower:
                return True
        
        # Check for common city names in SC/GA
        sc_cities = ["charleston", "columbia", "greenville", "myrtle beach", "aiken", "spartanburg"]
        ga_cities = ["atlanta", "savannah", "augusta", "columbus", "macon", "athens"]
        
        for city in sc_cities + ga_cities:
            if city in location_lower:
                return True
        
        return False
    
    def detect_emergency(self, user_input: str) -> bool:
        """Detect emergency situations in user input"""
        input_lower = user_input.lower()
        
        for keyword in settings.emergency_keywords:
            if keyword in input_lower:
                return True
        
        return False
    
    def update_lead_data(self, user_input: str, field: str, value: str):
        """Update lead data with extracted information"""
        setattr(self.lead_data, field, value)
        self.logger.info(f"Updated lead data: {field} = {value}")
    
    def get_conversation_summary(self) -> Dict:
        """Generate conversation summary for follow-up"""
        return {
            "conversation_id": f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "start_time": self.start_time.isoformat(),
            "duration_minutes": (datetime.now() - self.start_time).total_seconds() / 60,
            "turns": self.turn_count,
            "final_state": self.current_state.value,
            "lead_data": {
                k: v for k, v in self.lead_data.__dict__.items() 
                if v is not None
            },
            "qualification_status": "qualified" if self.current_state != ConversationState.DISQUALIFICATION else "disqualified"
        }
    
    def reset_conversation(self):
        """Reset conversation for new caller"""
        self.conversation_history = []
        self.current_state = ConversationState.GREETING
        self.lead_data = LeadData()
        self.turn_count = 0
        self.start_time = datetime.now()
        self.logger.info("Conversation reset for new caller")
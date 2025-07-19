"""
Lead Qualification Module for Ted Sink Law

Screens potential clients and cases to determine eligibility based on
Ted Sink Law's practice areas, geographic coverage, and qualification criteria.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import re

from ..data.firm_info import TedSinkLawInfo
from ..data.practice_areas import TedSinkLawPracticeAreas, PracticeArea
from ..data.client_standards import TedSinkLawClientStandards

class QualificationStatus(Enum):
    """Lead qualification status"""
    QUALIFIED = "qualified"
    NOT_QUALIFIED = "not_qualified"
    NEEDS_MORE_INFO = "needs_more_info"
    EMERGENCY = "emergency"
    REFERRAL_NEEDED = "referral_needed"

class CasePriority(Enum):
    """Case priority levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    EMERGENCY = "emergency"

@dataclass
class LeadInfo:
    """Information collected about a potential lead"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    case_type: Optional[str] = None
    incident_date: Optional[str] = None
    injuries: Optional[str] = None
    medical_treatment: Optional[str] = None
    insurance_info: Optional[str] = None
    previous_attorney: Optional[str] = None
    urgency_level: Optional[str] = None
    additional_notes: Optional[str] = None

@dataclass
class QualificationResult:
    """Result of lead qualification process"""
    status: QualificationStatus
    priority: CasePriority
    practice_area: Optional[PracticeArea]
    reasoning: List[str]
    next_steps: List[str]
    disqualification_reason: Optional[str] = None
    referral_suggestions: List[str] = None

class TedSinkLawLeadQualifier:
    """Lead qualification system for Ted Sink Law"""
    
    # QUALIFICATION CRITERIA
    QUALIFICATION_CRITERIA = {
        "geographic": {
            "required": ["South Carolina", "Georgia"],
            "disqualifying": ["All other states"],
            "description": "Must be resident of South Carolina or Georgia"
        },
        "case_type": {
            "required": "Personal injury cases only",
            "disqualifying": [
                "criminal", "family law", "business law", "real estate",
                "estate planning", "bankruptcy", "immigration"
            ],
            "description": "Must be personal injury case"
        },
        "timeline": {
            "required": "Within statute of limitations",
            "disqualifying": "Outside statute of limitations",
            "description": "Case must be within legal time limits"
        },
        "damages": {
            "required": "Significant damages or medical treatment",
            "disqualifying": "Minimal or no damages",
            "description": "Must have meaningful damages to pursue"
        },
        "liability": {
            "required": "Clear liability or strong case",
            "disqualifying": "Unclear liability or weak case",
            "description": "Must have reasonable chance of success"
        }
    }
    
    # EMERGENCY INDICATORS
    EMERGENCY_INDICATORS = [
        "hospital", "emergency room", "ER", "ambulance",
        "severe injury", "critical condition", "life-threatening",
        "immediate", "urgent", "emergency", "serious accident",
        "broken bones", "head injury", "trauma", "surgery"
    ]
    
    # HIGH PRIORITY CASE INDICATORS
    HIGH_PRIORITY_INDICATORS = [
        "wrongful death", "fatal", "death", "serious injury",
        "permanent disability", "significant medical bills",
        "lost wages", "pain and suffering", "emotional distress",
        "truck accident", "motorcycle accident", "pedestrian accident"
    ]
    
    # DISQUALIFICATION KEYWORDS
    DISQUALIFICATION_KEYWORDS = {
        "geographic": ["florida", "north carolina", "tennessee", "alabama", "virginia"],
        "case_type": ["divorce", "custody", "criminal", "business", "real estate", "bankruptcy"],
        "timeline": ["years ago", "old case", "statute expired", "too late"],
        "damages": ["minor", "small", "minimal", "no injury", "no damage"]
    }
    
    def __init__(self):
        """Initialize the lead qualifier"""
        self.firm_info = TedSinkLawInfo()
        self.practice_areas = TedSinkLawPracticeAreas()
        self.client_standards = TedSinkLawClientStandards()
    
    def qualify_lead(self, lead_info: LeadInfo) -> QualificationResult:
        """
        Qualify a potential lead based on collected information
        
        Args:
            lead_info: Information about the potential lead
            
        Returns:
            QualificationResult with status, priority, and next steps
        """
        reasoning = []
        next_steps = []
        disqualification_reason = None
        
        # Check for emergency situations first
        if self._is_emergency_case(lead_info):
            return QualificationResult(
                status=QualificationStatus.EMERGENCY,
                priority=CasePriority.EMERGENCY,
                practice_area=self._identify_practice_area(lead_info.case_type),
                reasoning=["Emergency situation detected - immediate attention required"],
                next_steps=["Immediate attorney contact", "Emergency consultation scheduling"]
            )
        
        # Geographic qualification
        if not self._qualify_geographic(lead_info.location, reasoning):
            disqualification_reason = "Geographic location outside service area"
            return QualificationResult(
                status=QualificationStatus.NOT_QUALIFIED,
                priority=CasePriority.LOW,
                practice_area=None,
                reasoning=reasoning,
                next_steps=["Provide referral to local attorney"],
                disqualification_reason=disqualification_reason,
                referral_suggestions=["Local personal injury attorney in your area"]
            )
        
        # Case type qualification
        if not self._qualify_case_type(lead_info.case_type, reasoning):
            disqualification_reason = "Case type not handled by firm"
            return QualificationResult(
                status=QualificationStatus.NOT_QUALIFIED,
                priority=CasePriority.LOW,
                practice_area=None,
                reasoning=reasoning,
                next_steps=["Provide referral to appropriate attorney"],
                disqualification_reason=disqualification_reason,
                referral_suggestions=self._get_referral_suggestions(lead_info.case_type)
            )
        
        # Timeline qualification
        if not self._qualify_timeline(lead_info.incident_date, reasoning):
            disqualification_reason = "Case outside statute of limitations"
            return QualificationResult(
                status=QualificationStatus.NOT_QUALIFIED,
                priority=CasePriority.LOW,
                practice_area=self._identify_practice_area(lead_info.case_type),
                reasoning=reasoning,
                next_steps=["Explain statute of limitations", "Provide general legal information"],
                disqualification_reason=disqualification_reason
            )
        
        # Damages qualification
        if not self._qualify_damages(lead_info.injuries, lead_info.medical_treatment, reasoning):
            disqualification_reason = "Insufficient damages to pursue case"
            return QualificationResult(
                status=QualificationStatus.NOT_QUALIFIED,
                priority=CasePriority.LOW,
                practice_area=self._identify_practice_area(lead_info.case_type),
                reasoning=reasoning,
                next_steps=["Explain damages requirements", "Provide general legal guidance"],
                disqualification_reason=disqualification_reason
            )
        
        # Determine priority
        priority = self._determine_priority(lead_info)
        
        # Identify practice area
        practice_area = self._identify_practice_area(lead_info.case_type)
        
        # Generate next steps
        next_steps = self._generate_next_steps(lead_info, priority)
        
        return QualificationResult(
            status=QualificationStatus.QUALIFIED,
            priority=priority,
            practice_area=practice_area,
            reasoning=reasoning,
            next_steps=next_steps
        )
    
    def _is_emergency_case(self, lead_info: LeadInfo) -> bool:
        """Check if case requires emergency handling"""
        if not lead_info.case_type and not lead_info.injuries and not lead_info.additional_notes:
            return False
        
        text_to_check = " ".join(filter(None, [
            lead_info.case_type or "",
            lead_info.injuries or "",
            lead_info.urgency_level or "",
            lead_info.additional_notes or ""
        ])).lower()
        
        return any(indicator in text_to_check for indicator in self.EMERGENCY_INDICATORS)
    
    def _qualify_geographic(self, location: Optional[str], reasoning: List[str]) -> bool:
        """Qualify based on geographic location"""
        if not location:
            reasoning.append("Location not provided - will need to confirm during consultation")
            return True  # Allow to proceed with more information
        
        location_lower = location.lower()
        
        # Check for disqualifying states
        for state in self.DISQUALIFICATION_KEYWORDS["geographic"]:
            if state in location_lower:
                reasoning.append(f"Location {location} is outside service area")
                return False
        
        # Check for qualifying states
        for state in self.firm_info.SERVICE_STATES:
            if state.lower() in location_lower:
                reasoning.append(f"Location {location} is within service area")
                return True
        
        # Check for city names in service states
        for office in self.firm_info.OFFICES:
            if office.city.lower() in location_lower:
                reasoning.append(f"Location {location} is within service area")
                return True
        
        reasoning.append(f"Location {location} needs verification - may be outside service area")
        return True  # Allow to proceed with verification
    
    def _qualify_case_type(self, case_type: Optional[str], reasoning: List[str]) -> bool:
        """Qualify based on case type"""
        if not case_type:
            reasoning.append("Case type not specified - will need to determine during consultation")
            return True  # Allow to proceed with more information
        
        case_lower = case_type.lower()
        
        # Check for disqualifying case types
        for keyword in self.DISQUALIFICATION_KEYWORDS["case_type"]:
            if keyword in case_lower:
                reasoning.append(f"Case type '{case_type}' is not handled by firm")
                return False
        
        # Check if it's a personal injury case
        if self.practice_areas.is_personal_injury_case(case_type):
            reasoning.append(f"Case type '{case_type}' is within firm's practice areas")
            return True
        
        reasoning.append(f"Case type '{case_type}' needs clarification - may not be personal injury")
        return True  # Allow to proceed with clarification
    
    def _qualify_timeline(self, incident_date: Optional[str], reasoning: List[str]) -> bool:
        """Qualify based on timeline and statute of limitations"""
        if not incident_date:
            reasoning.append("Incident date not provided - will need to confirm during consultation")
            return True  # Allow to proceed with more information
        
        # Check for obvious timeline issues
        incident_lower = incident_date.lower()
        for keyword in self.DISQUALIFICATION_KEYWORDS["timeline"]:
            if keyword in incident_lower:
                reasoning.append(f"Incident date '{incident_date}' suggests timeline issues")
                return False
        
        # Basic date parsing (simplified)
        try:
            # This is a simplified check - in production would need more sophisticated date parsing
            if "years ago" in incident_lower or "old" in incident_lower:
                reasoning.append("Incident appears to be too old for statute of limitations")
                return False
            
            reasoning.append(f"Incident date '{incident_date}' appears within timeline")
            return True
        except:
            reasoning.append(f"Incident date '{incident_date}' needs verification")
            return True  # Allow to proceed with verification
    
    def _qualify_damages(self, injuries: Optional[str], medical_treatment: Optional[str], reasoning: List[str]) -> bool:
        """Qualify based on damages and medical treatment"""
        if not injuries and not medical_treatment:
            reasoning.append("Injury and treatment information not provided - will need to assess during consultation")
            return True  # Allow to proceed with more information
        
        text_to_check = " ".join(filter(None, [injuries or "", medical_treatment or ""])).lower()
        
        # Check for disqualifying damage indicators
        for keyword in self.DISQUALIFICATION_KEYWORDS["damages"]:
            if keyword in text_to_check:
                reasoning.append(f"Damages appear minimal based on description")
                return False
        
        # Check for qualifying damage indicators
        if any(indicator in text_to_check for indicator in self.HIGH_PRIORITY_INDICATORS):
            reasoning.append("Significant damages indicated")
            return True
        
        reasoning.append("Damages need assessment during consultation")
        return True  # Allow to proceed with assessment
    
    def _determine_priority(self, lead_info: LeadInfo) -> CasePriority:
        """Determine case priority based on lead information"""
        if self._is_emergency_case(lead_info):
            return CasePriority.EMERGENCY
        
        text_to_check = " ".join(filter(None, [
            lead_info.case_type or "",
            lead_info.injuries or "",
            lead_info.urgency_level or "",
            lead_info.additional_notes or ""
        ])).lower()
        
        # Check for high priority indicators
        if any(indicator in text_to_check for indicator in self.HIGH_PRIORITY_INDICATORS):
            return CasePriority.HIGH
        
        # Check for medium priority (most personal injury cases)
        if lead_info.case_type and self.practice_areas.is_personal_injury_case(lead_info.case_type):
            return CasePriority.MEDIUM
        
        return CasePriority.LOW
    
    def _identify_practice_area(self, case_type: Optional[str]) -> Optional[PracticeArea]:
        """Identify the specific practice area for the case"""
        if not case_type:
            return None
        
        return self.practice_areas.find_practice_area_by_keyword(case_type)
    
    def _generate_next_steps(self, lead_info: LeadInfo, priority: CasePriority) -> List[str]:
        """Generate appropriate next steps based on qualification result"""
        next_steps = []
        
        if priority == CasePriority.EMERGENCY:
            next_steps.extend([
                "Immediate attorney contact",
                "Emergency consultation scheduling",
                "Hospital/home visit coordination if needed"
            ])
        elif priority == CasePriority.HIGH:
            next_steps.extend([
                "Same-day consultation scheduling",
                "Priority case assignment",
                "Comprehensive case evaluation"
            ])
        else:
            next_steps.extend([
                "Free consultation scheduling",
                "Case evaluation and assessment",
                "Detailed case review"
            ])
        
        # Add standard next steps
        next_steps.extend([
            "Collect complete case information",
            "Explain firm's contingency fee structure",
            "Discuss same-day response guarantee"
        ])
        
        return next_steps
    
    def _get_referral_suggestions(self, case_type: Optional[str]) -> List[str]:
        """Get referral suggestions for non-qualified cases"""
        if not case_type:
            return ["Local attorney directory", "State bar association referral service"]
        
        case_lower = case_type.lower()
        
        if "criminal" in case_lower:
            return ["Criminal defense attorney", "Public defender's office"]
        elif "family" in case_lower or "divorce" in case_lower:
            return ["Family law attorney", "Divorce attorney"]
        elif "business" in case_lower:
            return ["Business law attorney", "Corporate attorney"]
        elif "real estate" in case_lower:
            return ["Real estate attorney", "Property law attorney"]
        else:
            return ["Local attorney directory", "State bar association referral service"]
    
    def collect_lead_info(self, conversation_text: str) -> LeadInfo:
        """Extract lead information from conversation text"""
        # This is a simplified implementation
        # In production, would use NLP to extract structured information
        
        lead_info = LeadInfo()
        
        # Extract basic information using regex patterns
        # Phone number
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phone_match = re.search(phone_pattern, conversation_text)
        if phone_match:
            lead_info.phone = phone_match.group()
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, conversation_text)
        if email_match:
            lead_info.email = email_match.group()
        
        # Location (simplified)
        location_keywords = ["in", "at", "from", "near", "around"]
        words = conversation_text.split()
        for i, word in enumerate(words):
            if word.lower() in location_keywords and i + 1 < len(words):
                potential_location = words[i + 1]
                if any(state.lower() in potential_location.lower() for state in self.firm_info.SERVICE_STATES):
                    lead_info.location = potential_location
                    break
        
        return lead_info
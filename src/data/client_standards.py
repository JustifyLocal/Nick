"""
Client Service Standards Module for Ted Sink Law

Defines the firm's client service standards, guarantees, and operational protocols
that ensure exceptional client experience and professional service delivery.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum

class ServiceLevel(Enum):
    """Service level classifications"""
    STANDARD = "standard"
    URGENT = "urgent"
    EMERGENCY = "emergency"

@dataclass
class ServiceGuarantee:
    """Represents a service guarantee offered by Ted Sink Law"""
    name: str
    description: str
    terms: str
    duration: Optional[str] = None

@dataclass
class CommunicationProtocol:
    """Defines communication standards and protocols"""
    channel: str
    response_time: str
    availability: str
    description: str

class TedSinkLawClientStandards:
    """Client service standards and protocols for Ted Sink Law"""
    
    # CORE SERVICE GUARANTEES
    SERVICE_GUARANTEES = [
        ServiceGuarantee(
            name="Free Consultation Guarantee",
            description="Completely free initial consultations with no time limits or obligations",
            terms="No cost, no pressure, no obligation to hire the firm",
            duration="Unlimited"
        ),
        ServiceGuarantee(
            name="Same-Day Response Guarantee",
            description="Guaranteed same-day response from an attorney or case manager",
            terms="All inquiries receive response within 24 hours",
            duration="24 hours"
        ),
        ServiceGuarantee(
            name="30-Day Satisfaction Guarantee",
            description="If not satisfied within first 30 days, no fees are charged",
            terms="Complete refund of any fees paid if client is not satisfied",
            duration="30 days"
        ),
        ServiceGuarantee(
            name="No Fee Unless We Win",
            description="Contingency fee structure - no upfront costs",
            terms="Firm fronts all costs for medical records, police reports, and investigations",
            duration="Entire case duration"
        ),
        ServiceGuarantee(
            name="24/7 Availability",
            description="Available around the clock for urgent matters",
            terms="Emergency consultations and immediate response for urgent cases",
            duration="24/7"
        )
    ]
    
    # COMMUNICATION PROTOCOLS
    COMMUNICATION_PROTOCOLS = [
        CommunicationProtocol(
            channel="Phone",
            response_time="Immediate to 4 hours",
            availability="24/7",
            description="Primary communication channel with guaranteed response times"
        ),
        CommunicationProtocol(
            channel="Text Message",
            response_time="Within 2 hours",
            availability="Business hours + emergency",
            description="Quick updates and scheduling via text messaging"
        ),
        CommunicationProtocol(
            channel="Email",
            response_time="Within 24 hours",
            availability="Business hours",
            description="Detailed communications and document sharing"
        ),
        CommunicationProtocol(
            channel="In-Person",
            response_time="Same day scheduling",
            availability="Business hours + emergency",
            description="Face-to-face consultations at any office location"
        ),
        CommunicationProtocol(
            channel="Virtual",
            response_time="Same day scheduling",
            availability="Business hours",
            description="Video consultations for remote clients"
        )
    ]
    
    # CONSULTATION FORMATS
    CONSULTATION_FORMATS = [
        {
            "format": "Phone Consultation",
            "duration": "30-60 minutes",
            "availability": "24/7",
            "description": "Initial case review and assessment over the phone",
            "best_for": "Quick case evaluation and immediate guidance"
        },
        {
            "format": "In-Person Office Meeting",
            "duration": "60-90 minutes",
            "availability": "Business hours",
            "description": "Comprehensive consultation at any office location",
            "best_for": "Detailed case review and face-to-face discussion"
        },
        {
            "format": "Virtual Appointment",
            "duration": "45-75 minutes",
            "availability": "Business hours",
            "description": "Video consultation using modern technology",
            "best_for": "Remote clients or those unable to travel"
        },
        {
            "format": "Home Visit",
            "duration": "60-90 minutes",
            "availability": "Business hours + emergency",
            "description": "Attorney visits client at home for consultation",
            "best_for": "Injured clients unable to travel to office"
        },
        {
            "format": "Hospital Visit",
            "duration": "30-60 minutes",
            "availability": "24/7 emergency",
            "description": "Immediate consultation at hospital bedside",
            "best_for": "Severely injured clients requiring immediate attention"
        }
    ]
    
    # CLIENT SERVICE STANDARDS
    CLIENT_SERVICE_STANDARDS = {
        "initial_contact": {
            "response_time": "Immediate to 4 hours",
            "professionalism": "Warm, empathetic, and confident",
            "information_collection": "Essential case details and contact information",
            "next_steps": "Clear explanation of consultation process"
        },
        "consultation": {
            "duration": "30-90 minutes based on format",
            "content": "Case evaluation, legal options, and firm capabilities",
            "documentation": "Comprehensive case notes and action plan",
            "follow_up": "Immediate next steps and timeline"
        },
        "case_management": {
            "communication_frequency": "Weekly updates minimum",
            "accessibility": "Direct access to attorneys and case managers",
            "transparency": "Regular case status and progress updates",
            "support": "Comprehensive assistance throughout case"
        },
        "emergency_handling": {
            "response_time": "Immediate",
            "availability": "24/7",
            "protocol": "Immediate attorney contact and emergency consultation",
            "support": "Hospital visits and immediate legal guidance"
        }
    }
    
    # INTENSIVE SUPPORT PERIOD
    INTENSIVE_SUPPORT_PERIOD = {
        "duration": "30 days",
        "description": "Intensive support during the 'roughest part' of cases",
        "services": [
            "Daily check-ins if needed",
            "Immediate response to all inquiries",
            "Comprehensive case setup and documentation",
            "Medical appointment coordination",
            "Insurance communication assistance",
            "Emotional support and guidance"
        ],
        "objectives": [
            "Establish strong attorney-client relationship",
            "Ensure client feels supported and informed",
            "Begin case preparation and investigation",
            "Address immediate client concerns and needs"
        ]
    }
    
    # QUALITY ASSURANCE STANDARDS
    QUALITY_STANDARDS = {
        "professional_conduct": [
            "Maintain highest ethical standards",
            "Treat every client with respect and dignity",
            "Provide honest and realistic case assessments",
            "Maintain client confidentiality"
        ],
        "communication_quality": [
            "Clear, understandable language",
            "Regular and proactive communication",
            "Prompt response to all inquiries",
            "Comprehensive case updates"
        ],
        "case_management": [
            "Thorough case investigation",
            "Aggressive representation",
            "Regular case status reviews",
            "Strategic case planning"
        ],
        "client_satisfaction": [
            "Exceed client expectations",
            "Provide 'wow moments' in service",
            "Maintain high client satisfaction ratings",
            "Address concerns promptly and effectively"
        ]
    }
    
    # LEAD QUALIFICATION CRITERIA
    LEAD_QUALIFICATION = {
        "ideal_client_profile": {
            "case_types": "Personal injury cases with clear liability and damages",
            "geographic_area": "South Carolina and Georgia residents",
            "damages": "Significant medical treatment needs or inadequate insurance offers",
            "timeline": "Within statute of limitations",
            "motivation": "Seeking fair compensation and justice"
        },
        "disqualifying_factors": [
            "Cases outside South Carolina or Georgia",
            "Non-personal injury matters",
            "Cases with minimal damages",
            "Unclear liability situations",
            "Cases outside statute of limitations",
            "Conflict of interest situations"
        ],
        "critical_intake_information": [
            "Client contact details",
            "Incident circumstances and date",
            "Injury details and medical treatment status",
            "Insurance information",
            "Previous legal representation",
            "Timeline considerations"
        ]
    }
    
    @classmethod
    def get_service_guarantee(cls, guarantee_name: str) -> Optional[ServiceGuarantee]:
        """Get a specific service guarantee by name"""
        for guarantee in cls.SERVICE_GUARANTEES:
            if guarantee.name.lower() == guarantee_name.lower():
                return guarantee
        return None
    
    @classmethod
    def get_communication_protocol(cls, channel: str) -> Optional[CommunicationProtocol]:
        """Get communication protocol for a specific channel"""
        for protocol in cls.COMMUNICATION_PROTOCOLS:
            if protocol.channel.lower() == channel.lower():
                return protocol
        return None
    
    @classmethod
    def get_consultation_format(cls, format_name: str) -> Optional[Dict]:
        """Get consultation format details by name"""
        for format_info in cls.CONSULTATION_FORMATS:
            if format_info["format"].lower() == format_name.lower():
                return format_info
        return None
    
    @classmethod
    def is_ideal_client(cls, case_type: str, location: str, damages: str) -> bool:
        """Check if a potential client meets ideal profile criteria"""
        # Check case type
        from .practice_areas import TedSinkLawPracticeAreas
        if not TedSinkLawPracticeAreas.is_personal_injury_case(case_type):
            return False
        
        # Check geographic area
        from .firm_info import TedSinkLawInfo
        if not TedSinkLawInfo.is_service_area(location):
            return False
        
        # Check for significant damages
        damage_keywords = ["significant", "serious", "major", "extensive", "severe"]
        if not any(keyword in damages.lower() for keyword in damage_keywords):
            return False
        
        return True
    
    @classmethod
    def get_emergency_protocol(cls) -> Dict:
        """Get emergency handling protocol"""
        return {
            "immediate_response": "24/7 availability with immediate attorney contact",
            "consultation_options": ["Phone consultation", "Hospital visit", "Home visit"],
            "priority_handling": "Emergency cases receive immediate attention",
            "follow_up": "Same-day detailed consultation and case setup"
        }
    
    @classmethod
    def get_intensive_support_details(cls) -> Dict:
        """Get details about the 30-day intensive support period"""
        return cls.INTENSIVE_SUPPORT_PERIOD
"""
Ted Sink Law Firm Information Module

Contains all essential information about Ted Law: Accident & Injury Law Firm, LLC
including contact details, office locations, staff information, and operational policies.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import time

@dataclass
class OfficeLocation:
    """Represents a Ted Sink Law office location"""
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    is_primary: bool = False
    timezone: str = "America/New_York"

@dataclass
class StaffMember:
    """Represents a staff member at Ted Sink Law"""
    name: str
    title: str
    role: str
    contact_info: Optional[str] = None

class TedSinkLawInfo:
    """Central repository for all Ted Sink Law firm information"""
    
    # Firm Identity
    FIRM_NAME = "Ted Law: Accident & Injury Law Firm, LLC"
    LEGAL_NAME = "Ted Law: Accident & Injury Law Firm, LLC"
    FOUNDING_YEAR = 2019
    FOUNDER = "Ted Sink"
    FOUNDER_CREDENTIALS = [
        "Yale University",
        "Stanford Graduate School of Business", 
        "Charleston School of Law"
    ]
    
    # Brand Positioning
    BRAND_POSITIONING = "next-generation law firm"
    BRAND_TAGLINE = "The iPhone of law firms"
    BRAND_DESCRIPTION = "Sleek, modern, user-friendly, and results-oriented while maintaining genuine personal connection"
    
    # Geographic Coverage
    SERVICE_STATES = ["South Carolina", "Georgia"]
    TIMEZONE = "America/New_York"
    
    # Office Locations
    OFFICES = [
        OfficeLocation(
            name="North Charleston",
            address="1075-A E Montague Ave",
            city="North Charleston", 
            state="SC",
            zip_code="29405",
            phone="(843) 800-0000",
            is_primary=True
        ),
        OfficeLocation(
            name="Greenville",
            address="123 Main Street",  # Placeholder - actual address needed
            city="Greenville",
            state="SC", 
            zip_code="29601",
            phone="(864) 800-0000"
        ),
        OfficeLocation(
            name="Myrtle Beach",
            address="456 Ocean Blvd",  # Placeholder - actual address needed
            city="Myrtle Beach",
            state="SC",
            zip_code="29577", 
            phone="(843) 800-0000"
        ),
        OfficeLocation(
            name="Columbia",
            address="789 State Street",  # Placeholder - actual address needed
            city="Columbia",
            state="SC",
            zip_code="29201",
            phone="(803) 800-0000"
        ),
        OfficeLocation(
            name="Aiken",
            address="321 Laurens Street",  # Placeholder - actual address needed
            city="Aiken", 
            state="SC",
            zip_code="29801",
            phone="(803) 800-0000"
        ),
        OfficeLocation(
            name="Atlanta",
            address="654 Peachtree Street",  # Placeholder - actual address needed
            city="Atlanta",
            state="GA",
            zip_code="30308",
            phone="(404) 800-0000"
        )
    ]
    
    # Staff Information
    STAFF = [
        StaffMember(
            name="Ted Sink",
            title="Founder & Managing Attorney",
            role="Managing attorney, case strategy, client relations"
        ),
        StaffMember(
            name="Laura",
            title="Senior Attorney",
            role="Legal staff, case management, client representation"
        ),
        StaffMember(
            name="Kevin",
            title="Support Staff",
            role="Administrative support, case coordination"
        ),
        StaffMember(
            name="Angela Grunwald",
            title="Client Services & Intake Coordinator",
            role="Client intake, case coordination, client communication"
        )
    ]
    
    # Operational Policies
    AVAILABILITY = "24/7"
    RESPONSE_TIME = "Same-day guaranteed"
    CONSULTATION_FEE = "Completely free"
    FEE_STRUCTURE = "Contingency basis - no fee unless we win"
    SATISFACTION_GUARANTEE = "30-day satisfaction guarantee"
    
    # Consultation Formats
    CONSULTATION_FORMATS = [
        "Phone consultations",
        "In-person meetings at any office",
        "Virtual appointments",
        "Home visits for injured clients",
        "Hospital visits for injured clients"
    ]
    
    # Awards and Recognition
    AWARDS = [
        "5-star ratings across multiple platforms",
        "Client Choice Award from Avvo",
        "Recognition from major media outlets"
    ]
    
    # Notable Results
    NOTABLE_CASE = {
        "description": "Converted $35,000 offer to $2,250,000 settlement",
        "demonstrates": "Proven results and negotiation expertise"
    }
    
    @classmethod
    def get_primary_office(cls) -> OfficeLocation:
        """Get the primary office location"""
        return next(office for office in cls.OFFICES if office.is_primary)
    
    @classmethod
    def get_office_by_city(cls, city: str) -> Optional[OfficeLocation]:
        """Get office location by city name"""
        for office in cls.OFFICES:
            if office.city.lower() == city.lower():
                return office
        return None
    
    @classmethod
    def get_office_by_state(cls, state: str) -> List[OfficeLocation]:
        """Get all offices in a specific state"""
        return [office for office in cls.OFFICES if office.state.lower() == state.lower()]
    
    @classmethod
    def is_service_area(cls, state: str) -> bool:
        """Check if a state is in the service area"""
        return state.lower() in [s.lower() for s in cls.SERVICE_STATES]
    
    @classmethod
    def get_contact_info(cls) -> Dict[str, str]:
        """Get primary contact information"""
        primary_office = cls.get_primary_office()
        return {
            "firm_name": cls.FIRM_NAME,
            "phone": primary_office.phone,
            "address": f"{primary_office.address}, {primary_office.city}, {primary_office.state} {primary_office.zip_code}",
            "availability": cls.AVAILABILITY,
            "response_time": cls.RESPONSE_TIME
        }
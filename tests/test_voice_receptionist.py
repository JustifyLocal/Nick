"""
Test Suite for Ted Sink Law Voice Receptionist AI

Comprehensive tests for all components of the voice receptionist system
including brand personality, lead qualification, appointment scheduling,
and emergency handling.
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch

from src.core.voice_receptionist import TedSinkLawVoiceReceptionist, CallSession
from src.core.brand_personality import TedSinkLawBrandPersonality
from src.qualification.lead_qualifier import TedSinkLawLeadQualifier, LeadInfo, QualificationResult, QualificationStatus, CasePriority
from src.scheduling.appointment_scheduler import AppointmentScheduler
from src.scheduling.emergency_handler import EmergencyHandler
from src.data.firm_info import TedSinkLawInfo
from src.data.practice_areas import TedSinkLawPracticeAreas
from src.data.client_standards import TedSinkLawClientStandards

class TestTedSinkLawVoiceReceptionist:
    """Test cases for the main voice receptionist AI"""
    
    @pytest.fixture
    def receptionist(self):
        """Create a voice receptionist instance for testing"""
        return TedSinkLawVoiceReceptionist()
    
    @pytest.fixture
    def sample_session_id(self):
        """Sample session ID for testing"""
        return "test_session_123"
    
    @pytest.mark.asyncio
    async def test_handle_call(self, receptionist, sample_session_id):
        """Test call handling initialization"""
        greeting = await receptionist.handle_call(sample_session_id)
        
        # Check that greeting is generated
        assert greeting is not None
        assert "Ted Law" in greeting
        assert "Alex" in greeting
        
        # Check that session is created
        session = receptionist.get_session_info(sample_session_id)
        assert session is not None
        assert session.session_id == sample_session_id
        assert len(session.conversation_history) > 0
    
    @pytest.mark.asyncio
    async def test_process_client_response_qualified(self, receptionist, sample_session_id):
        """Test processing qualified client response"""
        # Start call
        await receptionist.handle_call(sample_session_id)
        
        # Process qualified client response
        client_message = "I was in a car accident in Charleston, South Carolina. I have serious injuries and need help."
        response = await receptionist.process_client_response(sample_session_id, client_message)
        
        # Check response
        assert response is not None
        assert "free consultation" in response.lower()
        assert "no obligation" in response.lower()
        
        # Check session state
        session = receptionist.get_session_info(sample_session_id)
        assert session.qualification_result is not None
        assert session.qualification_result.status == QualificationStatus.QUALIFIED
    
    @pytest.mark.asyncio
    async def test_process_client_response_not_qualified(self, receptionist, sample_session_id):
        """Test processing non-qualified client response"""
        # Start call
        await receptionist.handle_call(sample_session_id)
        
        # Process non-qualified client response
        client_message = "I need help with a divorce case in Florida."
        response = await receptionist.process_client_response(sample_session_id, client_message)
        
        # Check response
        assert response is not None
        assert "specialize" in response.lower() or "personal injury" in response.lower()
        
        # Check session state
        session = receptionist.get_session_info(sample_session_id)
        assert session.qualification_result is not None
        assert session.qualification_result.status == QualificationStatus.NOT_QUALIFIED
    
    @pytest.mark.asyncio
    async def test_emergency_handling(self, receptionist, sample_session_id):
        """Test emergency situation handling"""
        # Start call
        await receptionist.handle_call(sample_session_id)
        
        # Process emergency client response
        client_message = "I'm in the hospital with serious injuries from a truck accident. This is urgent!"
        response = await receptionist.process_client_response(sample_session_id, client_message)
        
        # Check response
        assert response is not None
        assert "urgent" in response.lower() or "immediate" in response.lower()
        assert "attorney" in response.lower()
        
        # Check session state
        session = receptionist.get_session_info(sample_session_id)
        assert session.emergency_handled is True
    
    @pytest.mark.asyncio
    async def test_appointment_scheduling(self, receptionist, sample_session_id):
        """Test appointment scheduling"""
        # Start call and qualify client
        await receptionist.handle_call(sample_session_id)
        client_message = "I was in a car accident in Atlanta, Georgia. I have injuries and need help."
        await receptionist.process_client_response(sample_session_id, client_message)
        
        # Schedule appointment
        appointment_preferences = {
            "format": "phone",
            "name": "John Doe",
            "phone": "555-123-4567"
        }
        
        confirmation = await receptionist.schedule_appointment(sample_session_id, appointment_preferences)
        
        # Check confirmation
        assert confirmation is not None
        assert "scheduled" in confirmation.lower() or "consultation" in confirmation.lower()
        
        # Check session state
        session = receptionist.get_session_info(sample_session_id)
        assert session.appointment_scheduled is True
    
    @pytest.mark.asyncio
    async def test_end_call(self, receptionist, sample_session_id):
        """Test call ending"""
        # Start call and qualify client
        await receptionist.handle_call(sample_session_id)
        client_message = "I was in a car accident in Charleston, South Carolina."
        await receptionist.process_client_response(sample_session_id, client_message)
        
        # End call
        ending_message = await receptionist.end_call(sample_session_id)
        
        # Check ending message
        assert ending_message is not None
        assert "thank you" in ending_message.lower()
        
        # Check that session is cleaned up
        session = receptionist.get_session_info(sample_session_id)
        assert session is None

class TestBrandPersonality:
    """Test cases for brand personality module"""
    
    @pytest.fixture
    def brand_personality(self):
        """Create brand personality instance for testing"""
        return TedSinkLawBrandPersonality()
    
    def test_get_personality_profile(self, brand_personality):
        """Test personality profile retrieval"""
        profile = brand_personality.get_personality_profile()
        
        assert profile.name == "Alex"
        assert len(profile.traits) > 0
        assert len(profile.key_phrases) > 0
        assert len(profile.conversation_starters) > 0
    
    def test_get_conversation_starter(self, brand_personality):
        """Test conversation starter generation"""
        # Standard starter
        starter = brand_personality.get_conversation_starter()
        assert "Ted Law" in starter
        assert "Alex" in starter
        
        # Emergency starter
        emergency_starter = brand_personality.get_conversation_starter("emergency")
        assert "urgent" in emergency_starter.lower()
    
    def test_get_empathy_response(self, brand_personality):
        """Test empathy response generation"""
        response = brand_personality.get_empathy_response("severe_injury")
        assert "sorry" in response.lower() or "difficult" in response.lower()
        
        response = brand_personality.get_empathy_response("financial_stress")
        assert "financial" in response.lower() or "strain" in response.lower()
    
    def test_is_brand_aligned(self, brand_personality):
        """Test brand alignment checking"""
        aligned_response = "We offer free consultations for personal injury cases in South Carolina and Georgia."
        assert brand_personality.is_brand_aligned(aligned_response) is True
        
        non_aligned_response = "We handle all types of legal cases."
        assert brand_personality.is_brand_aligned(non_aligned_response) is False

class TestLeadQualifier:
    """Test cases for lead qualification module"""
    
    @pytest.fixture
    def lead_qualifier(self):
        """Create lead qualifier instance for testing"""
        return TedSinkLawLeadQualifier()
    
    def test_qualify_lead_qualified(self, lead_qualifier):
        """Test qualifying a valid lead"""
        lead_info = LeadInfo(
            location="Charleston, South Carolina",
            case_type="car accident",
            injuries="broken leg and back pain",
            medical_treatment="hospital treatment and ongoing physical therapy"
        )
        
        result = lead_qualifier.qualify_lead(lead_info)
        
        assert result.status == QualificationStatus.QUALIFIED
        assert result.priority in [CasePriority.HIGH, CasePriority.MEDIUM]
        assert result.practice_area is not None
        assert len(result.next_steps) > 0
    
    def test_qualify_lead_not_qualified_geographic(self, lead_qualifier):
        """Test disqualifying lead due to geographic location"""
        lead_info = LeadInfo(
            location="Miami, Florida",
            case_type="car accident",
            injuries="minor injuries"
        )
        
        result = lead_qualifier.qualify_lead(lead_info)
        
        assert result.status == QualificationStatus.NOT_QUALIFIED
        assert "geographic" in result.disqualification_reason.lower()
        assert result.referral_suggestions is not None
    
    def test_qualify_lead_not_qualified_case_type(self, lead_qualifier):
        """Test disqualifying lead due to case type"""
        lead_info = LeadInfo(
            location="Atlanta, Georgia",
            case_type="divorce",
            injuries="emotional distress"
        )
        
        result = lead_qualifier.qualify_lead(lead_info)
        
        assert result.status == QualificationStatus.NOT_QUALIFIED
        assert "case type" in result.disqualification_reason.lower()
    
    def test_qualify_lead_emergency(self, lead_qualifier):
        """Test emergency lead qualification"""
        lead_info = LeadInfo(
            location="Columbia, South Carolina",
            case_type="truck accident",
            injuries="severe head injury",
            urgency_level="emergency"
        )
        
        result = lead_qualifier.qualify_lead(lead_info)
        
        assert result.status == QualificationStatus.EMERGENCY
        assert result.priority == CasePriority.EMERGENCY
    
    def test_find_practice_area_by_keyword(self, lead_qualifier):
        """Test practice area identification"""
        practice_area = lead_qualifier.practice_areas.find_practice_area_by_keyword("car accident")
        assert practice_area is not None
        assert practice_area.name == "Car Accidents"
        
        practice_area = lead_qualifier.practice_areas.find_practice_area_by_keyword("divorce")
        assert practice_area is not None
        assert practice_area.is_handled is False

class TestAppointmentScheduler:
    """Test cases for appointment scheduling module"""
    
    @pytest.fixture
    def scheduler(self):
        """Create appointment scheduler instance for testing"""
        return AppointmentScheduler()
    
    @pytest.mark.asyncio
    async def test_schedule_appointment(self, scheduler):
        """Test appointment scheduling"""
        # Create mock qualification result
        qualification_result = Mock()
        qualification_result.status.value = "qualified"
        qualification_result.priority.value = "medium"
        qualification_result.practice_area.name = "Car Accidents"
        
        appointment_preferences = {
            "format": "phone",
            "name": "Jane Smith",
            "phone": "555-987-6543"
        }
        
        result = await scheduler.schedule_appointment("test_session", appointment_preferences, qualification_result)
        
        assert result is not None
        assert "confirmation_id" in result
        assert result["format"] == "phone"
        assert result["consultation_fee"] == "Free"
    
    def test_get_consultation_formats(self, scheduler):
        """Test consultation format retrieval"""
        formats = scheduler.get_consultation_formats()
        assert len(formats) > 0
        
        # Check for expected formats
        format_names = [f["format"] for f in formats]
        assert "Phone Consultation" in format_names
        assert "In-Person Office Meeting" in format_names
        assert "Virtual Appointment" in format_names
    
    def test_get_office_locations(self, scheduler):
        """Test office location retrieval"""
        locations = scheduler.get_office_locations()
        assert len(locations) > 0
        
        # Check for primary office
        primary_offices = [loc for loc in locations if loc["is_primary"]]
        assert len(primary_offices) > 0

class TestEmergencyHandler:
    """Test cases for emergency handling module"""
    
    @pytest.fixture
    def emergency_handler(self):
        """Create emergency handler instance for testing"""
        return EmergencyHandler()
    
    @pytest.mark.asyncio
    async def test_handle_emergency(self, emergency_handler):
        """Test emergency handling"""
        client_message = "I'm in the hospital with serious injuries from a car accident. This is urgent!"
        
        response = await emergency_handler.handle_emergency("test_session", client_message)
        
        assert response is not None
        assert "urgent" in response.lower() or "immediate" in response.lower()
        assert "attorney" in response.lower()
        
        # Check that emergency is registered
        active_emergencies = emergency_handler.get_active_emergencies()
        assert "test_session" in active_emergencies
    
    def test_assess_emergency_level(self, emergency_handler):
        """Test emergency level assessment"""
        # Critical emergency
        critical_message = "I'm in critical condition with life-threatening injuries"
        level = emergency_handler._assess_emergency_level(critical_message)
        assert level.value == "critical"
        
        # Urgent emergency
        urgent_message = "I have serious injuries and need immediate help"
        level = emergency_handler._assess_emergency_level(urgent_message)
        assert level.value == "urgent"
        
        # High priority
        high_priority_message = "I have significant medical bills from an accident"
        level = emergency_handler._assess_emergency_level(high_priority_message)
        assert level.value == "high_priority"

class TestFirmInfo:
    """Test cases for firm information module"""
    
    @pytest.fixture
    def firm_info(self):
        """Create firm info instance for testing"""
        return TedSinkLawInfo()
    
    def test_get_primary_office(self, firm_info):
        """Test primary office retrieval"""
        primary_office = firm_info.get_primary_office()
        assert primary_office is not None
        assert primary_office.is_primary is True
        assert primary_office.city == "North Charleston"
    
    def test_is_service_area(self, firm_info):
        """Test service area validation"""
        assert firm_info.is_service_area("South Carolina") is True
        assert firm_info.is_service_area("Georgia") is True
        assert firm_info.is_service_area("Florida") is False
        assert firm_info.is_service_area("North Carolina") is False
    
    def test_get_office_by_city(self, firm_info):
        """Test office lookup by city"""
        office = firm_info.get_office_by_city("Atlanta")
        assert office is not None
        assert office.city == "Atlanta"
        assert office.state == "GA"
        
        office = firm_info.get_office_by_city("New York")
        assert office is None

class TestPracticeAreas:
    """Test cases for practice areas module"""
    
    @pytest.fixture
    def practice_areas(self):
        """Create practice areas instance for testing"""
        return TedSinkLawPracticeAreas()
    
    def test_is_personal_injury_case(self, practice_areas):
        """Test personal injury case identification"""
        assert practice_areas.is_personal_injury_case("car accident") is True
        assert practice_areas.is_personal_injury_case("slip and fall") is True
        assert practice_areas.is_personal_injury_case("divorce") is False
        assert practice_areas.is_personal_injury_case("criminal case") is False
    
    def test_is_non_personal_injury_case(self, practice_areas):
        """Test non-personal injury case identification"""
        assert practice_areas.is_non_personal_injury_case("divorce") is True
        assert practice_areas.is_non_personal_injury_case("criminal defense") is True
        assert practice_areas.is_non_personal_injury_case("car accident") is False
    
    def test_get_high_priority_cases(self, practice_areas):
        """Test high priority case retrieval"""
        high_priority_cases = practice_areas.get_high_priority_cases()
        assert len(high_priority_cases) > 0
        
        case_names = [case.name for case in high_priority_cases]
        assert "Car Accidents" in case_names
        assert "Truck Accidents" in case_names
        assert "Wrongful Death" in case_names

class TestClientStandards:
    """Test cases for client standards module"""
    
    @pytest.fixture
    def client_standards(self):
        """Create client standards instance for testing"""
        return TedSinkLawClientStandards()
    
    def test_get_service_guarantee(self, client_standards):
        """Test service guarantee retrieval"""
        guarantee = client_standards.get_service_guarantee("Free Consultation Guarantee")
        assert guarantee is not None
        assert guarantee.name == "Free Consultation Guarantee"
        assert "free" in guarantee.description.lower()
    
    def test_get_consultation_format(self, client_standards):
        """Test consultation format retrieval"""
        format_info = client_standards.get_consultation_format("Phone Consultation")
        assert format_info is not None
        assert format_info["format"] == "Phone Consultation"
        assert "30-60 minutes" in format_info["duration"]
    
    def test_get_emergency_protocol(self, client_standards):
        """Test emergency protocol retrieval"""
        protocol = client_standards.get_emergency_protocol()
        assert protocol is not None
        assert "immediate_response" in protocol
        assert "consultation_options" in protocol

if __name__ == "__main__":
    pytest.main([__file__])
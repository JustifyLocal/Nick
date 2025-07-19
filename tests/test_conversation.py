"""
Tests for Ted Sink Law Voice Receptionist AI conversation functionality
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from ai_engine.conversation_manager import (
    ConversationManager, 
    ConversationState, 
    CaseType, 
    LeadData
)
from ai_engine.ai_handler import AIHandler
from config.settings import settings


class TestConversationManager:
    """Test cases for ConversationManager"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.conversation_manager = ConversationManager()
    
    def test_initialization(self):
        """Test conversation manager initialization"""
        assert self.conversation_manager.current_state == ConversationState.GREETING
        assert self.conversation_manager.turn_count == 0
        assert isinstance(self.conversation_manager.lead_data, LeadData)
        assert len(self.conversation_manager.conversation_history) == 0
    
    def test_brand_prompt_generation(self):
        """Test brand prompt generation"""
        prompt = self.conversation_manager.get_brand_prompt()
        
        # Check that key brand elements are present
        assert settings.firm_name in prompt
        assert str(settings.firm_founded) in prompt
        assert settings.founder in prompt
        assert "next-generation law firm" in prompt
        assert "no fee unless we win" in prompt
    
    def test_case_type_analysis_personal_injury(self):
        """Test case type analysis for personal injury cases"""
        test_cases = [
            "I was in a car accident",
            "I got hurt at work",
            "I slipped and fell at the store",
            "My mother died in a nursing home accident"
        ]
        
        for test_case in test_cases:
            case_type, info = self.conversation_manager.analyze_case_type(test_case)
            assert case_type == CaseType.PERSONAL_INJURY
            assert "Personal injury case detected" in info
    
    def test_case_type_analysis_disqualified(self):
        """Test case type analysis for disqualified cases"""
        test_cases = [
            "I need help with a divorce",
            "I want to start a business",
            "I need help with a criminal case",
            "I want to buy a house"
        ]
        
        for test_case in test_cases:
            case_type, info = self.conversation_manager.analyze_case_type(test_case)
            assert case_type == CaseType.DISQUALIFIED
            assert "Case involves" in info
    
    def test_jurisdiction_check_valid(self):
        """Test jurisdiction check for valid locations"""
        valid_locations = [
            "I was in Charleston, South Carolina",
            "The accident happened in Atlanta, Georgia",
            "I live in Columbia",
            "It occurred in Greenville"
        ]
        
        for location in valid_locations:
            assert self.conversation_manager.check_jurisdiction(location) == True
    
    def test_jurisdiction_check_invalid(self):
        """Test jurisdiction check for invalid locations"""
        invalid_locations = [
            "I was in New York",
            "The accident happened in California",
            "I live in Texas",
            "It occurred in Florida"
        ]
        
        for location in invalid_locations:
            assert self.conversation_manager.check_jurisdiction(location) == False
    
    def test_emergency_detection(self):
        """Test emergency situation detection"""
        emergency_phrases = [
            "This is an emergency",
            "I need urgent help",
            "I'm in the hospital",
            "This is life-threatening"
        ]
        
        for phrase in emergency_phrases:
            assert self.conversation_manager.detect_emergency(phrase) == True
        
        non_emergency_phrases = [
            "I had a minor accident",
            "I want to schedule a consultation",
            "I have some questions"
        ]
        
        for phrase in non_emergency_phrases:
            assert self.conversation_manager.detect_emergency(phrase) == False
    
    def test_lead_data_update(self):
        """Test lead data updating"""
        self.conversation_manager.update_lead_data("", "name", "John Doe")
        self.conversation_manager.update_lead_data("", "phone", "(555) 123-4567")
        
        assert self.conversation_manager.lead_data.name == "John Doe"
        assert self.conversation_manager.lead_data.phone == "(555) 123-4567"
    
    def test_conversation_summary(self):
        """Test conversation summary generation"""
        # Add some test data
        self.conversation_manager.lead_data.name = "John Doe"
        self.conversation_manager.lead_data.phone = "(555) 123-4567"
        self.conversation_manager.turn_count = 5
        self.conversation_manager.current_state = ConversationState.INTAKE_COLLECTION
        
        summary = self.conversation_manager.get_conversation_summary()
        
        assert "conversation_id" in summary
        assert summary["turns"] == 5
        assert summary["final_state"] == "intake_collection"
        assert summary["lead_data"]["name"] == "John Doe"
        assert summary["lead_data"]["phone"] == "(555) 123-4567"
    
    def test_conversation_reset(self):
        """Test conversation reset"""
        # Add some data
        self.conversation_manager.lead_data.name = "John Doe"
        self.conversation_manager.turn_count = 5
        self.conversation_manager.current_state = ConversationState.INTAKE_COLLECTION
        
        # Reset
        self.conversation_manager.reset_conversation()
        
        assert self.conversation_manager.current_state == ConversationState.GREETING
        assert self.conversation_manager.turn_count == 0
        assert self.conversation_manager.lead_data.name is None
        assert len(self.conversation_manager.conversation_history) == 0


class TestAIHandler:
    """Test cases for AIHandler"""
    
    def setup_method(self):
        """Set up test fixtures"""
        with patch('ai_engine.ai_handler.OpenAI'):
            self.ai_handler = AIHandler()
    
    @patch('ai_engine.ai_handler.OpenAI')
    def test_initialization(self, mock_openai):
        """Test AI handler initialization"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        handler = AIHandler()
        assert handler.client == mock_client
        assert isinstance(handler.conversation_manager, ConversationManager)
    
    @patch('ai_engine.ai_handler.OpenAI')
    def test_generate_response_success(self, mock_openai):
        """Test successful response generation"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Thank you for calling Ted Law. How can I help you today?"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        handler = AIHandler()
        handler.client = mock_client
        
        response_data = handler.generate_response("Hello, I need help with a car accident")
        
        assert "response" in response_data
        assert "conversation_state" in response_data
        assert "extracted_data" in response_data
        assert "next_actions" in response_data
        assert "confidence_score" in response_data
    
    @patch('ai_engine.ai_handler.OpenAI')
    def test_generate_response_failure(self, mock_openai):
        """Test response generation failure"""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        handler = AIHandler()
        handler.client = mock_client
        
        response_data = handler.generate_response("Hello")
        
        assert response_data["conversation_state"] == "fallback"
        assert "I apologize for the technical difficulty" in response_data["response"]
        assert response_data["confidence_score"] == 0.3
    
    def test_extract_contact_info(self):
        """Test contact information extraction"""
        test_text = "My name is John Doe and my phone is (555) 123-4567"
        
        contact_info = self.ai_handler._extract_contact_info(test_text)
        
        assert contact_info["name"] == "John Doe"
        assert contact_info["phone"] == "(555) 123-4567"
    
    def test_extract_incident_info(self):
        """Test incident information extraction"""
        test_text = "The accident happened on 12/15/2023 in Charleston"
        
        incident_info = self.ai_handler._extract_incident_info(test_text)
        
        assert incident_info["incident_date"] == "12/15/2023"
        assert incident_info["incident_location"] == "Charleston"
    
    def test_extract_office_preference(self):
        """Test office preference extraction"""
        test_cases = [
            ("I prefer the Charleston office", "north_charleston"),
            ("Can I meet at the Atlanta location?", "atlanta"),
            ("I'd like to go to Greenville", "greenville")
        ]
        
        for text, expected in test_cases:
            result = self.ai_handler._extract_office_preference(text)
            assert result == expected
    
    def test_assess_urgency_level(self):
        """Test urgency level assessment"""
        high_urgency = "This is an emergency, I'm in the hospital"
        medium_urgency = "I was hurt in an accident and need medical treatment"
        low_urgency = "I want to schedule a consultation"
        
        assert self.ai_handler._assess_urgency_level(high_urgency) == "high"
        assert self.ai_handler._assess_urgency_level(medium_urgency) == "medium"
        assert self.ai_handler._assess_urgency_level(low_urgency) == "low"
    
    def test_has_sufficient_intake_data(self):
        """Test intake data sufficiency check"""
        # Initially insufficient
        assert self.ai_handler._has_sufficient_intake_data() == False
        
        # Add required fields
        self.ai_handler.conversation_manager.lead_data.name = "John Doe"
        self.ai_handler.conversation_manager.lead_data.phone = "(555) 123-4567"
        self.ai_handler.conversation_manager.lead_data.incident_date = "12/15/2023"
        self.ai_handler.conversation_manager.lead_data.case_type = "Car Accident"
        
        assert self.ai_handler._has_sufficient_intake_data() == True
    
    def test_calculate_confidence_score(self):
        """Test confidence score calculation"""
        user_input = "I was in a car accident"
        ai_response = "Thank you for calling Ted Law, the next-generation personal injury law firm. We offer completely free consultations with no obligation."
        
        score = self.ai_handler._calculate_confidence_score(user_input, ai_response)
        
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be high due to brand keywords and comprehensive response


class TestIntegration:
    """Integration tests for the complete system"""
    
    @patch('ai_engine.ai_handler.OpenAI')
    def test_complete_conversation_flow(self, mock_openai):
        """Test a complete conversation flow"""
        # Mock OpenAI responses for different conversation stages
        mock_responses = [
            "Thank you for calling Ted Law, the next-generation personal injury law firm. How can I help you today?",
            "I understand you were in a car accident. Could you tell me when this happened and where?",
            "Thank you for that information. I can schedule you for a free consultation today. What's your name and phone number?",
            "Perfect! I have you scheduled for a consultation. You'll hear from an attorney or case manager the same day."
        ]
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = mock_responses[0]
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        handler = AIHandler()
        handler.client = mock_client
        
        # Simulate conversation flow
        conversation_steps = [
            "Hello, I need help with a car accident",
            "It happened last week in Charleston",
            "My name is John Doe and my phone is (555) 123-4567",
            "Yes, that sounds good"
        ]
        
        for step in conversation_steps:
            response = handler.generate_response(step)
            assert response["response"] is not None
            assert response["confidence_score"] > 0.0
        
        # Check final conversation summary
        summary = handler.get_conversation_summary()
        assert summary["turns"] == len(conversation_steps)
        assert summary["qualification_status"] == "qualified"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
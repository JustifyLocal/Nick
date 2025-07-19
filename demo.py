#!/usr/bin/env python3
"""
Demo script for Ted Sink Law Voice Receptionist AI
Showcases the system with sample conversations
"""
import json
import time
from typing import Dict, List

# Mock AI responses for demo purposes
DEMO_RESPONSES = {
    "greeting": [
        "Thank you for calling Ted Law, the next-generation personal injury law firm. This is Sarah, your AI legal assistant. How can I help you today?",
        "Welcome to Ted Law, where we combine 21st century technology with personal attention. I'm here to help with your personal injury case. What happened?"
    ],
    "case_screening": [
        "I understand you were in a car accident. That's exactly the type of case we handle. Could you tell me when this happened and where?",
        "A car accident - we have extensive experience with these cases. We offer completely free consultations with no obligation. When did this occur?"
    ],
    "jurisdiction_check": [
        "Charleston, South Carolina - perfect! That's within our service area. We have an office right there at 1075-A E Montague Ave.",
        "Great! South Carolina is one of our primary service states. We can definitely help you with your case."
    ],
    "intake_collection": [
        "Thank you for that information. I can schedule you for a free consultation today. What's your name and phone number?",
        "Perfect! I have the details about your accident. Now I need your contact information to schedule your free consultation."
    ],
    "consultation_booking": [
        "Excellent! I have you scheduled for a consultation today. You'll hear from an attorney or case manager the same day - that's our guarantee.",
        "Perfect! I've scheduled your free consultation. We guarantee same-day response from an attorney or case manager."
    ],
    "emergency_handling": [
        "This sounds urgent! I can schedule you for an immediate consultation. We also offer home or hospital visits if you can't travel.",
        "I understand this is an emergency situation. Let me get you scheduled immediately. We're available 24/7 for urgent cases."
    ],
    "disqualification": [
        "I appreciate you considering Ted Law. Unfortunately, we specialize exclusively in personal injury cases in South Carolina and Georgia.",
        "Thank you for calling Ted Law. We focus specifically on personal injury cases in our service area. I'd be happy to provide referrals."
    ]
}

SAMPLE_CONVERSATIONS = [
    {
        "title": "Car Accident Case - Qualified Lead",
        "conversation": [
            ("Hello, I need help with a car accident", "greeting"),
            ("It happened last week in Charleston", "case_screening"),
            ("My name is John Doe and my phone is (555) 123-4567", "intake_collection"),
            ("Yes, that sounds good", "consultation_booking")
        ]
    },
    {
        "title": "Emergency Medical Malpractice",
        "conversation": [
            ("This is an emergency! My mother is in the hospital", "emergency_handling"),
            ("It's medical malpractice in Atlanta", "case_screening"),
            ("Her name is Mary Smith, phone (555) 987-6543", "intake_collection"),
            ("Yes, please help us immediately", "consultation_booking")
        ]
    },
    {
        "title": "Disqualified Case - Divorce",
        "conversation": [
            ("I need help with a divorce", "greeting"),
            ("It's a family law case", "disqualification")
        ]
    },
    {
        "title": "Out of Jurisdiction Case",
        "conversation": [
            ("I was in an accident in New York", "greeting"),
            ("The accident happened in Manhattan", "disqualification")
        ]
    }
]


def print_brand_header():
    """Print Ted Sink Law brand header"""
    print("=" * 80)
    print("🎯 TED SINK LAW VOICE RECEPTIONIST AI DEMO")
    print("=" * 80)
    print("🏢 Ted Law: Accident & Injury Law Firm, LLC")
    print("📍 Serving South Carolina & Georgia")
    print("🚀 Next-Generation Personal Injury Law Firm")
    print("💬 AI-Powered Client Intake & Lead Qualification")
    print("=" * 80)
    print()


def print_conversation_turn(user_input: str, ai_response: str, state: str, turn: int):
    """Print a conversation turn with formatting"""
    print(f"🔄 Turn {turn} - State: {state.upper()}")
    print(f"👤 Caller: {user_input}")
    print(f"🤖 AI: {ai_response}")
    print(f"📊 Extracted Data: {get_extracted_data(user_input, state)}")
    print("-" * 80)


def get_extracted_data(user_input: str, state: str) -> Dict:
    """Mock data extraction for demo"""
    extracted = {}
    
    if "name" in user_input.lower() and "phone" in user_input.lower():
        extracted["name"] = "John Doe" if "john" in user_input.lower() else "Mary Smith"
        extracted["phone"] = "(555) 123-4567" if "123" in user_input else "(555) 987-6543"
    
    if "charleston" in user_input.lower():
        extracted["incident_location"] = "Charleston, SC"
    elif "atlanta" in user_input.lower():
        extracted["incident_location"] = "Atlanta, GA"
    
    if "car accident" in user_input.lower():
        extracted["case_type"] = "Car Accident"
    elif "medical malpractice" in user_input.lower():
        extracted["case_type"] = "Medical Malpractice"
    
    if "emergency" in user_input.lower() or "hospital" in user_input.lower():
        extracted["urgency_level"] = "high"
    
    return extracted


def run_conversation_demo(conversation_data: Dict):
    """Run a complete conversation demo"""
    print(f"📞 {conversation_data['title']}")
    print("=" * 80)
    
    for i, (user_input, state) in enumerate(conversation_data['conversation'], 1):
        # Get AI response
        responses = DEMO_RESPONSES.get(state, ["I understand. How can I help you further?"])
        ai_response = responses[0] if i == 1 else responses[-1]  # Use first for greeting, last for others
        
        # Print conversation turn
        print_conversation_turn(user_input, ai_response, state, i)
        
        # Simulate processing time
        time.sleep(1)
    
    # Print conversation summary
    print("📋 CONVERSATION SUMMARY")
    print("=" * 80)
    print(f"✅ Status: {'Qualified' if 'disqualification' not in [s for _, s in conversation_data['conversation']] else 'Disqualified'}")
    print(f"📊 Total Turns: {len(conversation_data['conversation'])}")
    print(f"🎯 Final State: {conversation_data['conversation'][-1][1]}")
    print("=" * 80)
    print()


def showcase_features():
    """Showcase key features of the system"""
    print("🚀 SYSTEM FEATURES SHOWCASE")
    print("=" * 80)
    
    features = [
        ("🎯 Lead Qualification", "Automatically screens for personal injury cases in SC/GA"),
        ("🗣️ Brand Voice", "Maintains Ted Sink Law's confident, empathetic tone"),
        ("⚡ Emergency Detection", "Identifies urgent cases for immediate attention"),
        ("📊 Data Extraction", "Automatically extracts contact and case information"),
        ("🏢 Office Integration", "Suggests appropriate office locations"),
        ("📅 Consultation Booking", "Schedules free consultations with same-day guarantee"),
        ("🚫 Disqualification", "Professionally handles non-qualifying cases"),
        ("🔒 Jurisdiction Check", "Verifies geographic coverage automatically")
    ]
    
    for feature, description in features:
        print(f"{feature}: {description}")
    
    print("=" * 80)
    print()


def showcase_brand_elements():
    """Showcase Ted Sink Law brand elements"""
    print("🏢 BRAND ELEMENTS INTEGRATION")
    print("=" * 80)
    
    brand_elements = [
        "Next-generation law firm with 21st century technology",
        "We won't back down from a fight",
        "No fee unless we win",
        "David vs. Goliath positioning",
        "Personal attention with rapid response",
        "Same-day attorney or case manager response",
        "30-day satisfaction guarantee",
        "Free consultations with no obligation"
    ]
    
    for element in brand_elements:
        print(f"✅ {element}")
    
    print("=" * 80)
    print()


def main():
    """Main demo function"""
    print_brand_header()
    
    # Showcase features
    showcase_features()
    
    # Showcase brand elements
    showcase_brand_elements()
    
    # Run conversation demos
    print("💬 CONVERSATION DEMOS")
    print("=" * 80)
    
    for conversation in SAMPLE_CONVERSATIONS:
        run_conversation_demo(conversation)
        time.sleep(2)  # Pause between conversations
    
    # Final summary
    print("🎉 DEMO COMPLETE")
    print("=" * 80)
    print("The Ted Sink Law Voice Receptionist AI is ready for deployment!")
    print("Key capabilities demonstrated:")
    print("• Intelligent lead qualification")
    print("• Brand-authentic conversations")
    print("• Emergency situation handling")
    print("• Professional disqualification")
    print("• Automated data extraction")
    print("• Consultation scheduling")
    print("=" * 80)


if __name__ == "__main__":
    main()
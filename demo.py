#!/usr/bin/env python3
"""
Ted Sink Law Voice Receptionist AI Demo

This demo shows how to use the voice receptionist AI system
to handle client interactions, qualify leads, and schedule appointments.
"""

import asyncio
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.voice_receptionist import TedSinkLawVoiceReceptionist

async def demo_qualified_client():
    """Demo with a qualified client"""
    print("\n" + "="*60)
    print("DEMO: QUALIFIED CLIENT - CAR ACCIDENT IN SOUTH CAROLINA")
    print("="*60)
    
    receptionist = TedSinkLawVoiceReceptionist()
    session_id = "demo_qualified_001"
    
    # Start call
    print("\n🤖 AI: ", end="")
    greeting = await receptionist.handle_call(session_id)
    print(greeting)
    
    # Client response
    print("\n👤 Client: I was in a car accident in Charleston, South Carolina last week. I have serious injuries including a broken leg and back pain. I need help with my case.")
    
    # AI response
    print("\n🤖 AI: ", end="")
    response = await receptionist.process_client_response(session_id, "I was in a car accident in Charleston, South Carolina last week. I have serious injuries including a broken leg and back pain. I need help with my case.")
    print(response)
    
    # Client response
    print("\n👤 Client: Yes, I'd like to schedule a consultation. Can we do it over the phone?")
    
    # Schedule appointment
    appointment_preferences = {
        "format": "phone",
        "name": "John Smith",
        "phone": "555-123-4567"
    }
    
    print("\n🤖 AI: ", end="")
    confirmation = await receptionist.schedule_appointment(session_id, appointment_preferences)
    print(confirmation)
    
    # End call
    print("\n👤 Client: Thank you, that sounds great!")
    
    print("\n🤖 AI: ", end="")
    ending = await receptionist.end_call(session_id)
    print(ending)

async def demo_not_qualified_client():
    """Demo with a non-qualified client"""
    print("\n" + "="*60)
    print("DEMO: NON-QUALIFIED CLIENT - DIVORCE CASE IN FLORIDA")
    print("="*60)
    
    receptionist = TedSinkLawVoiceReceptionist()
    session_id = "demo_not_qualified_001"
    
    # Start call
    print("\n🤖 AI: ", end="")
    greeting = await receptionist.handle_call(session_id)
    print(greeting)
    
    # Client response
    print("\n👤 Client: I need help with a divorce case. I live in Miami, Florida and my husband and I are having issues with custody and property division.")
    
    # AI response
    print("\n🤖 AI: ", end="")
    response = await receptionist.process_client_response(session_id, "I need help with a divorce case. I live in Miami, Florida and my husband and I are having issues with custody and property division.")
    print(response)
    
    # End call
    print("\n👤 Client: I understand. Thank you for the referral information.")
    
    print("\n🤖 AI: ", end="")
    ending = await receptionist.end_call(session_id)
    print(ending)

async def demo_emergency_client():
    """Demo with an emergency client"""
    print("\n" + "="*60)
    print("DEMO: EMERGENCY CLIENT - HOSPITALIZED WITH SERIOUS INJURIES")
    print("="*60)
    
    receptionist = TedSinkLawVoiceReceptionist()
    session_id = "demo_emergency_001"
    
    # Start call
    print("\n🤖 AI: ", end="")
    greeting = await receptionist.handle_call(session_id)
    print(greeting)
    
    # Client response
    print("\n👤 Client: I'm in the hospital right now! I was in a serious truck accident in Atlanta and I have severe head injuries and broken bones. This is urgent and I need immediate help!")
    
    # AI response
    print("\n🤖 AI: ", end="")
    response = await receptionist.process_client_response(session_id, "I'm in the hospital right now! I was in a serious truck accident in Atlanta and I have severe head injuries and broken bones. This is urgent and I need immediate help!")
    print(response)
    
    # End call
    print("\n👤 Client: Thank you so much for the immediate help!")
    
    print("\n🤖 AI: ", end="")
    ending = await receptionist.end_call(session_id)
    print(ending)

async def demo_uncertain_client():
    """Demo with an uncertain client"""
    print("\n" + "="*60)
    print("DEMO: UNCERTAIN CLIENT - NEEDS MORE INFORMATION")
    print("="*60)
    
    receptionist = TedSinkLawVoiceReceptionist()
    session_id = "demo_uncertain_001"
    
    # Start call
    print("\n🤖 AI: ", end="")
    greeting = await receptionist.handle_call(session_id)
    print(greeting)
    
    # Client response
    print("\n👤 Client: I think I might need legal help, but I'm not sure. Something happened at work and I got hurt.")
    
    # AI response
    print("\n🤖 AI: ", end="")
    response = await receptionist.process_client_response(session_id, "I think I might need legal help, but I'm not sure. Something happened at work and I got hurt.")
    print(response)
    
    # Client response
    print("\n👤 Client: It was a construction accident in Columbia, South Carolina. I fell from scaffolding and broke my arm. I've been getting workers comp but it's not enough.")
    
    # AI response
    print("\n🤖 AI: ", end="")
    response = await receptionist.process_client_response(session_id, "It was a construction accident in Columbia, South Carolina. I fell from scaffolding and broke my arm. I've been getting workers comp but it's not enough.")
    print(response)
    
    # End call
    print("\n👤 Client: I'll think about it and call back. Thank you for the information.")
    
    print("\n🤖 AI: ", end="")
    ending = await receptionist.end_call(session_id)
    print(ending)

def show_system_info():
    """Display system information"""
    print("\n" + "="*60)
    print("TED SINK LAW VOICE RECEPTIONIST AI SYSTEM")
    print("="*60)
    print("🤖 AI Name: Alex")
    print("🏢 Firm: Ted Law: Accident & Injury Law Firm, LLC")
    print("📍 Service Areas: South Carolina and Georgia")
    print("⚖️ Practice Areas: Personal Injury Cases Only")
    print("💬 Features: Lead Qualification, Appointment Scheduling, Emergency Handling")
    print("🎯 Brand: Next-generation law firm with 21st century technology")
    print("="*60)

async def main():
    """Main demo function"""
    show_system_info()
    
    # Run all demos
    await demo_qualified_client()
    await demo_not_qualified_client()
    await demo_emergency_client()
    await demo_uncertain_client()
    
    print("\n" + "="*60)
    print("DEMO COMPLETED")
    print("="*60)
    print("This demo showcased the Ted Sink Law Voice Receptionist AI's ability to:")
    print("✅ Handle qualified personal injury clients")
    print("✅ Professionally redirect non-qualified clients")
    print("✅ Provide immediate emergency assistance")
    print("✅ Gather information from uncertain clients")
    print("✅ Maintain brand voice and personality throughout")
    print("✅ Schedule appointments and provide follow-up")
    print("="*60)

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
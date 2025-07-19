"""
Appointment Scheduler Module for Ted Sink Law

Handles scheduling of consultations for qualified clients with
multiple format options and office locations.
"""

import asyncio
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum

from ..data.firm_info import TedSinkLawInfo
from ..data.client_standards import TedSinkLawClientStandards
from ..qualification.lead_qualifier import QualificationResult

class ConsultationFormat(Enum):
    """Available consultation formats"""
    PHONE = "phone"
    IN_PERSON = "in_person"
    VIRTUAL = "virtual"
    HOME_VISIT = "home_visit"
    HOSPITAL_VISIT = "hospital_visit"

@dataclass
class AppointmentSlot:
    """Represents an available appointment slot"""
    date: datetime
    format: ConsultationFormat
    office_location: Optional[str]
    attorney: str
    duration: int  # minutes
    is_available: bool = True

@dataclass
class AppointmentRequest:
    """Client appointment request"""
    session_id: str
    preferred_format: ConsultationFormat
    preferred_date: Optional[datetime]
    preferred_time: Optional[str]
    preferred_location: Optional[str]
    urgency_level: str
    case_type: str
    client_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]

class AppointmentScheduler:
    """Handles appointment scheduling for Ted Sink Law"""
    
    def __init__(self):
        """Initialize the appointment scheduler"""
        self.firm_info = TedSinkLawInfo()
        self.client_standards = TedSinkLawClientStandards()
        
        # Available attorneys for consultations
        self.attorneys = [
            "Ted Sink",
            "Laura",
            "Angela Grunwald"
        ]
        
        # Business hours (simplified)
        self.business_hours = {
            "monday": {"start": "9:00", "end": "17:00"},
            "tuesday": {"start": "9:00", "end": "17:00"},
            "wednesday": {"start": "9:00", "end": "17:00"},
            "thursday": {"start": "9:00", "end": "17:00"},
            "friday": {"start": "9:00", "end": "17:00"},
            "saturday": {"start": "10:00", "end": "14:00"},
            "sunday": {"start": "closed", "end": "closed"}
        }
        
        # Emergency availability
        self.emergency_available = True
    
    async def schedule_appointment(self, session_id: str, 
                                 appointment_preferences: Dict[str, Any],
                                 qualification_result: QualificationResult) -> Dict[str, Any]:
        """
        Schedule an appointment for a qualified client
        
        Args:
            session_id: Call session identifier
            appointment_preferences: Client's appointment preferences
            qualification_result: Lead qualification result
            
        Returns:
            Appointment confirmation details
        """
        
        # Create appointment request
        request = self._create_appointment_request(session_id, appointment_preferences, qualification_result)
        
        # Find available slots
        available_slots = await self._find_available_slots(request)
        
        if not available_slots:
            return self._generate_no_availability_response(request)
        
        # Select best slot
        selected_slot = self._select_best_slot(available_slots, request)
        
        # Confirm appointment
        confirmation = await self._confirm_appointment(selected_slot, request)
        
        return confirmation
    
    def _create_appointment_request(self, session_id: str, 
                                  preferences: Dict[str, Any],
                                  qualification_result: QualificationResult) -> AppointmentRequest:
        """Create appointment request from preferences"""
        
        # Determine format
        format_str = preferences.get("format", "phone").lower()
        if format_str == "phone":
            format_enum = ConsultationFormat.PHONE
        elif format_str == "in_person":
            format_enum = ConsultationFormat.IN_PERSON
        elif format_str == "virtual":
            format_enum = ConsultationFormat.VIRTUAL
        elif format_str == "home":
            format_enum = ConsultationFormat.HOME_VISIT
        elif format_str == "hospital":
            format_enum = ConsultationFormat.HOSPITAL_VISIT
        else:
            format_enum = ConsultationFormat.PHONE
        
        # Parse date if provided
        preferred_date = None
        if preferences.get("date"):
            try:
                preferred_date = datetime.strptime(preferences["date"], "%Y-%m-%d")
            except:
                preferred_date = None
        
        return AppointmentRequest(
            session_id=session_id,
            preferred_format=format_enum,
            preferred_date=preferred_date,
            preferred_time=preferences.get("time"),
            preferred_location=preferences.get("location"),
            urgency_level=qualification_result.priority.value,
            case_type=qualification_result.practice_area.name if qualification_result.practice_area else "personal injury",
            client_name=preferences.get("name"),
            contact_phone=preferences.get("phone"),
            contact_email=preferences.get("email")
        )
    
    async def _find_available_slots(self, request: AppointmentRequest) -> List[AppointmentSlot]:
        """Find available appointment slots"""
        slots = []
        
        # Determine start date
        start_date = request.preferred_date or datetime.now()
        if start_date < datetime.now():
            start_date = datetime.now()
        
        # Generate slots for next 7 days
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            
            # Skip weekends for non-emergency cases
            if current_date.weekday() >= 5 and request.urgency_level != "emergency":
                continue
            
            # Generate slots for this date
            day_slots = self._generate_day_slots(current_date, request)
            slots.extend(day_slots)
        
        return slots
    
    def _generate_day_slots(self, date: datetime, request: AppointmentRequest) -> List[AppointmentSlot]:
        """Generate available slots for a specific day"""
        slots = []
        
        # Get business hours for this day
        day_name = date.strftime("%A").lower()
        if day_name not in self.business_hours:
            return slots
        
        hours = self.business_hours[day_name]
        if hours["start"] == "closed":
            return slots
        
        # Generate time slots
        start_hour = int(hours["start"].split(":")[0])
        end_hour = int(hours["end"].split(":")[0])
        
        for hour in range(start_hour, end_hour):
            for minute in [0, 30]:  # 30-minute intervals
                slot_time = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # Skip past times
                if slot_time < datetime.now():
                    continue
                
                # Determine duration based on format
                duration = self._get_consultation_duration(request.preferred_format)
                
                # Determine attorney
                attorney = self._select_attorney(request)
                
                # Determine office location
                office_location = self._select_office_location(request)
                
                slot = AppointmentSlot(
                    date=slot_time,
                    format=request.preferred_format,
                    office_location=office_location,
                    attorney=attorney,
                    duration=duration
                )
                
                slots.append(slot)
        
        return slots
    
    def _get_consultation_duration(self, format: ConsultationFormat) -> int:
        """Get consultation duration based on format"""
        duration_map = {
            ConsultationFormat.PHONE: 45,
            ConsultationFormat.IN_PERSON: 75,
            ConsultationFormat.VIRTUAL: 60,
            ConsultationFormat.HOME_VISIT: 90,
            ConsultationFormat.HOSPITAL_VISIT: 60
        }
        return duration_map.get(format, 60)
    
    def _select_attorney(self, request: AppointmentRequest) -> str:
        """Select appropriate attorney for consultation"""
        # For emergency cases, prioritize Ted Sink
        if request.urgency_level == "emergency":
            return "Ted Sink"
        
        # For high priority cases, use senior attorneys
        if request.urgency_level == "high":
            return "Ted Sink" if "Ted Sink" in self.attorneys else self.attorneys[0]
        
        # For standard cases, rotate among available attorneys
        return self.attorneys[0]  # Simplified - would implement rotation logic
    
    def _select_office_location(self, request: AppointmentRequest) -> Optional[str]:
        """Select appropriate office location"""
        if request.preferred_format in [ConsultationFormat.PHONE, ConsultationFormat.VIRTUAL]:
            return None
        
        if request.preferred_location:
            # Check if preferred location matches an office
            for office in self.firm_info.OFFICES:
                if office.city.lower() in request.preferred_location.lower():
                    return office.name
        
        # Default to primary office
        return self.firm_info.get_primary_office().name
    
    def _select_best_slot(self, available_slots: List[AppointmentSlot], 
                         request: AppointmentRequest) -> AppointmentSlot:
        """Select the best available slot"""
        
        # For emergency cases, prioritize earliest available
        if request.urgency_level == "emergency":
            return min(available_slots, key=lambda x: x.date)
        
        # For high priority cases, prioritize same day or next day
        if request.urgency_level == "high":
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            
            same_day_slots = [s for s in available_slots if s.date.date() == today]
            if same_day_slots:
                return min(same_day_slots, key=lambda x: x.date)
            
            next_day_slots = [s for s in available_slots if s.date.date() == tomorrow]
            if next_day_slots:
                return min(next_day_slots, key=lambda x: x.date)
        
        # For standard cases, prefer preferred format and time
        preferred_slots = [s for s in available_slots if s.format == request.preferred_format]
        if preferred_slots:
            return min(preferred_slots, key=lambda x: x.date)
        
        # Fallback to earliest available
        return min(available_slots, key=lambda x: x.date)
    
    async def _confirm_appointment(self, slot: AppointmentSlot, 
                                 request: AppointmentRequest) -> Dict[str, Any]:
        """Confirm the appointment and generate confirmation details"""
        
        # Generate confirmation ID
        confirmation_id = f"CONF_{request.session_id}_{slot.date.strftime('%Y%m%d_%H%M')}"
        
        # Format details for response
        confirmation = {
            "confirmation_id": confirmation_id,
            "session_id": request.session_id,
            "format": slot.format.value,
            "date": slot.date.strftime("%Y-%m-%d"),
            "time": slot.date.strftime("%I:%M %p"),
            "duration": f"{slot.duration} minutes",
            "attorney": slot.attorney,
            "office_location": slot.office_location,
            "case_type": request.case_type,
            "client_name": request.client_name,
            "contact_phone": request.contact_phone,
            "contact_email": request.contact_email,
            "urgency_level": request.urgency_level,
            "consultation_fee": "Free",
            "preparation_notes": self._generate_preparation_notes(slot, request)
        }
        
        # Log appointment
        await self._log_appointment(confirmation)
        
        return confirmation
    
    def _generate_preparation_notes(self, slot: AppointmentSlot, 
                                  request: AppointmentRequest) -> List[str]:
        """Generate preparation notes for the consultation"""
        notes = []
        
        if slot.format == ConsultationFormat.PHONE:
            notes.extend([
                "Ensure quiet environment for phone consultation",
                "Have case details and documents ready",
                "Be prepared to discuss timeline and damages"
            ])
        
        elif slot.format == ConsultationFormat.IN_PERSON:
            notes.extend([
                "Bring any relevant documents (police reports, medical records)",
                "Arrive 10 minutes early for paperwork",
                "Bring photo ID for verification"
            ])
        
        elif slot.format == ConsultationFormat.VIRTUAL:
            notes.extend([
                "Test video conferencing software beforehand",
                "Ensure stable internet connection",
                "Have documents ready to share via screen share"
            ])
        
        elif slot.format == ConsultationFormat.HOME_VISIT:
            notes.extend([
                "Ensure safe and accessible environment",
                "Have any relevant documents available",
                "Inform family members of appointment"
            ])
        
        elif slot.format == ConsultationFormat.HOSPITAL_VISIT:
            notes.extend([
                "Confirm hospital visitor policies",
                "Ensure patient is stable for consultation",
                "Have medical records and incident details ready"
            ])
        
        # Add general notes
        notes.extend([
            "Consultation is completely free with no obligation",
            "We'll discuss your case and legal options",
            "Bring list of questions you'd like answered"
        ])
        
        return notes
    
    async def _log_appointment(self, confirmation: Dict[str, Any]) -> None:
        """Log the appointment for record keeping"""
        # In production, this would save to database
        print(f"Appointment logged: {confirmation['confirmation_id']}")
    
    def _generate_no_availability_response(self, request: AppointmentRequest) -> Dict[str, Any]:
        """Generate response when no slots are available"""
        return {
            "error": "no_availability",
            "message": "I apologize, but we don't have any available slots in the next few days.",
            "suggestions": [
                "We can schedule a phone consultation for next week",
                "We can add you to our waitlist for cancellations",
                "We can arrange an emergency consultation if this is urgent"
            ],
            "alternative_formats": [
                "Phone consultation (available sooner)",
                "Virtual consultation (more flexible scheduling)",
                "Home visit (for injured clients)"
            ]
        }
    
    def get_consultation_formats(self) -> List[Dict[str, str]]:
        """Get available consultation formats"""
        return self.client_standards.CONSULTATION_FORMATS
    
    def get_office_locations(self) -> List[Dict[str, str]]:
        """Get available office locations"""
        locations = []
        for office in self.firm_info.OFFICES:
            locations.append({
                "name": office.name,
                "address": f"{office.address}, {office.city}, {office.state} {office.zip_code}",
                "phone": office.phone,
                "is_primary": office.is_primary
            })
        return locations
"""
Call Logger Utility for Ted Sink Law Voice Receptionist AI

Records and logs all call interactions for quality assurance,
analytics, and compliance purposes.
"""

import json
import logging
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
import os

@dataclass
class CallLog:
    """Call log entry"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    client_info: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    qualification_result: Optional[Dict[str, Any]]
    appointment_scheduled: bool
    emergency_handled: bool
    call_duration: Optional[int]  # seconds
    outcome: str
    quality_score: Optional[float]

class CallLogger:
    """Handles call logging and analytics for Ted Sink Law"""
    
    def __init__(self, log_directory: str = "logs"):
        """Initialize the call logger"""
        self.log_directory = log_directory
        self.log_file = os.path.join(log_directory, "call_logs.json")
        
        # Ensure log directory exists
        os.makedirs(log_directory, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        if not self.logger.handlers:
            file_handler = logging.FileHandler(os.path.join(log_directory, "call_logger.log"))
            file_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(file_handler)
        
        # Initialize call logs storage
        self.call_logs: Dict[str, CallLog] = {}
    
    def log_call_start(self, session_id: str) -> None:
        """Log the start of a call"""
        call_log = CallLog(
            session_id=session_id,
            start_time=datetime.now(),
            end_time=None,
            client_info={},
            conversation_history=[],
            qualification_result=None,
            appointment_scheduled=False,
            emergency_handled=False,
            call_duration=None,
            outcome="in_progress",
            quality_score=None
        )
        
        self.call_logs[session_id] = call_log
        
        # Log to file
        self.logger.info(f"Call started - Session ID: {session_id}")
        
        # Save to JSON file
        self._save_call_logs()
    
    def log_interaction(self, session_id: str, client_message: str, ai_response: str) -> None:
        """Log a conversation interaction"""
        if session_id not in self.call_logs:
            self.logger.warning(f"Attempted to log interaction for unknown session: {session_id}")
            return
        
        call_log = self.call_logs[session_id]
        
        # Add to conversation history
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "client_message": client_message,
            "ai_response": ai_response
        }
        
        call_log.conversation_history.append(interaction)
        
        # Log to file
        self.logger.info(f"Interaction logged - Session ID: {session_id}")
        
        # Save to JSON file
        self._save_call_logs()
    
    def log_call_end(self, session_id: str, session_data: Any) -> None:
        """Log the end of a call"""
        if session_id not in self.call_logs:
            self.logger.warning(f"Attempted to log call end for unknown session: {session_id}")
            return
        
        call_log = self.call_logs[session_id]
        call_log.end_time = datetime.now()
        
        # Calculate call duration
        if call_log.start_time and call_log.end_time:
            duration = (call_log.end_time - call_log.start_time).total_seconds()
            call_log.call_duration = int(duration)
        
        # Update call outcome
        if hasattr(session_data, 'emergency_handled') and session_data.emergency_handled:
            call_log.outcome = "emergency_handled"
        elif hasattr(session_data, 'appointment_scheduled') and session_data.appointment_scheduled:
            call_log.outcome = "appointment_scheduled"
        elif hasattr(session_data, 'qualification_result'):
            if session_data.qualification_result.status.value == "qualified":
                call_log.outcome = "qualified_no_appointment"
            elif session_data.qualification_result.status.value == "not_qualified":
                call_log.outcome = "not_qualified"
            else:
                call_log.outcome = "incomplete"
        else:
            call_log.outcome = "incomplete"
        
        # Update session data
        if hasattr(session_data, 'client_info'):
            call_log.client_info = session_data.client_info
        if hasattr(session_data, 'qualification_result') and session_data.qualification_result:
            call_log.qualification_result = self._qualification_result_to_dict(session_data.qualification_result)
        if hasattr(session_data, 'appointment_scheduled'):
            call_log.appointment_scheduled = session_data.appointment_scheduled
        if hasattr(session_data, 'emergency_handled'):
            call_log.emergency_handled = session_data.emergency_handled
        
        # Calculate quality score
        call_log.quality_score = self._calculate_quality_score(call_log)
        
        # Log to file
        self.logger.info(f"Call ended - Session ID: {session_id}, Outcome: {call_log.outcome}, Duration: {call_log.call_duration}s")
        
        # Save to JSON file
        self._save_call_logs()
        
        # Generate analytics
        self._generate_call_analytics(call_log)
    
    def _qualification_result_to_dict(self, qualification_result: Any) -> Dict[str, Any]:
        """Convert qualification result to dictionary for JSON serialization"""
        if not qualification_result:
            return {}
        
        return {
            "status": qualification_result.status.value if hasattr(qualification_result.status, 'value') else str(qualification_result.status),
            "priority": qualification_result.priority.value if hasattr(qualification_result.priority, 'value') else str(qualification_result.priority),
            "practice_area": qualification_result.practice_area.name if qualification_result.practice_area else None,
            "reasoning": qualification_result.reasoning,
            "next_steps": qualification_result.next_steps,
            "disqualification_reason": qualification_result.disqualification_reason,
            "referral_suggestions": qualification_result.referral_suggestions
        }
    
    def _calculate_quality_score(self, call_log: CallLog) -> float:
        """Calculate quality score for the call"""
        score = 0.0
        
        # Base score for completed call
        if call_log.outcome != "incomplete":
            score += 20.0
        
        # Points for appointment scheduling
        if call_log.appointment_scheduled:
            score += 30.0
        
        # Points for emergency handling
        if call_log.emergency_handled:
            score += 25.0
        
        # Points for qualification
        if call_log.qualification_result and call_log.qualification_result.get("status") == "qualified":
            score += 15.0
        
        # Points for conversation length (optimal range)
        if call_log.conversation_history:
            interaction_count = len(call_log.conversation_history)
            if 3 <= interaction_count <= 10:  # Optimal conversation length
                score += 10.0
            elif interaction_count > 10:  # Too long
                score += 5.0
        
        # Points for call duration (optimal range)
        if call_log.call_duration:
            if 60 <= call_log.call_duration <= 300:  # 1-5 minutes optimal
                score += 10.0
            elif call_log.call_duration < 60:  # Too short
                score += 5.0
            elif call_log.call_duration > 300:  # Too long
                score += 5.0
        
        return min(score, 100.0)  # Cap at 100
    
    def _generate_call_analytics(self, call_log: CallLog) -> None:
        """Generate analytics for the call"""
        analytics = {
            "session_id": call_log.session_id,
            "call_date": call_log.start_time.strftime("%Y-%m-%d"),
            "call_time": call_log.start_time.strftime("%H:%M:%S"),
            "duration_seconds": call_log.call_duration,
            "outcome": call_log.outcome,
            "quality_score": call_log.quality_score,
            "appointment_scheduled": call_log.appointment_scheduled,
            "emergency_handled": call_log.emergency_handled,
            "interaction_count": len(call_log.conversation_history),
            "case_type": call_log.qualification_result.get("practice_area") if call_log.qualification_result else None,
            "qualification_status": call_log.qualification_result.get("status") if call_log.qualification_result else None
        }
        
        # Save analytics to separate file
        analytics_file = os.path.join(self.log_directory, "call_analytics.json")
        try:
            with open(analytics_file, 'a') as f:
                f.write(json.dumps(analytics) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to save analytics: {e}")
    
    def _save_call_logs(self) -> None:
        """Save call logs to JSON file"""
        try:
            # Convert call logs to serializable format
            serializable_logs = {}
            for session_id, call_log in self.call_logs.items():
                serializable_logs[session_id] = asdict(call_log)
                # Convert datetime objects to strings
                if serializable_logs[session_id]["start_time"]:
                    serializable_logs[session_id]["start_time"] = serializable_logs[session_id]["start_time"].isoformat()
                if serializable_logs[session_id]["end_time"]:
                    serializable_logs[session_id]["end_time"] = serializable_logs[session_id]["end_time"].isoformat()
            
            with open(self.log_file, 'w') as f:
                json.dump(serializable_logs, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save call logs: {e}")
    
    def get_call_log(self, session_id: str) -> Optional[CallLog]:
        """Get call log for a specific session"""
        return self.call_logs.get(session_id)
    
    def get_all_call_logs(self) -> Dict[str, CallLog]:
        """Get all call logs"""
        return self.call_logs.copy()
    
    def get_call_logs_by_date(self, date: str) -> List[CallLog]:
        """Get call logs for a specific date"""
        logs = []
        for call_log in self.call_logs.values():
            if call_log.start_time.strftime("%Y-%m-%d") == date:
                logs.append(call_log)
        return logs
    
    def get_call_logs_by_outcome(self, outcome: str) -> List[CallLog]:
        """Get call logs with specific outcome"""
        logs = []
        for call_log in self.call_logs.values():
            if call_log.outcome == outcome:
                logs.append(call_log)
        return logs
    
    def get_quality_metrics(self) -> Dict[str, Any]:
        """Get quality metrics for all calls"""
        if not self.call_logs:
            return {}
        
        total_calls = len(self.call_logs)
        completed_calls = len([log for log in self.call_logs.values() if log.outcome != "incomplete"])
        appointments_scheduled = len([log for log in self.call_logs.values() if log.appointment_scheduled])
        emergencies_handled = len([log for log in self.call_logs.values() if log.emergency_handled])
        
        quality_scores = [log.quality_score for log in self.call_logs.values() if log.quality_score is not None]
        avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        call_durations = [log.call_duration for log in self.call_logs.values() if log.call_duration is not None]
        avg_call_duration = sum(call_durations) / len(call_durations) if call_durations else 0
        
        return {
            "total_calls": total_calls,
            "completed_calls": completed_calls,
            "completion_rate": (completed_calls / total_calls * 100) if total_calls > 0 else 0,
            "appointments_scheduled": appointments_scheduled,
            "appointment_rate": (appointments_scheduled / total_calls * 100) if total_calls > 0 else 0,
            "emergencies_handled": emergencies_handled,
            "average_quality_score": round(avg_quality_score, 2),
            "average_call_duration": round(avg_call_duration, 2)
        }
    
    def export_call_logs(self, filename: str = None) -> str:
        """Export call logs to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"call_logs_export_{timestamp}.json"
        
        filepath = os.path.join(self.log_directory, filename)
        
        try:
            # Convert to serializable format
            serializable_logs = {}
            for session_id, call_log in self.call_logs.items():
                serializable_logs[session_id] = asdict(call_log)
                # Convert datetime objects to strings
                if serializable_logs[session_id]["start_time"]:
                    serializable_logs[session_id]["start_time"] = serializable_logs[session_id]["start_time"].isoformat()
                if serializable_logs[session_id]["end_time"]:
                    serializable_logs[session_id]["end_time"] = serializable_logs[session_id]["end_time"].isoformat()
            
            with open(filepath, 'w') as f:
                json.dump(serializable_logs, f, indent=2)
            
            self.logger.info(f"Call logs exported to: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to export call logs: {e}")
            return ""
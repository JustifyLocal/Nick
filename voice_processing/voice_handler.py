"""
Voice Processing Handler for Ted Sink Law Voice Receptionist AI
Handles speech-to-text and text-to-speech conversion
"""
import os
import tempfile
import logging
from typing import Optional, Tuple, Dict
from pathlib import Path

import whisper
import torch
import torchaudio
from elevenlabs import generate, save, set_api_key, Voice, VoiceSettings
from elevenlabs.api import History

from config.settings import settings


class VoiceHandler:
    """
    Handles voice input/output processing for the AI receptionist
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize Whisper model for speech-to-text
        self.whisper_model = whisper.load_model("base")
        
        # Configure ElevenLabs for text-to-speech
        set_api_key(settings.elevenlabs_api_key)
        
        # Voice settings for Ted Sink Law brand
        self.voice_settings = VoiceSettings(
            stability=settings.voice_stability,
            similarity_boost=settings.voice_similarity_boost,
            style=0.0,
            use_speaker_boost=True
        )
        
        # Create temporary directory for audio files
        self.temp_dir = Path(tempfile.mkdtemp())
        self.logger.info(f"Voice handler initialized with temp directory: {self.temp_dir}")
    
    def speech_to_text(self, audio_file_path: str) -> Tuple[str, Dict]:
        """
        Convert speech to text using OpenAI Whisper
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Tuple of (transcribed_text, metadata)
        """
        try:
            self.logger.info(f"Processing speech-to-text for: {audio_file_path}")
            
            # Load and transcribe audio
            result = self.whisper_model.transcribe(
                audio_file_path,
                language="en",
                task="transcribe"
            )
            
            transcribed_text = result["text"].strip()
            metadata = {
                "language": result.get("language", "en"),
                "confidence": result.get("confidence", 0.0),
                "segments": len(result.get("segments", [])),
                "duration": result.get("duration", 0.0)
            }
            
            self.logger.info(f"Transcription completed: '{transcribed_text[:100]}...'")
            return transcribed_text, metadata
            
        except Exception as e:
            self.logger.error(f"Error in speech-to-text: {str(e)}")
            return "", {"error": str(e)}
    
    def text_to_speech(self, text: str, output_path: Optional[str] = None) -> Tuple[str, Dict]:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: Text to convert to speech
            output_path: Optional output path for audio file
            
        Returns:
            Tuple of (audio_file_path, metadata)
        """
        try:
            self.logger.info(f"Processing text-to-speech: '{text[:100]}...'")
            
            # Generate audio using ElevenLabs
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=settings.voice_id,
                    settings=self.voice_settings
                ),
                model="eleven_monolingual_v1"
            )
            
            # Save audio file
            if output_path is None:
                output_path = self.temp_dir / f"response_{hash(text) % 10000}.mp3"
            
            save(audio, str(output_path))
            
            metadata = {
                "text_length": len(text),
                "word_count": len(text.split()),
                "voice_id": settings.voice_id,
                "model": "eleven_monolingual_v1",
                "file_size": os.path.getsize(output_path)
            }
            
            self.logger.info(f"Text-to-speech completed: {output_path}")
            return str(output_path), metadata
            
        except Exception as e:
            self.logger.error(f"Error in text-to-speech: {str(e)}")
            return "", {"error": str(e)}
    
    def process_conversation_turn(self, audio_input_path: str, response_text: str) -> Dict:
        """
        Process a complete conversation turn (speech-to-text + text-to-speech)
        
        Args:
            audio_input_path: Path to input audio file
            response_text: Text response to convert to speech
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Step 1: Speech to text
            transcribed_text, stt_metadata = self.speech_to_text(audio_input_path)
            
            if not transcribed_text:
                return {
                    "success": False,
                    "error": "Failed to transcribe audio",
                    "stt_metadata": stt_metadata
                }
            
            # Step 2: Text to speech
            audio_output_path, tts_metadata = self.text_to_speech(response_text)
            
            if not audio_output_path:
                return {
                    "success": False,
                    "error": "Failed to generate speech",
                    "transcribed_text": transcribed_text,
                    "stt_metadata": stt_metadata,
                    "tts_metadata": tts_metadata
                }
            
            return {
                "success": True,
                "transcribed_text": transcribed_text,
                "response_text": response_text,
                "audio_output_path": audio_output_path,
                "stt_metadata": stt_metadata,
                "tts_metadata": tts_metadata
            }
            
        except Exception as e:
            self.logger.error(f"Error in conversation turn processing: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_brand_voice_prompt(self) -> str:
        """
        Create a text prompt that demonstrates Ted Sink Law's brand voice
        for voice training/optimization
        """
        return """
        Thank you for calling Ted Law, the next-generation personal injury law firm. 
        This is Sarah, your AI legal assistant. How can I help you today?
        
        We offer completely free consultations with no obligation, and we don't charge 
        any fees unless we win your case. Our team uses 21st century technology to 
        provide personal attention and rapid response to all our clients.
        
        We handle all types of personal injury cases throughout South Carolina and Georgia, 
        including car accidents, truck accidents, workers' compensation, and wrongful death cases.
        
        I can schedule you for a free consultation today - we guarantee you'll speak with 
        an attorney or case manager the same day. We won't back down from a fight, and 
        we're here to help take you from one of the worst days of your life to one of the best.
        """
    
    def optimize_voice_settings(self, sample_text: Optional[str] = None) -> Dict:
        """
        Optimize voice settings for Ted Sink Law's brand voice
        
        Args:
            sample_text: Optional sample text for testing
            
        Returns:
            Dictionary with optimization results
        """
        try:
            if sample_text is None:
                sample_text = self.create_brand_voice_prompt()
            
            # Test different voice settings
            test_settings = [
                VoiceSettings(stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True),
                VoiceSettings(stability=0.7, similarity_boost=0.8, style=0.1, use_speaker_boost=True),
                VoiceSettings(stability=0.6, similarity_boost=0.7, style=0.0, use_speaker_boost=True)
            ]
            
            results = []
            for i, test_setting in enumerate(test_settings):
                try:
                    audio = generate(
                        text=sample_text,
                        voice=Voice(
                            voice_id=settings.voice_id,
                            settings=test_setting
                        ),
                        model="eleven_monolingual_v1"
                    )
                    
                    test_output_path = self.temp_dir / f"voice_test_{i}.mp3"
                    save(audio, str(test_output_path))
                    
                    results.append({
                        "setting_index": i,
                        "settings": {
                            "stability": test_setting.stability,
                            "similarity_boost": test_setting.similarity_boost,
                            "style": test_setting.style
                        },
                        "output_path": str(test_output_path),
                        "success": True
                    })
                    
                except Exception as e:
                    results.append({
                        "setting_index": i,
                        "settings": {
                            "stability": test_setting.stability,
                            "similarity_boost": test_setting.similarity_boost,
                            "style": test_setting.style
                        },
                        "error": str(e),
                        "success": False
                    })
            
            return {
                "success": True,
                "test_results": results,
                "recommended_setting": results[0] if results else None
            }
            
        except Exception as e:
            self.logger.error(f"Error in voice optimization: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_voice_history(self, limit: int = 10) -> Dict:
        """
        Get recent voice generation history from ElevenLabs
        
        Args:
            limit: Number of recent items to retrieve
            
        Returns:
            Dictionary with voice history
        """
        try:
            history = History.from_api()
            recent_items = history.history[:limit]
            
            return {
                "success": True,
                "history": [
                    {
                        "id": item.history_id,
                        "text": item.text,
                        "voice_id": item.voice_id,
                        "created_at": item.created_at.isoformat() if item.created_at else None,
                        "duration": item.duration,
                        "file_size": item.file_size
                    }
                    for item in recent_items
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting voice history: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files"""
        try:
            for file_path in self.temp_dir.glob("*.mp3"):
                file_path.unlink()
            self.logger.info("Temporary audio files cleaned up")
        except Exception as e:
            self.logger.error(f"Error cleaning up temp files: {str(e)}")
    
    def get_audio_info(self, audio_file_path: str) -> Dict:
        """
        Get information about an audio file
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary with audio file information
        """
        try:
            if not os.path.exists(audio_file_path):
                return {"error": "File not found"}
            
            # Load audio file
            waveform, sample_rate = torchaudio.load(audio_file_path)
            
            # Calculate duration
            duration = waveform.shape[1] / sample_rate
            
            # Get file size
            file_size = os.path.getsize(audio_file_path)
            
            return {
                "file_path": audio_file_path,
                "duration_seconds": duration,
                "sample_rate": sample_rate,
                "channels": waveform.shape[0],
                "file_size_bytes": file_size,
                "file_size_mb": file_size / (1024 * 1024)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting audio info: {str(e)}")
            return {"error": str(e)}
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.cleanup_temp_files()
        except:
            pass
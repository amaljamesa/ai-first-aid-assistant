"""
LIFELINE AI - Voice Processing Service
Speech-to-text conversion for voice inputs
"""

import base64
import io
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class VoiceProcessor:
    """Process voice/audio input to text"""
    
    def __init__(self):
        self.ai_enabled = settings.AI_ENABLED
        self.openai_key = settings.OPENAI_API_KEY
        
    async def transcribe(
        self,
        audio_data: str,
        format: str = "wav"
    ) -> str:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Base64 encoded audio data
            format: Audio format (wav, mp3, m4a, flac)
            
        Returns:
            Transcribed text
        """
        try:
            if self.ai_enabled and self.openai_key:
                return await self._transcribe_with_ai(audio_data, format)
            else:
                # Fallback: return placeholder
                logger.warning("Voice transcription requires AI service. Returning placeholder.")
                return "Voice input received. Please provide text description of the emergency."
                
        except Exception as e:
            logger.error(f"Voice transcription error: {str(e)}")
            return "Unable to process voice input. Please try text input instead."
    
    async def _transcribe_with_ai(
        self,
        audio_data: str,
        format: str
    ) -> str:
        """Transcribe using OpenAI Whisper API"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_data)
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = f"audio.{format}"
            
            # Transcribe
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
            
            return transcript.text
            
        except Exception as e:
            logger.error(f"OpenAI transcription error: {str(e)}")
            raise Exception(f"Voice transcription failed: {str(e)}")

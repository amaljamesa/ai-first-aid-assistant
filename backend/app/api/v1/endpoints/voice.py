"""
LIFELINE AI - Voice Input Processing Endpoint
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.models.schemas import VoiceInputRequest, EmergencyRequest, ApiResponse
from app.services.ai.voice_processor import VoiceProcessor
from app.services.ai.emergency_classifier import EmergencyClassifier
from app.core.config import settings

router = APIRouter()


@router.post("/process", response_model=ApiResponse)
async def process_voice_input(request: VoiceInputRequest) -> Dict[str, Any]:
    """
    Process voice/audio input and detect emergency
    
    - **audio**: Base64 encoded audio data
    - **format**: Audio format (wav, mp3, m4a, flac)
    - **location**: Optional user location
    """
    try:
        # Validate audio format
        if request.format.lower() not in settings.SUPPORTED_AUDIO_FORMATS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error": {
                        "code": "UNSUPPORTED_FORMAT",
                        "message": f"Audio format '{request.format}' not supported. Supported formats: {', '.join(settings.SUPPORTED_AUDIO_FORMATS)}",
                    },
                    "timestamp": None,
                }
            )
        
        # Process voice to text
        voice_processor = VoiceProcessor()
        transcribed_text = await voice_processor.transcribe(
            audio_data=request.audio,
            format=request.format
        )
        
        # Create emergency input from transcription
        emergency_input = {
            "type": "text",
            "content": transcribed_text,
            "timestamp": None,
            "location": request.location.dict() if request.location else None,
        }
        
        # Use emergency detection endpoint logic
        emergency_request = EmergencyRequest(input=emergency_input)
        
        # Import here to avoid circular dependency
        from app.api.v1.endpoints.emergency import detect_emergency
        
        return await detect_emergency(emergency_request)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "VOICE_PROCESSING_ERROR",
                    "message": str(e),
                },
                "timestamp": None,
            }
        )


@router.get("/health")
async def health_check():
    """Voice service health check"""
    return {"status": "healthy", "service": "voice"}

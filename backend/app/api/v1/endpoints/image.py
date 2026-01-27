"""
LIFELINE AI - Image Input Processing Endpoint
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.models.schemas import ImageInputRequest, EmergencyRequest, ApiResponse
from app.services.ai.image_processor import ImageProcessor
from app.services.ai.emergency_classifier import EmergencyClassifier
from app.core.config import settings

router = APIRouter()


@router.post("/process", response_model=ApiResponse)
async def process_image_input(request: ImageInputRequest) -> Dict[str, Any]:
    """
    Process image input and detect emergency
    
    - **image**: Base64 encoded image data
    - **format**: Image format (jpg, jpeg, png, webp)
    - **location**: Optional user location
    """
    try:
        # Validate image format
        if request.format.lower() not in settings.SUPPORTED_IMAGE_FORMATS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error": {
                        "code": "UNSUPPORTED_FORMAT",
                        "message": f"Image format '{request.format}' not supported. Supported formats: {', '.join(settings.SUPPORTED_IMAGE_FORMATS)}",
                    },
                    "timestamp": None,
                }
            )
        
        # Process image
        image_processor = ImageProcessor()
        image_description = await image_processor.analyze(
            image_data=request.image,
            format=request.format
        )
        
        # Create emergency input from image analysis
        emergency_input = {
            "type": "text",
            "content": image_description,
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
                    "code": "IMAGE_PROCESSING_ERROR",
                    "message": str(e),
                },
                "timestamp": None,
            }
        )


@router.get("/health")
async def health_check():
    """Image service health check"""
    return {"status": "healthy", "service": "image"}

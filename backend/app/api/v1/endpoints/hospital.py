"""
LIFELINE AI - Hospital Finder Endpoint
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List

from app.models.schemas import HospitalSearchRequest, Hospital, ApiResponse
from app.services.location.hospital_finder import HospitalFinder
from app.core.config import settings

router = APIRouter()


@router.post("/nearby", response_model=ApiResponse)
async def find_nearby_hospitals(request: HospitalSearchRequest) -> Dict[str, Any]:
    """
    Find nearby hospitals based on location
    
    - **location**: User's current location (latitude, longitude)
    - **radius**: Search radius in kilometers (default: 10km, max: 100km)
    """
    try:
        hospital_finder = HospitalFinder()
        hospitals = await hospital_finder.find_nearby(
            location=request.location,
            radius=request.radius
        )
        
        # Limit results
        hospitals = hospitals[:settings.MAX_HOSPITAL_RESULTS]
        
        return {
            "success": True,
            "data": [hospital.dict() for hospital in hospitals],
            "timestamp": None,
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "HOSPITAL_SEARCH_ERROR",
                    "message": str(e),
                },
                "timestamp": None,
            }
        )


@router.get("/health")
async def health_check():
    """Hospital service health check"""
    return {"status": "healthy", "service": "hospitals"}

"""
LIFELINE AI - Emergency Detection Endpoint
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from datetime import datetime

from app.models.schemas import (
    EmergencyRequest,
    EmergencyResponse,
    ApiResponse,
    FirstAidRequest,
    FirstAidInstruction,
    EmergencyDetection,
)
from app.services.ai.emergency_classifier import EmergencyClassifier
from app.services.ai.severity_scorer import SeverityScorer
from app.services.ai.first_aid_generator import FirstAidGenerator
from app.services.location.hospital_finder import HospitalFinder
from app.core.config import settings

router = APIRouter()


@router.post("/analyze", response_model=ApiResponse)
async def analyze_emergency(request: EmergencyRequest) -> Dict[str, Any]:
    """
    Analyze emergency input and provide complete response with instructions
    
    - **input**: Emergency input (text, voice, or image)
    - **userId**: Optional user identifier
    - **sessionId**: Optional session identifier
    """
    try:
        # Initialize services
        classifier = EmergencyClassifier()
        scorer = SeverityScorer()
        
        # Classify emergency
        classification_result = await classifier.classify(
            input_type=request.input.type,
            content=request.input.content
        )
        
        # Score severity
        severity_result = await scorer.score(
            emergency_type=classification_result["type"],
            content=request.input.content,
            classification_confidence=classification_result["confidence"]
        )
        
        # Determine if emergency call is needed
        should_call = (
            severity_result["severity"] == "critical" or
            severity_result["score"] >= settings.CRITICAL_SEVERITY_THRESHOLD
        )
        
        # Get first aid instructions
        first_aid_service = FirstAidGenerator()
        instructions = await first_aid_service.generate_instructions(
            emergency_type=classification_result["type"],
            severity=severity_result["severity"]
        )
        
        # Find nearest hospital if location provided
        nearest_hospital = None
        if request.input.location:
            hospital_finder = HospitalFinder()
            hospitals = await hospital_finder.find_nearby(
                location=request.input.location,
                radius=settings.DEFAULT_HOSPITAL_RADIUS
            )
            if hospitals:
                nearest_hospital = hospitals[0]
        
        # Build detection object
        detection = EmergencyDetection(
            emergencyType=classification_result["type"],
            severity=severity_result["severity"],
            confidence=classification_result["confidence"],
            detectedAt=datetime.now(),
        )
        
        # Build response
        response_data = EmergencyResponse(
            detection=detection,
            instructions=[FirstAidInstruction(**inst) for inst in instructions],
            shouldCallEmergency=should_call,
            nearestHospital=nearest_hospital,
            estimatedResponseTime=15 if should_call else None,
        )
        
        return {
            "success": True,
            "data": response_data.dict(),
            "timestamp": datetime.now().isoformat(),
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "ANALYSIS_ERROR",
                    "message": str(e),
                },
                "timestamp": datetime.now().isoformat(),
            }
        )


@router.post("/detect", response_model=ApiResponse)
async def detect_emergency(request: EmergencyRequest) -> Dict[str, Any]:
    """
    Detect emergency type and severity from user input
    
    - **input**: Emergency input (text, voice, or image)
    - **userId**: Optional user identifier
    - **sessionId**: Optional session identifier
    """
    try:
        # Initialize services
        classifier = EmergencyClassifier()
        scorer = SeverityScorer()
        
        # Classify emergency
        classification_result = await classifier.classify(
            input_type=request.input.type,
            content=request.input.content
        )
        
        # Score severity
        severity_result = await scorer.score(
            emergency_type=classification_result["type"],
            content=request.input.content,
            classification_confidence=classification_result["confidence"]
        )
        
        # Determine if emergency call is needed
        should_call = (
            severity_result["severity"] == "critical" or
            severity_result["score"] >= settings.CRITICAL_SEVERITY_THRESHOLD
        )
        
        # Get first aid instructions
        first_aid_service = FirstAidGenerator()
        instructions = await first_aid_service.generate_instructions(
            emergency_type=classification_result["type"],
            severity=severity_result["severity"]
        )
        
        # Find nearest hospital if location provided
        nearest_hospital = None
        if request.input.location:
            hospital_finder = HospitalFinder()
            hospitals = await hospital_finder.find_nearby(
                location=request.input.location,
                radius=settings.DEFAULT_HOSPITAL_RADIUS
            )
            if hospitals:
                nearest_hospital = hospitals[0]
        
        # Build response
        response_data = EmergencyResponse(
            detection={
                "emergencyType": classification_result["type"],
                "severity": severity_result["severity"],
                "confidence": classification_result["confidence"],
                "detectedAt": request.input.timestamp.isoformat(),
            },
            instructions=instructions,
            shouldCallEmergency=should_call,
            nearestHospital=nearest_hospital.dict() if nearest_hospital else None,
            estimatedResponseTime=15 if should_call else None,
        )
        
        return {
            "success": True,
            "data": response_data.dict(),
            "timestamp": response_data.detection["detectedAt"],
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "DETECTION_ERROR",
                    "message": str(e),
                },
                "timestamp": None,
            }
        )


@router.post("/first-aid", response_model=ApiResponse)
async def get_first_aid_instructions(request: FirstAidRequest) -> Dict[str, Any]:
    """
    Get first aid instructions for a specific emergency type and severity
    """
    try:
        first_aid_service = FirstAidGenerator()
        instructions = await first_aid_service.generate_instructions(
            emergency_type=request.emergencyType,
            severity=request.severity
        )
        
        # Find nearest hospital if location provided
        nearest_hospital = None
        if request.location:
            hospital_finder = HospitalFinder()
            hospitals = await hospital_finder.find_nearby(
                location=request.location,
                radius=settings.DEFAULT_HOSPITAL_RADIUS
            )
            if hospitals:
                nearest_hospital = hospitals[0]
        
        detection = EmergencyDetection(
            emergencyType=request.emergencyType,
            severity=request.severity,
            confidence=1.0,
            detectedAt=datetime.now(),
        )
        
        response_data = EmergencyResponse(
            detection=detection,
            instructions=[FirstAidInstruction(**inst) for inst in instructions],
            shouldCallEmergency=request.severity == "critical",
            nearestHospital=nearest_hospital,
            estimatedResponseTime=15 if request.severity == "critical" else None,
        )
        
        return {
            "success": True,
            "data": response_data.dict(),
            "timestamp": datetime.now().isoformat(),
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "FIRST_AID_ERROR",
                    "message": str(e),
                },
                "timestamp": None,
            }
        )


@router.get("/health")
async def health_check():
    """Emergency service health check"""
    return {"status": "healthy", "service": "emergency"}

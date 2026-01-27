"""
LIFELINE AI - Pydantic Schemas
Request and response models
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EmergencyType(str, Enum):
    """Emergency type enumeration"""
    MEDICAL = "medical"
    TRAUMA = "trauma"
    CARDIAC = "cardiac"
    RESPIRATORY = "respiratory"
    BURN = "burn"
    POISONING = "poisoning"
    FRACTURE = "fracture"
    BLEEDING = "bleeding"
    UNKNOWN = "unknown"


class SeverityLevel(str, Enum):
    """Severity level enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


class InputType(str, Enum):
    """Input type enumeration"""
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"


class LocationData(BaseModel):
    """Location data model"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    address: Optional[str] = Field(None, description="Formatted address")
    accuracy: Optional[float] = Field(None, description="Location accuracy in meters")


class EmergencyInput(BaseModel):
    """Emergency input model"""
    type: InputType = Field(..., description="Type of input")
    content: str = Field(..., description="Input content (text, base64 image, or audio)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Input timestamp")
    location: Optional[LocationData] = Field(None, description="User location")


class EmergencyRequest(BaseModel):
    """Emergency detection request"""
    input: EmergencyInput = Field(..., description="Emergency input data")
    userId: Optional[str] = Field(None, description="User identifier")
    sessionId: Optional[str] = Field(None, description="Session identifier")


class EmergencyDetection(BaseModel):
    """Emergency detection result"""
    emergencyType: EmergencyType = Field(..., description="Detected emergency type")
    severity: SeverityLevel = Field(..., description="Severity level")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    detectedAt: datetime = Field(default_factory=datetime.now, description="Detection timestamp")


class FirstAidInstruction(BaseModel):
    """First aid instruction step"""
    id: str = Field(..., description="Instruction identifier")
    step: int = Field(..., ge=1, description="Step number")
    title: str = Field(..., description="Step title")
    description: str = Field(..., description="Step description")
    imageUrl: Optional[str] = Field(None, description="Instruction image URL")
    animationUrl: Optional[str] = Field(None, description="Instruction animation URL")
    duration: Optional[int] = Field(None, ge=0, description="Step duration in seconds")


class Hospital(BaseModel):
    """Hospital information model"""
    id: str = Field(..., description="Hospital identifier")
    name: str = Field(..., description="Hospital name")
    address: str = Field(..., description="Hospital address")
    phone: str = Field(..., description="Hospital phone number")
    distance: float = Field(..., ge=0, description="Distance in kilometers")
    location: LocationData = Field(..., description="Hospital location")
    specialties: Optional[List[str]] = Field(None, description="Medical specialties")


class EmergencyResponse(BaseModel):
    """Emergency response model"""
    detection: EmergencyDetection = Field(..., description="Emergency detection result")
    instructions: List[FirstAidInstruction] = Field(..., description="First aid instructions")
    shouldCallEmergency: bool = Field(..., description="Whether to call emergency services")
    nearestHospital: Optional[Hospital] = Field(None, description="Nearest hospital")
    estimatedResponseTime: Optional[int] = Field(None, ge=0, description="Estimated response time in minutes")


class ApiResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = Field(..., description="Request success status")
    data: Optional[dict] = Field(None, description="Response data")
    error: Optional[dict] = Field(None, description="Error information")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class HospitalSearchRequest(BaseModel):
    """Hospital search request"""
    location: LocationData = Field(..., description="Search location")
    radius: float = Field(default=10.0, ge=0.1, le=100, description="Search radius in kilometers")


class FirstAidRequest(BaseModel):
    """First aid instructions request"""
    emergencyType: str = Field(..., description="Emergency type")
    severity: str = Field(..., description="Severity level")
    location: Optional[LocationData] = Field(None, description="User location")


class VoiceInputRequest(BaseModel):
    """Voice input request"""
    audio: str = Field(..., description="Base64 encoded audio data")
    format: str = Field(default="wav", description="Audio format")
    location: Optional[LocationData] = Field(None, description="User location")


class ImageInputRequest(BaseModel):
    """Image input request"""
    image: str = Field(..., description="Base64 encoded image data")
    format: str = Field(default="jpeg", description="Image format")
    location: Optional[LocationData] = Field(None, description="User location")

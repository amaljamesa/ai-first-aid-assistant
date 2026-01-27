"""
LIFELINE AI - API Router
Main API route aggregator
"""

from fastapi import APIRouter

from app.api.v1.endpoints import emergency, hospital, voice, image

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(emergency.router, prefix="/emergency", tags=["emergency"])
api_router.include_router(hospital.router, prefix="/hospitals", tags=["hospitals"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
api_router.include_router(image.router, prefix="/image", tags=["image"])

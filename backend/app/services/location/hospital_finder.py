"""
LIFELINE AI - Hospital Finder Service
Find nearby hospitals based on location
"""

from typing import List
import logging
import math

from app.models.schemas import LocationData, Hospital
from app.core.config import settings

logger = logging.getLogger(__name__)


class HospitalFinder:
    """Find nearby hospitals"""
    
    def __init__(self):
        # In production, this would connect to a hospital database or API
        # For now, using mock data with real coordinates
        self.hospitals_db = self._load_hospital_database()
    
    def _load_hospital_database(self) -> List[dict]:
        """Load hospital database (mock data for now)"""
        # In production, this would load from a database or external API
        # Example: Google Places API, OpenStreetMap, or custom database
        return [
            {
                "id": "hosp_001",
                "name": "City General Hospital",
                "address": "123 Medical Center Dr, City, State 12345",
                "phone": "+1-555-0100",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "specialties": ["Emergency", "Cardiology", "Trauma"],
            },
            {
                "id": "hosp_002",
                "name": "Regional Medical Center",
                "address": "456 Health Blvd, City, State 12345",
                "phone": "+1-555-0101",
                "latitude": 40.7580,
                "longitude": -73.9855,
                "specialties": ["Emergency", "Pediatrics", "Surgery"],
            },
            {
                "id": "hosp_003",
                "name": "Community Hospital",
                "address": "789 Care Street, City, State 12345",
                "phone": "+1-555-0102",
                "latitude": 40.7505,
                "longitude": -73.9934,
                "specialties": ["Emergency", "Internal Medicine"],
            },
        ]
    
    def _calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """Calculate distance between two coordinates in kilometers (Haversine formula)"""
        R = 6371  # Earth radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(math.radians(lat1)) *
            math.cos(math.radians(lat2)) *
            math.sin(dlon / 2) ** 2
        )
        
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        
        return distance
    
    async def find_nearby(
        self,
        location: LocationData,
        radius: float = 10.0
    ) -> List[Hospital]:
        """
        Find nearby hospitals
        
        Args:
            location: User location
            radius: Search radius in kilometers
            
        Returns:
            List of nearby hospitals sorted by distance
        """
        try:
            nearby_hospitals = []
            
            for hospital_data in self.hospitals_db:
                distance = self._calculate_distance(
                    location.latitude,
                    location.longitude,
                    hospital_data["latitude"],
                    hospital_data["longitude"]
                )
                
                if distance <= radius:
                    hospital = Hospital(
                        id=hospital_data["id"],
                        name=hospital_data["name"],
                        address=hospital_data["address"],
                        phone=hospital_data["phone"],
                        distance=distance,
                        location=LocationData(
                            latitude=hospital_data["latitude"],
                            longitude=hospital_data["longitude"],
                            address=hospital_data["address"],
                        ),
                        specialties=hospital_data.get("specialties"),
                    )
                    nearby_hospitals.append(hospital)
            
            # Sort by distance
            nearby_hospitals.sort(key=lambda x: x.distance)
            
            return nearby_hospitals
            
        except Exception as e:
            logger.error(f"Hospital search error: {str(e)}")
            return []

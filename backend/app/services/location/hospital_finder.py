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
        # Generate hospitals dynamically based on user location
        pass
    
    def _generate_nearby_hospitals(self, user_lat: float, user_lon: float) -> List[dict]:
        """Generate hospitals near user location"""
        import random
        
        hospitals = []
        hospital_names = [
            "General Hospital", "Medical Center", "Community Hospital", 
            "Regional Medical Center", "Emergency Hospital", "City Hospital",
            "Memorial Hospital", "Central Medical Center", "University Hospital"
        ]
        
        # Generate 5-8 hospitals within 50km of user location
        for i in range(random.randint(5, 8)):
            # Random offset within ~50km (roughly 0.45 degrees)
            lat_offset = random.uniform(-0.45, 0.45)
            lon_offset = random.uniform(-0.45, 0.45)
            
            hospital = {
                "id": f"hosp_{i+1:03d}",
                "name": random.choice(hospital_names),
                "address": f"{random.randint(100, 9999)} Medical Dr, Local City",
                "phone": f"+1-555-{random.randint(1000, 9999)}",
                "latitude": user_lat + lat_offset,
                "longitude": user_lon + lon_offset,
                "specialties": random.sample(["Emergency", "Cardiology", "Trauma", "Pediatrics", "Surgery", "Internal Medicine", "Urgent Care"], k=random.randint(2, 4)),
            }
            hospitals.append(hospital)
        
        return hospitals
        """Load hospital database (mock data for now)"""
        # In production, this would load from a database or external API
        # For now, using a broader set of hospitals across different locations
        return [
            # NYC Area
            {
                "id": "hosp_001",
                "name": "City General Hospital",
                "address": "123 Medical Center Dr, New York, NY 10001",
                "phone": "+1-555-0100",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "specialties": ["Emergency", "Cardiology", "Trauma"],
            },
            {
                "id": "hosp_002",
                "name": "Regional Medical Center",
                "address": "456 Health Blvd, New York, NY 10002",
                "phone": "+1-555-0101",
                "latitude": 40.7580,
                "longitude": -73.9855,
                "specialties": ["Emergency", "Pediatrics", "Surgery"],
            },
            # Generic locations that will be closer to most users
            {
                "id": "hosp_003",
                "name": "Community Hospital",
                "address": "789 Care Street, Local City",
                "phone": "+1-555-0102",
                "latitude": 40.0,  # More central location
                "longitude": -75.0,
                "specialties": ["Emergency", "Internal Medicine"],
            },
            {
                "id": "hosp_004",
                "name": "Emergency Medical Center",
                "address": "321 Urgent Care Ave, Local City",
                "phone": "+1-555-0103",
                "latitude": 39.0,
                "longitude": -76.0,
                "specialties": ["Emergency", "Urgent Care"],
            },
            {
                "id": "hosp_005",
                "name": "Central Hospital",
                "address": "555 Main St, Central City",
                "phone": "+1-555-0104",
                "latitude": 41.0,
                "longitude": -74.0,
                "specialties": ["Emergency", "General Medicine"],
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
        Find nearby hospitals - generates hospitals near user location
        """
        try:
            logger.info(f"Searching for hospitals near {location.latitude}, {location.longitude}")
            
            # Generate hospitals near user location
            hospital_data_list = self._generate_nearby_hospitals(location.latitude, location.longitude)
            
            hospitals = []
            for hospital_data in hospital_data_list:
                distance = self._calculate_distance(
                    location.latitude,
                    location.longitude,
                    hospital_data["latitude"],
                    hospital_data["longitude"]
                )
                
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
                hospitals.append(hospital)
            
            # Sort by distance (closest first)
            hospitals.sort(key=lambda x: x.distance)
            
            logger.info(f"Generated {len(hospitals)} hospitals near user location")
            return hospitals
            
        except Exception as e:
            logger.error(f"Hospital search error: {str(e)}")
            return []

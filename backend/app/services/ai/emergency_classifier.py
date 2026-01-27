"""
LIFELINE AI - Emergency Classifier Service
AI-powered emergency type classification
"""

from typing import Dict, Any
import logging

from app.core.config import settings
from app.models.schemas import EmergencyType

logger = logging.getLogger(__name__)


class EmergencyClassifier:
    """Classify emergency type from input content"""
    
    def __init__(self):
        self.ai_enabled = settings.AI_ENABLED
        self.openai_key = settings.OPENAI_API_KEY
        
    async def classify(
        self,
        input_type: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Classify emergency type from input
        
        Args:
            input_type: Type of input (text, voice, image)
            content: Input content
            
        Returns:
            Dictionary with 'type' and 'confidence' keys
        """
        try:
            if self.ai_enabled and self.openai_key:
                return await self._classify_with_ai(content)
            else:
                return await self._classify_with_rules(content)
                
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            # Fallback to rule-based classification
            return await self._classify_with_rules(content)
    
    async def _classify_with_ai(self, content: str) -> Dict[str, Any]:
        """Classify using AI/LLM"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""Analyze the following emergency situation and classify it into one of these categories:
- medical: General medical emergencies (fever, pain, illness)
- trauma: Physical injuries (cuts, bruises, impacts)
- cardiac: Heart-related emergencies (chest pain, heart attack)
- respiratory: Breathing problems (choking, asthma, difficulty breathing)
- burn: Burns and scalds
- poisoning: Poisoning or toxic exposure
- fracture: Broken bones
- bleeding: Severe bleeding or wounds
- unknown: Cannot determine

Emergency description: {content}

Respond in JSON format:
{{
    "type": "category_name",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}"""
            
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an emergency medical classification AI. Analyze emergency situations and classify them accurately."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Validate and normalize result
            emergency_type = result.get("type", "unknown").lower()
            if emergency_type not in [e.value for e in EmergencyType]:
                emergency_type = "unknown"
            
           return {
    "type": result.get("type", "unknown"),
    "severity": result.get("severity", "unknown"),
    "instructions": result.get("instructions", []),
    "call_emergency": result.get("call_emergency", False),
    "confidence": float(result.get("confidence", 0.7)),
}

            
        except Exception as e:
            logger.warning(f"AI classification failed: {str(e)}, falling back to rules")
            return await self._classify_with_rules(content)
    
    async def _classify_with_rules(self, content: str) -> Dict[str, Any]:
        """Rule-based classification fallback"""
        content_lower = content.lower()
        
        # Keyword-based classification
        keywords = {
            "cardiac": ["chest pain", "heart", "cardiac", "heart attack", "cardiac arrest", "palpitations"],
            "respiratory": ["breathing", "choke", "asthma", "shortness of breath", "can't breathe", "suffocating"],
            "bleeding": ["bleeding", "blood", "cut", "wound", "hemorrhage", "laceration"],
            "fracture": ["broken", "fracture", "bone", "dislocated", "sprain"],
            "burn": ["burn", "scald", "fire", "hot", "thermal"],
            "poisoning": ["poison", "toxic", "overdose", "ingested", "chemical"],
            "trauma": ["injury", "hurt", "accident", "fall", "hit", "struck"],
            "medical": ["fever", "pain", "sick", "ill", "nausea", "dizzy", "unconscious"],
        }
        
        scores = {}
        for emergency_type, keyword_list in keywords.items():
            score = sum(1 for keyword in keyword_list if keyword in content_lower)
            if score > 0:
                scores[emergency_type] = score
        
        if scores:
            # Get type with highest score
            emergency_type = max(scores, key=scores.get)
            confidence = min(0.9, 0.5 + (scores[emergency_type] * 0.1))
        else:
            emergency_type = "unknown"
            confidence = 0.3
        
        return {
            "type": emergency_type,
            "confidence": confidence,
            "reasoning": "Rule-based classification",
        }

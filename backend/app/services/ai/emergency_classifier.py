"""
LIFELINE AI - Emergency Classifier Service
AI-powered emergency type classification
"""

from typing import Dict, Any
import logging
import json

from app.core.config import settings
from app.models.schemas import EmergencyType
from app.services.ai.custom_classifier import CustomEmergencyClassifier

logger = logging.getLogger(__name__)


class EmergencyClassifier:
    """Classify emergency type from input content"""
    
    def __init__(self):
        self.ai_enabled = settings.AI_ENABLED
        self.openai_key = settings.OPENAI_API_KEY
        self.custom_classifier = CustomEmergencyClassifier()
        
    async def classify(
        self,
        input_type: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Classify emergency type from input
        """
        try:
            # Try custom model first
            if self.custom_classifier.is_available():
                return self.custom_classifier.classify(content)
            elif self.ai_enabled and self.openai_key:
                return await self._classify_with_ai(content)
            else:
                return await self._classify_with_rules(content)
                
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            return await self._classify_with_rules(content)
    
    async def _classify_with_ai(self, content: str) -> Dict[str, Any]:
        """Classify using AI/LLM"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""
Analyze the following emergency situation and classify it into one of these categories:
- medical
- trauma
- cardiac
- respiratory
- burn
- poisoning
- fracture
- bleeding
- unknown

Emergency description: {content}

Respond ONLY in JSON:
{{
    "type": "category_name",
    "confidence": 0.0,
    "reasoning": "short explanation"
}}
"""
            
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an emergency medical classification AI."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            
            result = json.loads(response.choices[0].message.content)

            # Normalize + validate
            emergency_type = result.get("type", "unknown").lower()
            if emergency_type not in [e.value for e in EmergencyType]:
                emergency_type = "unknown"

            return {
                "type": emergency_type,
                "confidence": float(result.get("confidence", 0.7)),
                "reasoning": result.get("reasoning", "AI classification"),
                "source": "ai"
            }

        except Exception as e:
            logger.warning(f"AI classification failed: {str(e)}, falling back to rules")
            return await self._classify_with_rules(content)
    
    async def _classify_with_rules(self, content: str) -> Dict[str, Any]:
        """Rule-based classification fallback"""
        content_lower = content.lower()
        
        keywords = {
            "cuts-wounds": ["cut", "wound", "bleeding", "blood", "gash", "laceration", "scrape"],
            "burns": ["burn", "scald", "fire", "hot", "steam", "chemical burn"],
            "choking": ["choking", "can't breathe", "swallowed", "stuck in throat", "gagging"],
            "cpr": ["unconscious", "not breathing", "no pulse", "cardiac arrest", "collapsed"],
            "sprains": ["sprain", "twisted", "ankle", "wrist", "swollen", "can't move"],
            "nosebleed": ["nosebleed", "nose bleeding", "bloody nose"],
            "allergic-reaction": ["allergic", "rash", "hives", "swelling", "itchy", "reaction"],
            "fainting": ["fainted", "dizzy", "lightheaded", "passed out", "unconscious"],
        }
        
        scores = {}
        for emergency_type, keyword_list in keywords.items():
            score = sum(1 for keyword in keyword_list if keyword in content_lower)
            if score > 0:
                scores[emergency_type] = score
        
        if scores:
            emergency_type = max(scores, key=scores.get)
            confidence = min(0.9, 0.5 + (scores[emergency_type] * 0.1))
        else:
            emergency_type = "cuts-wounds"  # Default to basic first aid
            confidence = 0.3
        
        return {
            "type": emergency_type,
            "confidence": confidence,
            "reasoning": "Rule-based classification",
            "source": "rules"
        }

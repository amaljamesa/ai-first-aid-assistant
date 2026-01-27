"""
LIFELINE AI - Severity Scorer Service
AI-powered severity assessment
"""

from typing import Dict, Any
import logging

from app.core.config import settings
from app.models.schemas import SeverityLevel

logger = logging.getLogger(__name__)


class SeverityScorer:
    """Score emergency severity level"""
    
    def __init__(self):
        self.ai_enabled = settings.AI_ENABLED
        self.openai_key = settings.OPENAI_API_KEY
        
    async def score(
        self,
        emergency_type: str,
        content: str,
        classification_confidence: float = 0.7
    ) -> Dict[str, Any]:
        """
        Score emergency severity
        
        Args:
            emergency_type: Detected emergency type
            content: Emergency description
            classification_confidence: Confidence from classification
            
        Returns:
            Dictionary with 'severity' and 'score' keys
        """
        try:
            if self.ai_enabled and self.openai_key:
                return await self._score_with_ai(emergency_type, content)
            else:
                return await self._score_with_rules(emergency_type, content, classification_confidence)
                
        except Exception as e:
            logger.error(f"Severity scoring error: {str(e)}")
            return await self._score_with_rules(emergency_type, content, classification_confidence)
    
    async def _score_with_ai(self, emergency_type: str, content: str) -> Dict[str, Any]:
        """Score severity using AI/LLM"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""Assess the severity of this emergency situation:

Emergency Type: {emergency_type}
Description: {content}

Rate the severity on a scale of 0.0 to 1.0:
- 0.8-1.0: CRITICAL - Life-threatening, immediate danger
- 0.6-0.79: HIGH - Serious, needs urgent attention
- 0.4-0.59: MODERATE - Needs medical attention but not immediately life-threatening
- 0.0-0.39: LOW - Minor issue, can wait or self-treat

Respond in JSON format:
{{
    "severity": "critical|high|moderate|low",
    "score": 0.0-1.0,
    "reasoning": "brief explanation"
}}"""
            
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an emergency medical severity assessment AI. Assess emergency severity accurately."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Validate severity level
            severity = result.get("severity", "moderate").lower()
            if severity not in [s.value for s in SeverityLevel]:
                # Map score to severity if invalid
                score = float(result.get("score", 0.5))
                if score >= 0.8:
                    severity = "critical"
                elif score >= 0.6:
                    severity = "high"
                elif score >= 0.4:
                    severity = "moderate"
                else:
                    severity = "low"
            
            return {
                "severity": severity,
                "score": float(result.get("score", 0.5)),
                "reasoning": result.get("reasoning", ""),
            }
            
        except Exception as e:
            logger.warning(f"AI severity scoring failed: {str(e)}, falling back to rules")
            return await self._score_with_rules(emergency_type, content, 0.7)
    
    async def _score_with_rules(
        self,
        emergency_type: str,
        content: str,
        confidence: float
    ) -> Dict[str, Any]:
        """Rule-based severity scoring"""
        content_lower = content.lower()
        
        # Critical indicators
        critical_keywords = [
            "unconscious", "not breathing", "cardiac arrest", "severe bleeding",
            "can't breathe", "choking", "severe pain", "chest pain", "heart attack"
        ]
        
        # High severity indicators
        high_keywords = [
            "broken", "fracture", "burn", "poison", "severe", "urgent", "emergency"
        ]
        
        # Moderate indicators
        moderate_keywords = [
            "pain", "hurt", "injury", "bleeding", "cut", "wound"
        ]
        
        critical_count = sum(1 for keyword in critical_keywords if keyword in content_lower)
        high_count = sum(1 for keyword in high_keywords if keyword in content_lower)
        moderate_count = sum(1 for keyword in moderate_keywords if keyword in content_lower)
        
        # Determine severity based on keywords and emergency type
        if critical_count > 0 or emergency_type in ["cardiac", "respiratory"]:
            severity = "critical"
            score = min(1.0, 0.8 + (critical_count * 0.05))
        elif high_count > 0 or emergency_type in ["bleeding", "fracture", "burn"]:
            severity = "high"
            score = min(0.79, 0.6 + (high_count * 0.05))
        elif moderate_count > 0:
            severity = "moderate"
            score = min(0.59, 0.4 + (moderate_count * 0.05))
        else:
            severity = "low"
            score = 0.3
        
        # Adjust based on classification confidence
        score = score * confidence
        
        return {
            "severity": severity,
            "score": score,
            "reasoning": "Rule-based severity assessment",
        }

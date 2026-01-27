"""
LIFELINE AI - First Aid Instruction Generator
Generate step-by-step first aid instructions
"""

from typing import List, Dict, Any
import logging
import uuid

from app.models.schemas import FirstAidInstruction
from app.core.config import settings

logger = logging.getLogger(__name__)


class FirstAidGenerator:
    """Generate first aid instructions for emergencies"""
    
    def __init__(self):
        self.ai_enabled = settings.AI_ENABLED
        self.openai_key = settings.OPENAI_API_KEY
        
    async def generate_instructions(
        self,
        emergency_type: str,
        severity: str
    ) -> List[Dict[str, Any]]:
        """
        Generate first aid instructions
        
        Args:
            emergency_type: Type of emergency
            severity: Severity level
            
        Returns:
            List of first aid instruction dictionaries
        """
        try:
            if self.ai_enabled and self.openai_key:
                return await self._generate_with_ai(emergency_type, severity)
            else:
                return await self._generate_with_templates(emergency_type, severity)
                
        except Exception as e:
            logger.error(f"Instruction generation error: {str(e)}")
            return await self._generate_with_templates(emergency_type, severity)
    
    async def _generate_with_ai(
        self,
        emergency_type: str,
        severity: str
    ) -> List[Dict[str, Any]]:
        """Generate instructions using AI/LLM"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""Generate step-by-step first aid instructions for a {severity} {emergency_type} emergency.

Provide clear, actionable steps that a layperson can follow. Include:
- Immediate actions to take
- What NOT to do
- When to call emergency services
- How to monitor the situation

Respond in JSON format with an array of instructions:
{{
    "instructions": [
        {{
            "step": 1,
            "title": "Step title",
            "description": "Detailed step description",
            "duration": 30
        }},
        ...
    ]
}}"""
            
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a first aid instruction generator. Provide clear, accurate, and actionable first aid steps."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            instructions = result.get("instructions", [])
            
            # Convert to FirstAidInstruction format
            formatted_instructions = []
            for idx, instruction in enumerate(instructions, 1):
                formatted_instructions.append({
                    "id": str(uuid.uuid4()),
                    "step": instruction.get("step", idx),
                    "title": instruction.get("title", f"Step {idx}"),
                    "description": instruction.get("description", ""),
                    "duration": instruction.get("duration"),
                })
            
            return formatted_instructions
            
        except Exception as e:
            logger.warning(f"AI instruction generation failed: {str(e)}, falling back to templates")
            return await self._generate_with_templates(emergency_type, severity)
    
    async def _generate_with_templates(
        self,
        emergency_type: str,
        severity: str
    ) -> List[Dict[str, Any]]:
        """Generate instructions from templates"""
        templates = {
            "cardiac": [
                {
                    "title": "Call Emergency Services",
                    "description": "Immediately call 911 or your local emergency number. This is a medical emergency.",
                    "duration": 0,
                },
                {
                    "title": "Check Responsiveness",
                    "description": "Check if the person is conscious and responsive. Gently shake their shoulders and ask if they're okay.",
                    "duration": 10,
                },
                {
                    "title": "Start CPR if Needed",
                    "description": "If the person is unresponsive and not breathing, begin CPR. Place hands on center of chest and push hard and fast (100-120 compressions per minute).",
                    "duration": 120,
                },
                {
                    "title": "Use AED if Available",
                    "description": "If an Automated External Defibrillator (AED) is available, follow its instructions immediately.",
                    "duration": 60,
                },
            ],
            "respiratory": [
                {
                    "title": "Assess Breathing",
                    "description": "Check if the person is breathing. Look for chest movement and listen for breath sounds.",
                    "duration": 10,
                },
                {
                    "title": "Clear Airway",
                    "description": "If the person is choking, perform the Heimlich maneuver. Stand behind them, place hands above navel, and give quick upward thrusts.",
                    "duration": 30,
                },
                {
                    "title": "Call Emergency Services",
                    "description": "If breathing doesn't improve, call 911 immediately.",
                    "duration": 0,
                },
                {
                    "title": "Monitor Condition",
                    "description": "Continue monitoring breathing and consciousness until help arrives.",
                    "duration": 0,
                },
            ],
            "bleeding": [
                {
                    "title": "Apply Direct Pressure",
                    "description": "Use a clean cloth or bandage to apply firm, direct pressure to the wound.",
                    "duration": 300,
                },
                {
                    "title": "Elevate the Injury",
                    "description": "If possible, raise the injured area above the level of the heart to reduce blood flow.",
                    "duration": 0,
                },
                {
                    "title": "Call Emergency Services",
                    "description": "If bleeding is severe or doesn't stop, call 911 immediately.",
                    "duration": 0,
                },
                {
                    "title": "Keep Pressure Until Help Arrives",
                    "description": "Continue applying pressure. Do not remove the bandage even if it becomes soaked with blood.",
                    "duration": 0,
                },
            ],
            "fracture": [
                {
                    "title": "Immobilize the Injury",
                    "description": "Keep the injured area still. Do not try to realign bones or push a bone back in.",
                    "duration": 0,
                },
                {
                    "title": "Apply Ice",
                    "description": "Apply a cold pack or ice wrapped in cloth to reduce swelling and pain.",
                    "duration": 600,
                },
                {
                    "title": "Seek Medical Attention",
                    "description": "Go to the emergency room or call 911 if the fracture is severe or the person cannot move.",
                    "duration": 0,
                },
                {
                    "title": "Monitor for Shock",
                    "description": "Watch for signs of shock: pale skin, rapid pulse, dizziness. Keep the person calm and lying down.",
                    "duration": 0,
                },
            ],
            "burn": [
                {
                    "title": "Cool the Burn",
                    "description": "Hold the burned area under cool (not cold) running water for 10-20 minutes, or apply a cool, wet compress.",
                    "duration": 1200,
                },
                {
                    "title": "Remove Tight Items",
                    "description": "Remove rings, bracelets, or tight clothing from the burned area before it swells.",
                    "duration": 30,
                },
                {
                    "title": "Cover the Burn",
                    "description": "Cover the burn with a sterile, non-adhesive bandage or clean cloth.",
                    "duration": 0,
                },
                {
                    "title": "Seek Medical Attention",
                    "description": "Call 911 for severe burns, or seek medical attention if the burn is larger than 3 inches or affects face, hands, or joints.",
                    "duration": 0,
                },
            ],
        }
        
        # Get template or use default
        instructions = templates.get(emergency_type, [
            {
                "title": "Assess the Situation",
                "description": "Carefully assess the emergency situation and ensure your own safety first.",
                "duration": 30,
            },
            {
                "title": "Call Emergency Services",
                "description": "Call 911 or your local emergency number if the situation is serious.",
                "duration": 0,
            },
            {
                "title": "Provide Basic Care",
                "description": "Provide basic first aid care while waiting for professional help to arrive.",
                "duration": 0,
            },
            {
                "title": "Monitor the Person",
                "description": "Continue monitoring the person's condition and stay with them until help arrives.",
                "duration": 0,
            },
        ])
        
        # Format instructions
        formatted = []
        for idx, instruction in enumerate(instructions, 1):
            formatted.append({
                "id": str(uuid.uuid4()),
                "step": idx,
                "title": instruction["title"],
                "description": instruction["description"],
                "duration": instruction.get("duration"),
            })
        
        return formatted

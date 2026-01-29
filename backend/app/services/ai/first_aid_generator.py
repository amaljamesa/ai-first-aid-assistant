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
            "cuts-wounds": [
                {
                    "title": "Stop the Bleeding",
                    "description": "Apply direct pressure to the wound with a clean cloth or bandage. Press firmly and continuously.",
                    "duration": 300,
                },
                {
                    "title": "Clean the Wound",
                    "description": "Once bleeding stops, gently clean the wound with clean water. Remove any visible debris.",
                    "duration": 120,
                },
                {
                    "title": "Apply Bandage",
                    "description": "Cover the wound with a sterile bandage or clean cloth. Secure with tape or wrap.",
                    "duration": 60,
                },
                {
                    "title": "Monitor for Infection",
                    "description": "Watch for signs of infection: increased pain, redness, swelling, or pus. Seek medical attention if needed.",
                    "duration": 0,
                },
            ],
            "burns": [
                {
                    "title": "Cool the Burn",
                    "description": "Hold the burned area under cool (not cold) running water for 10-20 minutes.",
                    "duration": 1200,
                },
                {
                    "title": "Remove Tight Items",
                    "description": "Remove rings, bracelets, or tight clothing from the burned area before it swells.",
                    "duration": 30,
                },
                {
                    "title": "Cover the Burn",
                    "description": "Cover with a sterile, non-adhesive bandage or clean cloth. Do not use ice or butter.",
                    "duration": 60,
                },
                {
                    "title": "Seek Medical Attention",
                    "description": "For severe burns or burns larger than 3 inches, call emergency services immediately.",
                    "duration": 0,
                },
            ],
            "choking": [
                {
                    "title": "Encourage Coughing",
                    "description": "If the person can cough, encourage them to keep coughing to try to clear the blockage.",
                    "duration": 30,
                },
                {
                    "title": "Back Blows",
                    "description": "Stand behind the person, lean them forward, and give 5 sharp back blows between the shoulder blades.",
                    "duration": 30,
                },
                {
                    "title": "Abdominal Thrusts",
                    "description": "Stand behind the person, place hands above navel, and give 5 quick upward thrusts.",
                    "duration": 30,
                },
                {
                    "title": "Call Emergency Services",
                    "description": "If the blockage doesn't clear, call 911 immediately and continue alternating back blows and thrusts.",
                    "duration": 0,
                },
            ],
            "cpr": [
                {
                    "title": "Check Responsiveness",
                    "description": "Tap the person's shoulders and shout 'Are you okay?' Check for normal breathing.",
                    "duration": 10,
                },
                {
                    "title": "Call for Help",
                    "description": "Call 911 immediately. Ask someone to find an AED if available.",
                    "duration": 0,
                },
                {
                    "title": "Position Hands",
                    "description": "Place heel of one hand on center of chest between nipples. Place other hand on top, interlacing fingers.",
                    "duration": 15,
                },
                {
                    "title": "Start Compressions",
                    "description": "Push hard and fast at least 2 inches deep at 100-120 compressions per minute. Let chest recoil completely.",
                    "duration": 120,
                },
            ],
            "sprains": [
                {
                    "title": "Rest the Injury",
                    "description": "Stop activity and rest the injured area. Avoid putting weight on it.",
                    "duration": 0,
                },
                {
                    "title": "Apply Ice",
                    "description": "Apply ice wrapped in a cloth for 15-20 minutes every 2-3 hours for the first 48 hours.",
                    "duration": 1200,
                },
                {
                    "title": "Compress the Area",
                    "description": "Wrap with an elastic bandage, not too tight. You should be able to slip a finger under it.",
                    "duration": 120,
                },
                {
                    "title": "Elevate if Possible",
                    "description": "Raise the injured area above heart level when resting to reduce swelling.",
                    "duration": 0,
                },
            ],
            "nosebleed": [
                {
                    "title": "Sit and Lean Forward",
                    "description": "Sit upright and lean slightly forward to prevent blood from running down the throat.",
                    "duration": 0,
                },
                {
                    "title": "Pinch the Nose",
                    "description": "Pinch the soft part of the nose (not the bridge) firmly for 10-15 minutes continuously.",
                    "duration": 900,
                },
                {
                    "title": "Apply Cold Compress",
                    "description": "Apply a cold compress or ice pack to the bridge of the nose while pinching.",
                    "duration": 900,
                },
                {
                    "title": "Seek Help if Needed",
                    "description": "If bleeding doesn't stop after 20 minutes or if caused by injury, seek medical attention.",
                    "duration": 0,
                },
            ],
            "allergic-reaction": [
                {
                    "title": "Remove the Trigger",
                    "description": "If possible, remove or avoid the allergen that caused the reaction.",
                    "duration": 30,
                },
                {
                    "title": "Use Antihistamine",
                    "description": "Give an antihistamine like Benadryl if available and the person is conscious.",
                    "duration": 60,
                },
                {
                    "title": "Watch for Severe Symptoms",
                    "description": "Monitor for difficulty breathing, swelling of face/throat, or rapid pulse.",
                    "duration": 0,
                },
                {
                    "title": "Call Emergency Services",
                    "description": "If symptoms are severe or person has an EpiPen, use it and call 911 immediately.",
                    "duration": 0,
                },
            ],
            "fainting": [
                {
                    "title": "Lay Person Down",
                    "description": "Help the person lie down on their back. If not possible, help them sit with head between knees.",
                    "duration": 30,
                },
                {
                    "title": "Elevate Legs",
                    "description": "Raise the person's legs 8-12 inches above heart level to improve blood flow to the brain.",
                    "duration": 0,
                },
                {
                    "title": "Loosen Tight Clothing",
                    "description": "Loosen belts, collars, or any tight clothing around the neck and waist.",
                    "duration": 30,
                },
                {
                    "title": "Monitor and Reassure",
                    "description": "Stay with the person, check breathing, and provide reassurance when they regain consciousness.",
                    "duration": 0,
                },
            ],
        }
        
        # Get template or use default
        instructions = templates.get(emergency_type, [
            {
                "title": "Assess the Situation",
                "description": "Carefully assess the situation and ensure your own safety first.",
                "duration": 30,
            },
            {
                "title": "Call for Help",
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

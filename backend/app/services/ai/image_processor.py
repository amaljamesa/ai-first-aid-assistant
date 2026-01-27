"""
LIFELINE AI - Image Processing Service
Image analysis and description generation
"""

import base64
import io
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Process image input and generate descriptions"""
    
    def __init__(self):
        self.ai_enabled = settings.AI_ENABLED
        self.openai_key = settings.OPENAI_API_KEY
        
    async def analyze(
        self,
        image_data: str,
        format: str = "jpeg"
    ) -> str:
        """
        Analyze image and generate description
        
        Args:
            image_data: Base64 encoded image data
            format: Image format (jpg, jpeg, png, webp)
            
        Returns:
            Image description text
        """
        try:
            if self.ai_enabled and self.openai_key:
                return await self._analyze_with_ai(image_data, format)
            else:
                # Fallback: return placeholder
                logger.warning("Image analysis requires AI service. Returning placeholder.")
                return "Image received. Please provide text description of the emergency situation shown in the image."
                
        except Exception as e:
            logger.error(f"Image analysis error: {str(e)}")
            return "Unable to process image. Please provide a text description of the emergency."
    
    async def _analyze_with_ai(
        self,
        image_data: str,
        format: str
    ) -> str:
        """Analyze image using OpenAI Vision API"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Prepare image for API
            image_url = f"data:image/{format};base64,{image_data}"
            
            # Analyze with GPT-4 Vision
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an emergency medical image analysis AI. Analyze images of medical emergencies and describe what you see in detail, focusing on visible injuries, symptoms, or emergency situations."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this emergency medical image. Describe what you see, including any visible injuries, symptoms, or emergency situations. Be specific and detailed."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI image analysis error: {str(e)}")
            raise Exception(f"Image analysis failed: {str(e)}")

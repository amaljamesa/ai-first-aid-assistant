"""
LIFELINE AI - Custom Model Service
Use trained emergency classification model
"""

import joblib
import json
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CustomEmergencyClassifier:
    """Custom trained emergency classifier"""
    
    def __init__(self):
        self.category_model = None
        self.severity_model = None
        self.config = None
        self.load_models()
    
    def load_models(self):
        """Load trained models"""
        try:
            model_dir = os.path.dirname(__file__)
            
            # Load models
            cat_path = os.path.join(model_dir, '../../emergency_category_model.pkl')
            sev_path = os.path.join(model_dir, '../../emergency_severity_model.pkl')
            config_path = os.path.join(model_dir, '../../model_config.json')
            
            if os.path.exists(cat_path) and os.path.exists(sev_path):
                self.category_model = joblib.load(cat_path)
                self.severity_model = joblib.load(sev_path)
                
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        self.config = json.load(f)
                
                logger.info("Custom models loaded successfully")
            else:
                logger.warning("Custom models not found, will use fallback")
                
        except Exception as e:
            logger.error(f"Error loading custom models: {e}")
    
    def is_available(self) -> bool:
        """Check if custom models are available"""
        return self.category_model is not None and self.severity_model is not None
    
    def classify(self, text: str) -> Dict[str, Any]:
        """Classify emergency text"""
        if not self.is_available():
            raise ValueError("Custom models not available")
        
        try:
            # Predict category and severity
            category = self.category_model.predict([text])[0]
            severity = self.severity_model.predict([text])[0]
            
            # Get confidence scores
            cat_proba = self.category_model.predict_proba([text])[0]
            sev_proba = self.severity_model.predict_proba([text])[0]
            
            cat_confidence = max(cat_proba)
            sev_confidence = max(sev_proba)
            overall_confidence = (cat_confidence + sev_confidence) / 2
            
            return {
                "type": category,
                "confidence": float(overall_confidence),
                "severity": severity,
                "severity_confidence": float(sev_confidence),
                "reasoning": f"Custom model classification (confidence: {overall_confidence:.2f})",
                "source": "custom_model"
            }
            
        except Exception as e:
            logger.error(f"Custom model classification error: {e}")
            raise
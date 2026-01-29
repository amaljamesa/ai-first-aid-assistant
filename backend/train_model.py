"""
LIFELINE AI - Simple Emergency Classifier Training
Minimal training setup for emergency classification
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import json

# Minimal training data
training_data = [
    ("I cut my finger with a knife, it's bleeding", "cuts-wounds", "moderate"),
    ("My hand is burned from the stove", "burns", "high"),
    ("Someone is choking on food", "choking", "critical"),
    ("Person collapsed and not breathing", "cpr", "critical"),
    ("Twisted my ankle playing sports", "sprains", "low"),
    ("Nose won't stop bleeding", "nosebleed", "moderate"),
    ("Having allergic reaction, face swelling", "allergic-reaction", "high"),
    ("Feeling dizzy and about to faint", "fainting", "moderate"),
    ("Deep cut on arm, blood everywhere", "cuts-wounds", "high"),
    ("Severe burn from hot oil", "burns", "critical"),
    ("Can't breathe, something stuck in throat", "choking", "critical"),
    ("No pulse, unconscious", "cpr", "critical"),
    ("Sprained wrist, very swollen", "sprains", "moderate"),
    ("Heavy nosebleed after accident", "nosebleed", "high"),
    ("Hives all over body, trouble breathing", "allergic-reaction", "critical"),
    ("Passed out briefly", "fainting", "moderate"),
    ("Small paper cut", "cuts-wounds", "low"),
    ("Minor burn from touching hot pan", "burns", "low"),
    ("Coughing but can still talk", "choking", "low"),
    ("Person is breathing but unconscious", "cpr", "high"),
    ("Mild ankle pain", "sprains", "low"),
    ("Light nosebleed", "nosebleed", "low"),
    ("Mild skin rash", "allergic-reaction", "low"),
    ("Feeling lightheaded", "fainting", "low"),
    # Add more variations
    ("Bleeding wound on leg", "cuts-wounds", "moderate"),
    ("Hot water spilled on skin", "burns", "moderate"),
    ("Food stuck in throat", "choking", "high"),
    ("Heart stopped beating", "cpr", "critical"),
    ("Injured knee from fall", "sprains", "moderate"),
    ("Blood from nose", "nosebleed", "low"),
    ("Swollen face from allergy", "allergic-reaction", "high"),
    ("Lost consciousness", "fainting", "high"),
]

def train_emergency_classifier():
    """Train a simple emergency classifier"""
    
    # Prepare data
    texts = [item[0] for item in training_data]
    categories = [item[1] for item in training_data]
    severities = [item[2] for item in training_data]
    
    # Split data
    X_train, X_test, y_cat_train, y_cat_test, y_sev_train, y_sev_test = train_test_split(
        texts, categories, severities, test_size=0.2, random_state=42
    )
    
    # Train category classifier
    category_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
        ('classifier', MultinomialNB())
    ])
    category_pipeline.fit(X_train, y_cat_train)
    
    # Train severity classifier
    severity_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
        ('classifier', MultinomialNB())
    ])
    severity_pipeline.fit(X_train, y_sev_train)
    
    # Evaluate
    cat_pred = category_pipeline.predict(X_test)
    sev_pred = severity_pipeline.predict(X_test)
    
    print("Category Classification Report:")
    print(classification_report(y_cat_test, cat_pred))
    
    print("\nSeverity Classification Report:")
    print(classification_report(y_sev_test, sev_pred))
    
    # Save models
    joblib.dump(category_pipeline, 'emergency_category_model.pkl')
    joblib.dump(severity_pipeline, 'emergency_severity_model.pkl')
    
    # Save label mappings
    categories_unique = list(set(categories))
    severities_unique = list(set(severities))
    
    with open('model_config.json', 'w') as f:
        json.dump({
            'categories': categories_unique,
            'severities': severities_unique
        }, f)
    
    print("\nModels saved successfully!")
    return category_pipeline, severity_pipeline

def predict_emergency(text, category_model, severity_model):
    """Predict emergency category and severity"""
    category = category_model.predict([text])[0]
    severity = severity_model.predict([text])[0]
    
    # Get confidence scores
    cat_proba = category_model.predict_proba([text])[0]
    sev_proba = severity_model.predict_proba([text])[0]
    
    cat_confidence = max(cat_proba)
    sev_confidence = max(sev_proba)
    
    return {
        'category': category,
        'severity': severity,
        'category_confidence': float(cat_confidence),
        'severity_confidence': float(sev_confidence),
        'overall_confidence': float((cat_confidence + sev_confidence) / 2)
    }

if __name__ == "__main__":
    # Train models
    cat_model, sev_model = train_emergency_classifier()
    
    # Test predictions
    test_cases = [
        "I have a deep cut that won't stop bleeding",
        "Someone is having trouble breathing",
        "Minor scrape on knee"
    ]
    
    print("\nTest Predictions:")
    for test in test_cases:
        result = predict_emergency(test, cat_model, sev_model)
        print(f"Text: {test}")
        print(f"Prediction: {result}")
        print()
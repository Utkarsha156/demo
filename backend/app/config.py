# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # PostgreSQL with pg8000 (pure Python driver)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+pg8000://postgres:password@localhost:5432/ai_storyweaver'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    
    # Using Hugging Face and Stability AI only
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
    STABILITY_AI_API_KEY = os.environ.get('STABILITY_AI_API_KEY')
    
    # Hugging Face models to use (free)
    CHAT_MODEL = "microsoft/DialoGPT-medium"
    STORY_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
    IMAGE_MODEL = "stabilityai/stable-diffusion-2-1"
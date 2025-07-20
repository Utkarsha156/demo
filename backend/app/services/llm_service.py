# backend/app/services/llm_service.py
import requests
import json
from flask import current_app

class HuggingFaceLLMService:
    def __init__(self):
        self.api_key = current_app.config['HUGGINGFACE_API_KEY']
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.chat_model = current_app.config['CHAT_MODEL']
        self.story_model = current_app.config['STORY_MODEL']
    
    def query_model(self, model_name, payload):
        """Generic method to query HuggingFace models"""
        api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        response = requests.post(api_url, headers=self.headers, json=payload)
        return response.json()
    
    def analyze_user_input(self, user_message, conversation_history):
        """Analyze if we need more information for the story"""
        
        # Check what information we have
        required_info = {
            'genre': False,
            'main_character': False,
            'setting': False,
            'plot_idea': False
        }
        
        # Simple keyword detection (you can enhance this)
        text = user_message.lower() + ' ' + ' '.join([msg.get('content', '') for msg in conversation_history])
        
        # Check for genre
        genres = ['adventure', 'mystery', 'romance', 'fantasy', 'horror', 'comedy', 'drama', 'thriller']
        if any(genre in text for genre in genres):
            required_info['genre'] = True
            
        # Check for character mentions
        if any(word in text for word in ['character', 'hero', 'protagonist', 'person', 'boy', 'girl', 'man', 'woman']):
            required_info['main_character'] = True
            
        # Check for setting
        settings = ['village', 'city', 'forest', 'palace', 'mountain', 'river', 'temple', 'school', 'home']
        if any(setting in text for setting in settings):
            required_info['setting'] = True
            
        # Check for plot
        if len(text.split()) > 20:  # If substantial description
            required_info['plot_idea'] = True
        
        return required_info
    
    def generate_follow_up_question(self, missing_info, conversation_history):
        """Generate appropriate follow-up questions"""
        
        questions = {
            'genre': "What genre would you like for your story? (adventure, mystery, fantasy, etc.)",
            'main_character': "Tell me about your main character. Who is the hero of your story?",
            'setting': "Where does your story take place? (a village, palace, forest, modern city, etc.)",
            'plot_idea': "What's the main plot or adventure you'd like to explore in your story?"
        }
        
        # Find first missing piece of information
        for info_type, has_info in missing_info.items():
            if not has_info:
                return questions[info_type]
        
        return None  # All info collected
    
    def generate_story(self, user_input, conversation_history):
        """Generate 10-paragraph Indian themed story"""
        
        # Combine all conversation context
        full_context = f"User's story idea: {user_input}\n"
        for msg in conversation_history:
            full_context += f"{msg['role']}: {msg['content']}\n"
        
        story_prompt = f"""
        Based on the following context, write a captivating 10-paragraph story with Indian cultural elements:
        
        {full_context}
        
        Requirements:
        - Exactly 10 paragraphs
        - Include Indian cultural elements (names, places, traditions, festivals, etc.)
        - Rich descriptions of Indian landscapes, architecture, or cultural practices
        - Each paragraph should be 3-4 sentences long
        - Make it engaging and family-friendly
        
        Story:
        """
        
        payload = {
            "inputs": story_prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        try:
            response = self.query_model(self.story_model, payload)
            
            if isinstance(response, list) and len(response) > 0:
                generated_text = response[0].get('generated_text', '')
                # Extract story content after the prompt
                story_start = generated_text.find("Story:")
                if story_start != -1:
                    story_content = generated_text[story_start + 6:].strip()
                else:
                    story_content = generated_text.strip()
                
                # Split into paragraphs
                paragraphs = [p.strip() for p in story_content.split('\n\n') if p.strip()]
                
                # Ensure we have exactly 10 paragraphs
                if len(paragraphs) < 10:
                    # Pad with additional content if needed
                    while len(paragraphs) < 10:
                        paragraphs.append(f"The story continues with more adventures in the beautiful land of India...")
                elif len(paragraphs) > 10:
                    paragraphs = paragraphs[:10]
                
                return paragraphs
            else:
                # Fallback story
                return self.generate_fallback_story()
                
        except Exception as e:
            print(f"Error generating story: {e}")
            return self.generate_fallback_story()
    
    def generate_fallback_story(self):
        """Fallback story in case of API issues"""
        return [
            "In a vibrant village nestled in the foothills of the Himalayas, lived a curious young girl named Priya. She had always been fascinated by the ancient stories her grandmother told her about magical adventures.",
            "One morning, while helping her mother in their spice garden, Priya discovered an unusual brass lamp buried beneath the tulsi plant. The lamp gleamed with an otherworldly shine despite being covered in earth.",
            "As she cleaned the lamp, a gentle voice emerged from within, speaking in melodious Sanskrit. The voice belonged to a kind spirit who had been waiting centuries for someone pure of heart to find the lamp.",
            "The spirit, named Vayu, offered to grant Priya one special journey to anywhere in India she wished to visit. Without hesitation, she asked to see the most beautiful temple in all the land.",
            "In a swirl of marigold petals and sandalwood fragrance, Priya found herself standing before the magnificent Golden Temple in Amritsar. The temple's reflection shimmered in the sacred waters of the sarovar.",
            "There, she met a wise old sage who taught her about the importance of seva, selfless service. Priya spent the day helping in the community kitchen, serving food to pilgrims from across the world.",
            "As the sun began to set, painting the sky in shades of saffron and rose, the sage gave Priya a small lotus seed. He told her it would grow into something beautiful if she planted it with love and care.",
            "Vayu appeared once more and transported Priya back to her village, where she immediately planted the lotus seed in the pond near her home. She watered it daily and sang to it the prayers she had learned.",
            "Months passed, and the lotus bloomed into the most magnificent flower the village had ever seen. Its fragrance attracted butterflies and brought peace to all who visited the pond.",
            "Priya realized that the greatest magic was not in the brass lamp or the mystical journey, but in the kindness and service she had learned to carry in her heart every day."
        ]
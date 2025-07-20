# backend/app/models/story.py
from app import db
from datetime import datetime
import json

class Story(db.Model):
    __tablename__ = 'stories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255))
    user_input = db.Column(db.Text, nullable=False)
    conversation_history = db.Column(db.JSON)
    country_theme = db.Column(db.String(100), default='Indian')
    status = db.Column(db.String(50), default='in_progress')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    pages = db.relationship('StoryPage', backref='story', lazy=True, cascade='all, delete-orphan')
    
    def set_conversation_history(self, history_list):
        """Store conversation as JSON"""
        self.conversation_history = json.dumps(history_list)
    
    def get_conversation_history(self):
        """Get conversation as Python list"""
        if self.conversation_history:
            return json.loads(self.conversation_history)
        return []
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'user_input': self.user_input,
            'country_theme': self.country_theme,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'pages_count': len(self.pages)
        }
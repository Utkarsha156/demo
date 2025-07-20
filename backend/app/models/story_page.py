# backend/app/models/story_page.py
from app import db
from datetime import datetime

class StoryPage(db.Model):
    __tablename__ = 'story_pages'
    
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    image_prompt = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('story_id', 'page_number', name='unique_story_page'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'page_number': self.page_number,
            'content': self.content,
            'image_url': self.image_url,
            'image_prompt': self.image_prompt,
            'created_at': self.created_at.isoformat()
        }
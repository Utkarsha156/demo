# backend/app/models/user.py
from app import db
from datetime import datetime
from passlib.hash import pbkdf2_sha256

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    stories = db.relationship('Story', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash password using passlib (no C++ compilation needed)"""
        self.password_hash = pbkdf2_sha256.hash(password)
    
    def check_password(self, password):
        """Verify password using passlib"""
        return pbkdf2_sha256.verify(password, self.password_hash)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
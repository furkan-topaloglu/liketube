from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Kullanıcı modeli"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))
    token = db.Column(db.Text)  # Encrypted token
    refresh_token = db.Column(db.Text)  # Encrypted refresh token
    token_uri = db.Column(db.String(500))
    client_id = db.Column(db.String(500))
    client_secret = db.Column(db.String(500))
    last_sync = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    videos = db.relationship('Video', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


class Video(db.Model):
    """Video modeli"""
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    video_id = db.Column(db.String(255), nullable=False, index=True)
    title = db.Column(db.String(500), nullable=False)
    channel = db.Column(db.String(255), nullable=False)
    channel_id = db.Column(db.String(255))
    description = db.Column(db.Text)
    thumbnail = db.Column(db.String(500))
    published_at = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    duration = db.Column(db.String(50))
    url = db.Column(db.String(500))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Filtreleme için index
    __table_args__ = (
        db.Index('idx_user_video', 'user_id', 'video_id'),
    )
    
    def to_dict(self):
        """Video objesini dictionary'ye çevir"""
        from utils import parse_duration
        
        duration_seconds = parse_duration(self.duration) if self.duration else 0
        
        return {
            'id': self.video_id,
            'title': self.title,
            'channel': self.channel,
            'channelId': self.channel_id,
            'description': self.description[:200] + '...' if self.description and len(self.description) > 200 else (self.description or ''),
            'thumbnail': self.thumbnail,
            'publishedAt': self.published_at.isoformat() if self.published_at else None,
            'viewCount': self.view_count,
            'likeCount': self.like_count,
            'duration': self.duration,
            'durationSeconds': duration_seconds,
            'url': self.url,
            'addedAt': self.added_at.isoformat() if self.added_at else None
        }
    
    def __repr__(self):
        return f'<Video {self.video_id} - {self.title[:50]}>'


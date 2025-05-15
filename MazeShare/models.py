from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # ... (추가 필드)

class Maze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    data = db.Column(db.JSON, nullable=False)  # 미로 데이터 (2D 배열)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # ... (추가 필드)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    maze_id = db.Column(db.Integer, db.ForeignKey('maze.id'))
    # ... (추가 필드)

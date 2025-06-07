from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

# 즐겨찾기 Many-to-Many 관계 테이블
bookmarks = db.Table('bookmarks',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('maze_id', db.Integer, db.ForeignKey('maze.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    mazes = db.relationship('Maze', backref='author', lazy=True)
    bookmarked_mazes = db.relationship('Maze', secondary=bookmarks, backref='bookmarked_by', lazy='dynamic')  # 추가

class Maze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    data = db.Column(db.JSON, nullable=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start = db.Column(db.JSON)
    end = db.Column(db.JSON)
    image_path = db.Column(db.String(200))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    maze_id = db.Column(db.Integer, db.ForeignKey('maze.id'), nullable=False)
    user = db.relationship('User', backref='reviews')
    maze = db.relationship('Maze', backref='reviews')

class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maze_id = db.Column(db.Integer, db.ForeignKey('maze.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_seconds = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    maze = db.relationship('Maze', backref='rankings')
    user = db.relationship('User', backref='rankings')

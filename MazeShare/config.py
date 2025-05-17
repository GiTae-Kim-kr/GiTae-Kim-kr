import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'maze_share.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

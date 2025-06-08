from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Maze, User, Review, bookmarks
from bp import maze_bp, auth_bp
from flask_login import LoginManager, current_user
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    sort_type = request.args.get('sort', '')
    filter_type = request.args.get('filter', '')
    per_page = 6

    mazes_query = Maze.query.join(User).filter(Maze.is_published == True)

    if query:
        mazes_query = mazes_query.filter(
            (Maze.title.ilike(f'%{query}%')) |
            (User.username.ilike(f'%{query}%'))
        )

    if filter_type == 'bookmarks' and current_user.is_authenticated:
        mazes_query = mazes_query.join(bookmarks, Maze.id == bookmarks.c.maze_id)\
                                 .filter(bookmarks.c.user_id == current_user.id)
    elif filter_type == 'my' and current_user.is_authenticated:
        mazes_query = mazes_query.filter(Maze.user_id == current_user.id)

    if sort_type == 'rating':
        mazes_query = mazes_query.outerjoin(Maze.reviews)\
            .group_by(Maze.id)\
            .order_by(func.coalesce(func.avg(Review.rating), 0).desc())
    else:
        mazes_query = mazes_query.order_by(Maze.created_at.desc())

    mazes = mazes_query.paginate(page=page, per_page=per_page)

    return render_template('index.html',
                         mazes=mazes,
                         query=query,
                         sort=sort_type,
                         filter=filter_type)

app.register_blueprint(maze_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)

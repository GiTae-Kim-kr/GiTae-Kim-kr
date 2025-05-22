from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Maze, User
from bp import maze_bp, auth_bp
from flask_login import LoginManager, current_user

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
    query = request.args.get('q', '')  # 검색어 파라미터 추가
    page = request.args.get('page', 1, type=int)
    per_page = 6

    if query:
        # 검색 쿼리가 있는 경우
        mazes = Maze.query.join(User)\
            .filter(
                (Maze.title.ilike(f'%{query}%')) |
                (User.username.ilike(f'%{query}%'))
            )\
            .filter(Maze.is_published == True)\
            .order_by(Maze.created_at.desc())\
            .paginate(page=page, per_page=per_page)
    else:
        # 일반 조회
        mazes = Maze.query.filter_by(is_published=True)\
            .order_by(Maze.created_at.desc())\
            .paginate(page=page, per_page=per_page)

    return render_template('index.html', mazes=mazes, query=query)


app.register_blueprint(maze_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)

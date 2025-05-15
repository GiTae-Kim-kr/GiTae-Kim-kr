from flask import Flask, render_template
from config import Config
from models import db, Maze  # Maze 모델도 import 필요!
from bp import maze_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    mazes = Maze.query.order_by(Maze.created_at.desc()).all()
    return render_template('index.html', mazes=mazes)

# Blueprint 등록
app.register_blueprint(maze_bp)

if __name__ == "__main__":
    app.run(debug=True)

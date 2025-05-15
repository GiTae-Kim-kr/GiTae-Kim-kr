from flask import Blueprint, render_template

maze_bp = Blueprint('maze', __name__)

@maze_bp.route('/create_maze')
def create_maze():
    return render_template('create_maze.html')

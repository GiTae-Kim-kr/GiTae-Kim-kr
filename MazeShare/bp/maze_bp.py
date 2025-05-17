from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from flask_login import login_required, current_user
from models import db, Maze


maze_bp = Blueprint('maze', __name__)

@maze_bp.route('/create_maze')
def create_maze():
    return render_template('create_maze.html')

@maze_bp.route('/save_maze', methods=['POST'])
@login_required
def save_maze():
    try:
        new_maze = Maze(
            title=request.form['title'],
            description=request.form['description'],
            data=request.form['maze_data'],
            start=request.form['start'],
            end=request.form['end'],
            is_published=request.form.get('is_published') == '1',
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_maze)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

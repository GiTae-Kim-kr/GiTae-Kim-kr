from flask import Blueprint, render_template, request, jsonify, current_app, redirect, json, flash
from datetime import datetime
from flask_login import login_required, current_user
from models import db, Maze, Review, User, Ranking
import base64
import os

maze_bp = Blueprint('maze', __name__)

@maze_bp.route('/create_maze')
def create_maze():
    return render_template('create_maze.html')

@maze_bp.route('/save_maze', methods=['POST'])
@login_required
def save_maze():
    try:
        maze_image_data = request.form['maze_image']
        header, encoded = maze_image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)

        maze_data = json.loads(request.form['maze_data'])
        start_pos = json.loads(request.form['start'])
        end_pos = json.loads(request.form['end'])

        new_maze = Maze(
            title=request.form['title'],
            description=request.form['description'],
            data=maze_data,
            start=start_pos,
            end=end_pos,
            is_published=request.form.get('is_published') == '1',
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_maze)
        db.session.commit()

        static_folder = current_app.static_folder
        img_dir = os.path.join(static_folder, 'mazes')
        os.makedirs(img_dir, exist_ok=True)
        img_filename = f'maze_{new_maze.id}.png'
        img_full_path = os.path.join(img_dir, img_filename)

        with open(img_full_path, 'wb') as f:
            f.write(image_bytes)

        new_maze.image_path = f'mazes/{img_filename}'
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@maze_bp.route('/submit_review/<int:maze_id>', methods=['POST'])
@login_required
def submit_review(maze_id):
    content = request.form.get('review')
    new_review = Review(
        content=content,
        user_id=current_user.id,
        maze_id=maze_id
    )
    db.session.add(new_review)
    db.session.commit()
    flash("리뷰가 등록되었습니다.", "success")
    return redirect(request.referrer)

@maze_bp.route('/maze_reviews/<int:maze_id>')
def maze_reviews(maze_id):
    reviews = Review.query.filter_by(maze_id=maze_id).order_by(Review.created_at.desc()).all()
    review_list = [
        {
            "username": review.user.username,
            "content": review.content,
            "created_at": review.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for review in reviews
    ]
    return jsonify(review_list)

@maze_bp.route('/play_maze/<int:maze_id>')
def play_maze(maze_id):
    maze = Maze.query.get_or_404(maze_id)
    return render_template('play_maze.html',
        maze=maze,
        maze_data=maze.data,
        start_pos=maze.start,
        end_pos=maze.end
    )

@maze_bp.route('/maze_reviews/<int:maze_id>/rankings')
def maze_rankings(maze_id):
    rankings = Ranking.query.filter_by(maze_id=maze_id) \
        .join(User) \
        .with_entities(
        User.username,
        Ranking.time_seconds
    ) \
        .order_by(Ranking.time_seconds.asc()) \
        .limit(10) \
        .all()

    return jsonify([
        {"username": r.username, "time_seconds": r.time_seconds}
        for r in rankings
    ])

# 랭킹 기록 저장 라우트 추가 (로그인 필요)
@maze_bp.route('/submit_time/<int:maze_id>', methods=['POST'])
@login_required
def submit_time(maze_id):
    data = request.get_json()
    time_seconds = data.get('time')
    if time_seconds is None:
        return jsonify({'success': False, 'message': '시간 정보가 없습니다.'}), 400
    new_ranking = Ranking(
        maze_id=maze_id,
        user_id=current_user.id,
        time_seconds=time_seconds
    )
    db.session.add(new_ranking)
    db.session.commit()
    return jsonify({'success': True})


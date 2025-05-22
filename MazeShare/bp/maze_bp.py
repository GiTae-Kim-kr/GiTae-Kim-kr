from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from flask_login import login_required, current_user
from models import db, Maze
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
        # 이미지 데이터 처리
        maze_image_data = request.form['maze_image']
        header, encoded = maze_image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)

        # 미로 데이터 먼저 저장 (ID 생성 위해)
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

        # 이미지 저장 경로 설정
        static_folder = current_app.static_folder  # Flask의 static 폴더 경로
        img_dir = os.path.join(static_folder, 'mazes')
        os.makedirs(img_dir, exist_ok=True)  # 디렉토리 없으면 생성

        # 파일 저장
        img_filename = f'maze_{new_maze.id}.png'
        img_full_path = os.path.join(img_dir, img_filename)

        with open(img_full_path, 'wb') as f:
            f.write(image_bytes)

        # DB에 상대 경로 저장 (static/ 제외)
        new_maze.image_path = f'mazes/{img_filename}'
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({'success': False, 'message': str(e)})


# bp/auth_bp.py
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        flash("로그인 성공!", "success")
    else:
        flash("아이디 또는 비밀번호가 올바르지 않습니다.", "danger")
    return redirect(url_for("index"))

@auth_bp.route('/signup', methods=['POST'])
def signup():
    username = request.form.get("username")
    password = generate_password_hash(request.form.get("password"))
    email = request.form.get("email")
    phone = request.form.get("phone")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("이미 존재하는 아이디입니다.", "danger")
        return redirect(url_for("index"))

    new_user = User( # noinspection PyArgumentList
        username=username,
        password=password,
        email=email,
        phone=phone
    )
    db.session.add(new_user)
    db.session.commit()

    flash("회원가입이 완료되었습니다. 로그인해주세요.", "success")
    return redirect(url_for("index"))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("로그아웃되었습니다.", "info")
    return redirect(url_for("index"))

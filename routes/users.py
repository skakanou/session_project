from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import re

user_bp = Blueprint('users', __name__)

def is_strong_pwd(pwd):
    if not pwd:
        return False
    
    return (
        len(pwd) >= 12 and
        re.search(r"[A-Z]", pwd) and
        re.search(r"[0-9]", pwd) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd)
    )

@user_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    if not is_strong_pwd(password):
        return render_template ('index.html', 
                               error="Mot de passe trop faible. Il doit comporter au moins 12 caractères, inclure une majuscule, un chiffre et un caractère spécial.")   
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return render_template('index.html', error="Nom d'utilisateur ou email déjà utilisé.")

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, 
                    email=email, 
                    password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return render_template('index.html', success="Inscription réussie ! Vous pouvez maintenant vous connecter.")

@user_bp.route('/login', methods=['POST'])


def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return render_template('index.html', error="Nom d'utilisateur ou mot de passe incorrect.")
    
    return redirect(url_for('users.user_dashboard'))
    
@user_bp.route('/user_dashboard')

def user_dashboard():
    return render_template('user_dash.html')
from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import Event, db, User
import re

#------------------------------------------------register-----------------------------------------------------

user_bp = Blueprint('users', __name__)

def is_strong_pwd(pwd):
    if not pwd:
        return False

    pwd = pwd.strip()

    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{12,}$"
    return bool(re.fullmatch(pattern, pwd))

@user_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        return render_template('index.html', error="Les mots de passe ne correspondent pas.")

    if not is_strong_pwd(password):
        return render_template ('index.html', 
                               error="Le mot de passe ne respecte pas les critères de sécurité : au moins 12 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.") 
      
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

#-----------------------------------------------------login-----------------------------------------------------

def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return render_template('index.html', error="Nom d'utilisateur ou mot de passe incorrect.")
    
    session['user_id'] = user.id
    session['username'] = user.username
    session['role'] = user.role
    
    if user.role == "admin":
        return render_template('admin_dash.html') # Redirige vers le tableau de bord admin

    else :
        return redirect(url_for('users.events')) # Redirige vers la page des événements

#-----------------------------------------------------logout-----------------------------------------------------
@user_bp.route('/logout')
def logout():
    session.clear()
    return render_template('index.html', success="You have been logged out successfully.")

#-----------------------------------------------------events & user dash-----------------------------------------------------
@user_bp.route('/events')
def events():
    if 'user_id' not in session:
        return redirect(url_for('users.login_page')) # Redirige vers la page de connexion si l'utilisateur n'est pas connecté
    
    events = Event.query.all() #Pour recuperer tous les événements de la base de données
    return render_template('events.html', events=events) # Rendu du template events
    

@user_bp.route('/user_dash')
def user_dash():
    if 'user_id' not in session:
        return redirect(url_for('users.login_page')) # Redirige vers la page de connexion si l'utilisateur n'est pas connecté
    return render_template('user_dash.html')

@user_bp.route('/login')
def login_page():
    return render_template('index.html')

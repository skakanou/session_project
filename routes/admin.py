from flask import Blueprint, render_template, request, session, redirect, url_for
from models import Event, db
from datetime import datetime


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_dash')
def admin_dash():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('users.login_page')) # Redirige vers la page de connexion si l'utilisateur n'est pas connecté ou n'est pas admin
    
    events = Event.query.all() #Pour recuperer tous les événements de la base de données
    return render_template('admin_dash.html', events=events) # Rendu du template admin

#-----------------------------------------------------create event-----------------------------------------------------

@admin_bp.route('/create_event', methods=['GET', 'POST'])
def create_event():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('users.login_page'))

    if request.method == 'POST':

        event_name = request.form.get('event_name')
        event_date = request.form.get('event_date')
        location = request.form.get('location')
        category = request.form.get('category')
        seats_available = request.form.get('seats_available')
        description = request.form.get('description')

        event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
        seats_available = int(seats_available)

        new_event = Event(
            event_name=event_name,
            event_date=event_date,
            location=location,
            category=category,
            seats_available=seats_available,
            description=description
        )

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('admin.admin_dash'))

    return render_template('create_event.html')
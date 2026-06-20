from models import Reservation, Event, db
from flask import Blueprint, request, redirect, url_for, flash, session
from routes.users import user_bp

reservation_bp = Blueprint('reservation', __name__)
@reservation_bp.route('/reserve/<int:event_id>', methods=['POST'])

def reserve(event_id):
    if 'user_id' not in session:
        return redirect(url_for('users.login_page'))

    event = Event.query.get_or_404(event_id)
    
    if event.seats_available <= 0:
        return "Sold out", 400
    
    reservation = Reservation(user_id=session['user_id'], event_id=event_id)

    event.seats_available -= 1

    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('users.user_dash'))
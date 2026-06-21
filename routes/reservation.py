from models import Booking, Event, db
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.users import user_bp
from datetime import date, datetime

reservation_bp = Blueprint('reservation', __name__)
@reservation_bp.route('/make_reservation/<int:event_id>', methods=['POST'])

#-----------------------------------------------------make reservation-----------------------------------------------------

def make_reservation(event_id):
    if 'user_id' not in session:
        return redirect(url_for('users.login_page'))

    event = Event.query.get_or_404(event_id)
    quantity = int(request.form.get('quantity', 1))
    
    if event.seats_available <= 0:
        return "Sold out", 400
    
    if event.seats_available < 0:
        return "Invalid event state", 400
    
    if event.seats_available < quantity:
        return "Not enough seats available", 400
    
    reservation = Booking.query.filter_by(
        user_id=session['user_id'], 
        event_id=event_id, 
        state='Confirmed'
        ).first()
    
    if reservation:
        reservation.quantity += quantity
    else:
        reservation = Booking(
            user_id=session['user_id'], 
            event_id=event_id,
            booking_date=date.today(),
            quantity=quantity
            )
        db.session.add(reservation)

    event.seats_available -= quantity

    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('users.user_dash'))

#-----------------------------------------------------cancel reservation-----------------------------------------------------
@reservation_bp.route('/cancel_reservation/<int:booking_id>', methods=['POST'])
def cancel_reservation(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('users.login_page'))

    reservation = Booking.query.get_or_404(booking_id)

    if reservation.user_id != session['user_id']:
        return "Unauthorized", 403
    
    if reservation.state == 'cancelled':
        return redirect(url_for('users.user_dash'))
    
    reservation.state = 'cancelled'
    reservation.event.seats_available += reservation.quantity

    db.session.commit()

    return redirect(url_for('users.user_dash'))
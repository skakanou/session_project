from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User(
        username="admin",
        email="exemple@exemple.com",
        password=generate_password_hash("Administrateur@123"),
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()
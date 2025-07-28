from app import app
from models import db, Message

with app.app_context():
    db.drop_all()
    db.create_all()

    msg1 = Message(username="Duane", body="Hello, world!")
    msg2 = Message(username="Ethan", body="What's up?")
    
    db.session.add_all([msg1, msg2])
    db.session.commit()

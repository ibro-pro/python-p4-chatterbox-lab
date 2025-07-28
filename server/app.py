from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
from flask_cors import CORS
CORS(app)

CORS(app)

@app.route('/')
def index():
    return {'message': 'Chatterbox API'}

# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages])

# POST a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_msg = Message(body=data['body'], username=data['username'])
    db.session.add(new_msg)
    db.session.commit()
    return make_response(jsonify(new_msg.to_dict()), 201)

# PATCH a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    message.body = data.get('body', message.body)
    db.session.commit()
    return jsonify(message.to_dict())

# DELETE a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return make_response('', 204)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

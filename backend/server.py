from Chatbot import *


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_data.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
chatbot = Chatbot('tushar5955/portfolioGPT')

# Define your database model
class ChatEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.String(50))
    bot = db.Column(db.String(50))

    def __repr__(self):
        return f"<ChatEntry {self.id}>"

# Create the SQLite database and table if they don't exist
with app.app_context():
    db.create_all()

# Your existing route for processing JSON and replying
@app.route('/reply', methods=['POST'])
def process_json():
    try:
        data = request.get_json()  # Parse the JSON data from the request
        message = data['message']
        response = chatbot.reply(message)

        # Store the conversation entry in the database
        entry = ChatEntry(user=message, bot=response)  # Update user and bot data accordingly
        db.session.add(entry)
        db.session.commit()

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Run the Flask app in debug mode

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import re

app = Flask(__name__)

# Use environment variables for security
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'mysql+pymysql://root:rootpassword@db:3306/waitlist_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    signup_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Waitlist {self.email}>'

# Create tables
with app.app_context():
    db.create_all()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/')
def home():
    with open('index.html') as f:
        return f.read()

@app.route('/submit', methods=['POST'])
def submit():
    try:
        email = request.form.get('email', '').strip().lower()
        
        # Validate email
        if not email or not is_valid_email(email):
            return jsonify({'success': False, 'message': 'Invalid email address'}), 400
        
        # Check if email already exists
        existing = Waitlist.query.filter_by(email=email).first()
        if existing:
            return jsonify({'success': False, 'message': 'Email already registered!'}), 409
        
        # Add to database
        new_entry = Waitlist(email=email)
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Successfully joined the waitlist!'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Something went wrong. Please try again.'}), 500

# Optional: Admin endpoint to view all emails
@app.route('/admin/emails')
def admin_emails():
    emails = Waitlist.query.all()
    return jsonify([{'email': e.email, 'date': e.signup_date} for e in emails])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


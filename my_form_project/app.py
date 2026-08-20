import re
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure local SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Schema
class UserSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    birthmark = db.Column(db.Text, nullable=False)
    dob = db.Column(db.String(10), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_name = request.form.get('name', '')
        user_email = request.form.get('email', '')
        user_phone = request.form.get('phone', '')
        user_address = request.form.get('address', '')
        user_birthmark = request.form.get('birthmark')
        user_dob = request.form.get('dob', '')

        # STRICT VALIDATION: Phone number must contain ONLY digits 0-9
        if not user_phone or not re.match(r'^\d+$', user_phone):
            return "Error: Phone number must contain digits only! No spaces or characters allowed.", 400

        
        new_entry = UserSubmission(
            name=user_name,
            email=user_email,
            phone=user_phone,
            address=user_address,
            birthmark=user_birthmark,
            dob=user_dob
        )
        db.session.add(new_entry)
        db.session.commit()

        return "Data submitted successfully!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
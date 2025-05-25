import os
from flask import Flask, render_template, request, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from sqlalchemy.dialects.mysql import LONGBLOB

app = Flask(__name__)

# Secret key for sessions, flash messages
app.secret_key = os.getenv('SECRET_KEY', 'key123')

# Use environment variable DATABASE_URL for DB connection (set this in Render or locally)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+mysqlconnector://root:root@localhost/portfolio'  # fallback for local testing
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Contact Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

# Define Resume model for storing PDF as blob
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    content_type = db.Column(db.String(100))
    data = db.Column(LONGBLOB)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_msg = Message(email=email, name=name, message=message)
        db.session.add(new_msg)
        db.session.commit()
        print(f"Message received from {name} ({email}): {message}")
        return render_template('contact.html', success=True)
    return render_template('contact.html', success=False)

@app.route('/download_resume/<int:resume_id>')
def download_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    return send_file(BytesIO(resume.data),
                     download_name=resume.filename,
                     mimetype=resume.content_type,
                     as_attachment=True)

# Insert resume PDF into DB only if not exists
def insert_resume():
    # Relative path to PDF inside your project directory, adjust if needed
    resume_path = os.path.join(os.path.dirname(__file__), 'static', 'Dhanunjay_T_Resume.pdf')

    print("Checking if resume already exists...")
    existing = Resume.query.first()
    if existing:
        print("Resume already exists in the database.")
        return

    if not os.path.exists(resume_path):
        print("🚫 Resume file not found at:", resume_path)
        return

    try:
        with open(resume_path, 'rb') as f:
            new_resume = Resume(
                filename='Dhanunjay_Tippana_Resume.pdf',
                content_type='application/pdf',
                data=f.read()
            )
            db.session.add(new_resume)
            db.session.commit()
            print("✅ Resume inserted successfully.")
    except Exception as e:
        print("❌ Error inserting resume:", e)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        insert_resume()
    app.run()

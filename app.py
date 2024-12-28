from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Limiter with a global limit
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"],  # Global limit for all routes
)

# Configure Talisman for security headers (including CSP)
Talisman(app)

# Task model
class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = TODO(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            logging.info(f"Task '{task_content}' added successfully")
            return redirect('/')
        except Exception as e:
            logging.error(f"Error adding task: {e}")
            return f"Error Adding Task: {e}"
    else:
        tasks = TODO.query.order_by(TODO.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/Contact/')
def contact():
    return render_template('contact.html')

@app.route('/Login/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = User.query.filter((User.username == username)).first()
        if existing_user:
            return 'User already exists!'

        if password != confirm_password:
            return 'Passwords do not match'

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            logging.info(f"User '{username}' registered successfully")
            return redirect('/')
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return f"Error: {e}"

    return render_template('login.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TODO.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        logging.info(f"Task with ID {id} deleted successfully")
        return redirect('/')
    except Exception as e:
        logging.error(f"Error deleting task with ID {id}: {e}")
        return f'Error Deleting Task: {e}'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = TODO.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            logging.info(f"Task with ID {id} updated successfully")
            return redirect('/')
        except Exception as e:
            logging.error(f"Error updating task with ID {id}: {e}")
            return f'Error Updating Task: {e}'

    return render_template('update.html', task=task)

if __name__ == "__main__":
    # Run the app with SSL context (self-signed certificate)
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True, port=5367)
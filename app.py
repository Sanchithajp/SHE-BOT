from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Needed for flash messages
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords

# Create the database tables
with app.app_context():
    db.create_all()

# Route for login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user and bcrypt.check_password_hash(existing_user.password, password):
        return f"Welcome back, {email}!"
    else:
        flash("Invalid email or password!", "danger")
        return redirect(url_for('login_page'))

# Route for signup page
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Route to handle signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists! Please log in.", "warning")
        return redirect(url_for('login_page'))
    
    # Hash password before storing
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("Signup successful! Please log in.", "success")
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''# link to database
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User_details(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(10))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password



@app.route('/')
def reg():
    return render_template('reg.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', message="Please enter both email and password.")
        
        user = User_details.query.filter(User_details.email == email).first()
        
        if user and user.password == password:
            session['user_id'] = user.id  # Save user ID in the session
            return redirect(url_for('home'))  # Redirect to home on successful login
            
        else:
            return render_template('login.html', message="Invalid credentials. Please try again.")
    
    return render_template('login.html')  # GET request to show login form

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name or not email or not password:
            return render_template('reg.html', message='Please enter all required fields.')

        if db.session.query(User_details).filter(User_details.email == email).count() == 0:
            user = User_details(name=name, email=email, password=password)
            db.session.add(user)

            db.session.commit()
            return redirect(url_for('login'))  # Redirect to login page after successful registration
        else:
            return render_template('reg.html', message='Email already registered.')
    
    return render_template('reg.html')  # GET request to show registration form


    #logout 
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they do not exist
    app.run()

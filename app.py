from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback

from forms import RegisterForm, LoginForm
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
def home_page():
    """Home page."""
    return redirect('/register')

@app.route('/register')
def register_page():
    """Register page where user can sign up new account."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()

        session['username'] = user.username

        return redirect(f"users/{user.username}")
    
    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    """Login page that allows existing user sign in."""

    if "username" in session:
        return redirect(f"users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form) 
        
    return render_template("users/login.html", form=form)
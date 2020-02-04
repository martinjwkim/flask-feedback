from flask import Flask, redirect, render_template, flash, session

from models import db, connect_db, User
from forms import UserForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'its a big secret'

connect_db(app)
db.create_all()

@app.route("/")
def root():
    """Homepage: redirect to /register."""

    return redirect("/register")


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = UserForm()
    
    if form.validate_on_submit():
        breakpoint()
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        data["email"] = data["email"] or None
        new_user = User.create_user(data)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash("You did it", 'good')
        return redirect('/secret')

    return render_template('userform.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user = User.authenicate(**data)
        if user:
            session['username']= user.username
            return redirect('/secret')
        flash("Invalid Credentials", 'bad')
    return render_template('userform.html', form=form)

@app.route('/secret')
def secret():

    if session.get('username'):
        return "You made it!"
    flash('Nice Try Idiot', 'bad')
    return redirect('/')
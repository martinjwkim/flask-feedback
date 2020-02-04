from flask import Flask, redirect, request, render_template, flash, session
from flask_mail import Mail, Message
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm


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
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        data["email"] = data["email"] or None
        new_user = User.create_user(data)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash("You did it", 'good')
        return redirect(f'/users/{new_user.username}')

    return render_template('form.html', form=form, action='Register', subject='User')


@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user = User.authenicate(**data)
        if user:
            session['username']= user.username
            return redirect(f'/users/{user.username}')
        flash("Invalid Credentials", 'bad')
    return render_template('form.html', form=form, action='Login', subject='User')


@app.route('/users/<username>')
def user_home(username):
    if session.get('username') != username:
        flash('Nice Try Idiot', 'bad')
        return redirect('/')

    user = User.query.filter_by(username=username).first()

    return render_template('user_details.html', user=user)


@app.route('/logout')
def logout():
    session.pop('username')

    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if session.get('username') != username:
        flash('Nice Try Idiot', 'bad')
        return redirect('/')

    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    flash('Your account has been deleted.', 'good')

    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    if session.get('username') != username:
        flash('Nice Try Idiot', 'bad')
        return redirect('/')

    form = FeedbackForm()
    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        title = form.data['title']
        content = form.data['content']
        new_feedback = Feedback(title=title, content=content, user_id=user.id)

        db.session.add(new_feedback)
        db.session.commit()

        flash('Feedback added.', 'good')

        return redirect(f'/users/{username}')

    return render_template('form.html', form=form, action='Add', subject='Feedback')


@app.route('/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if session.get('username') != feedback.user.username:
        flash('Nice Try Idiot', 'bad')
        return redirect('/')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.data['title']
        feedback.content = form.data['content']

        db.session.commit()

        flash('Feedback updated.', 'good')

        return redirect(f'/users/{feedback.user.username}')

    return render_template('form.html', form=form, action='Update', subject='Feedback')


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if session.get('username') != feedback.user.username:
        flash('Nice Try Idiot', 'bad')
        return redirect('/')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.user.username}')





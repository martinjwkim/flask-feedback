from wtforms import StringField, PasswordField, TextField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Email, Length

BOOTS_CLASS = {"class": "form-control"}

class UserForm(FlaskForm):
    """Form for adding playlists."""

    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=20)], render_kw=BOOTS_CLASS
    )

    password = PasswordField(
        "Password", validators=[InputRequired()]
    )

    email = StringField(
        "Email", validators=[Optional(), Email(), Length(min=1, max=50)]
    )

    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(min=1, max=30)]
    )

    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(min=1, max=30)]
    )


class LoginForm(FlaskForm):
    """Form for logging in"""

    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=20)]
    )

    password = PasswordField(
        "Password", validators=[InputRequired()]
    )


class FeedbackForm(FlaskForm):
    """Form for feedback"""

    title = StringField(
        "Title", validators=[InputRequired(), Length(min=1, max=100)]
    )

    content = TextField('Content', validators=[InputRequired()])
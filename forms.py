from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Email, Length


class UserForm(FlaskForm):
    """Form for adding playlists."""

    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=20)]
    )

    password = PasswordField(
        "Password", validators=[InputRequired()]
    )

    email = StringField(
        "Email", validators=[Optional(), Email, Length(min=1, max=50)]
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

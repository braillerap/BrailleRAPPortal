from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class RegisterForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(3, 80)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords don't match.")],
    )
    submit = SubmitField("Créer le compte")


class UserCreateForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(3, 80)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords don't match.")],
    )
    role = SelectField("Role", choices=[("user", "User"), ("admin", "Administrateur")])
    submit = SubmitField("Register user")


class LoginForm(FlaskForm):
    username = StringField("User name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UserEditForm(FlaskForm):
    username = StringField("User name", validators=[DataRequired(), Length(3, 80)])
    role = SelectField("Role", choices=[("user", "User"), ("admin", "Administrator")])
    is_active_account = BooleanField("Active user")
    new_password = PasswordField(
        "New password (leave empty for not changing it)",
        validators=[Optional(), Length(min=8)],
    )
    submit = SubmitField("Save")

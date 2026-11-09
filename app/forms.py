from flask_wtf import FlaskForm, _Auto, SUBMIT_METHODS
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Optional
from app.locales import localei18n

#
# FormTranslations is a base class to override standard translation fonction via babel
# 
# localei18n object must be provide at construction (and inject some dependency) 
class FormTranslations:

    
    def __init__(self, localetool:localei18n):
        self.localei18 = localetool

    #
    # gettext provide a function to retrieve a text message from the key passed as label in Form
    #
    def gettext(self, key:str):
        return self.localei18.get_string(key)

    #
    #*ngettext provide a function to retrieve a text message from the key passed as label in Form. Plural is not supported
    #
    def ngettext(self, singular, plural, n):
        return self.localei18.get_string(singular)
        return ungettext(singular, plural, n)



class BaseTranslate(FlaskForm):
    def __init__(self, formdata=_Auto, **kwargs):
        print ("BaseTranslate constructor")
        print (type(super()))

        super().__init__(formdata=formdata, **kwargs)
        

    def set_localei18 (self, locale:localei18n):
        self.localei18 = locale
    
    def _get_translations(self):
        print ("BaseTranslate._get_translations")
        return FormTranslations(self.localei18)
    
#
# User registration flask form
#
class RegisterForm(BaseTranslate):
    username = StringField("User name", validators=[DataRequired(), Length(3, 80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords don't match.")],
    )
    submit = SubmitField("Create user")


#
# User Creation flask orm
#
class UserCreateForm(BaseTranslate):
    username = StringField("User name", validators=[DataRequired(), Length(3, 80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords don't match.")],
    )
    role = SelectField("Role", choices=[("user", "User"), ("admin", "Administrator")])
    submit = SubmitField("Register user")

#
# User login flask form
#
class LoginForm(BaseTranslate):
    username = StringField("User name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


#
# profile edit flask form
#
class UserEditForm(BaseTranslate):
    username = StringField("User name", validators=[DataRequired(), Length(3, 80)])
    role = SelectField("Role", choices=[("user", "User"), ("admin", "Administrator")])
    is_active_account = BooleanField("Active user")
    new_password = PasswordField(
        "New password (leave empty for not changing it)",
        validators=[Optional(), Length(min=8)],
    )
    submit = SubmitField("Save")

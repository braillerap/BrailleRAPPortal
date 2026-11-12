from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Optional
from app.translations.locales import localei18n


localei18:localei18n = None

def forms_set_localei18 (localei18t:localei18n):
    global localei18

    localei18 = localei18t

def _ft (key:str) -> str:
    if localei18 != None:
        print ("_ft", key, localei18.get_string(key))
    else:
        print ("_ft", key)
    return localei18.get_string (key) if localei18 != None else key

class _tr ():
    def __init__(self, key:str):    
        self.key = key
    def __str__(self):
        return _ft(self.key)
    

#
# FormTranslations is a base class to override standard translation fonction via babel
# 
# localei18n object must be provide at construction (and inject some dependency) 
class FormTranslations:

    
    def __init__(self):
        #self.localei18 = localetool
        self.localei18 = None

    
    #
    # gettext provide a function to retrieve a text message from the key passed as label in Form
    #
    def gettext(self, key:str):
        print ("gettext call")
        if self.localei18:
            return self.localei18.get_string(key)
        else:
            return "no locale ???"

    #
    #*ngettext provide a function to retrieve a text message from the key passed as label in Form. Plural is not supported
    #
    def ngettext(self, singular, plural, n):
        if self.localei18:
            return self.localei18.get_string(singular)
        else:
            return "no locale define"
        #return ungettext(singular, plural, n)


class Translatori18 ():
    def __init__(self, key, localei18, codelocale):
        self.localei18 = localei18
        self.codelocale = codelocale
        self.key = key

    def __str__(self):
        print ("constructing", key, codelocale)
        return self.key
    
class BaseTranslate(FlaskForm):
    
    def set_localei18 (self, locale:localei18n, codelocale:str):
        self.localei18 = locale
        self.localei18.set_locale(codelocale)
        self.codelocale = codelocale
    
    def _tr18 (key:str):
        return Translatori18 (str(key) + self.codelocale, self.localei18, self.codelocale)

class _tr18p():
    def __init__(self):
        print ("_tr18p construct")
#
# User registration flask form
#
class RegisterForm(FlaskForm):
    username = StringField(_tr("form.user.name"), validators=[DataRequired(), Length(3, 80)])
    password = PasswordField(_tr("form.user.password"), validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField(
        _tr("form.user.confirmpassword"),
        validators=[DataRequired(), EqualTo("password", message=_tr("form.user.passwordnotmatch"))],
    )
    submit = SubmitField(_tr("form.createuser"))


#
# User Creation flask form
#
class UserCreateForm(FlaskForm):
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
class LoginForm(FlaskForm):

    username = StringField(_tr("form.user.name"), validators=[DataRequired()])
    password = PasswordField(_tr("form.user.password"), validators=[DataRequired()])
    submit = SubmitField(_tr("form.user.login"))


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

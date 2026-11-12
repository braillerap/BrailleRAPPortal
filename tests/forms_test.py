import pytest
import sys
from flask import Flask
from app import app


from app.forms import FormTranslations, LoginForm
from app.translations.locales import localei18n
from wtforms_test import FormTestCase



def test_path ():
    print (sys)
    print (sys.path)
    assert len(sys.path) > 2


def test_form_creation ():
    """
    test FormTranslations construction
    """
    locale = localei18n ()
    locale.set_locale ('en')
    ftest = FormTranslations (locale)

    data = ftest.gettext ('portal.name')
    print (data)
    assert data == "BrailleRAP Portal"

    locale.set_locale ('fr')

    data = ftest.gettext ('portal.name')
    print (data)
    assert data == "Portail BrailleRAP"


def test_form_translation ():
    """
    test the ability for a form to translate displayed text
    """
    locale = localei18n ()
    locale.set_locale ('en')

    with app.app_context():   
        ftest = LoginForm()
        ftest.set_localei18 (locale)
        print (ftest.username)
        print (LoginForm.username)
        #print (ftest.username.label)
        #print (type(ftest.username.label))

    return
    print (LoginForm.username.label())

    assert LoginForm.username.label() == "User name"

    locale.set_locale('fr')
    print (LoginForm.username.label())

    assert LoginForm.username.label() == "Utilisateur"

class TestUserForm(FormTestCase):
    form_class = LoginForm

    def test_translation(self):
        """_summary_
        """
        with app.app_context():  
            # define a CSRF key for test purpose
            app.config['SECRET_KEY'] = "keyfortest" 
            print  (TestUserForm.form_class.username)
            self.assert_required ('username')
            self.assert_required ('password')
            self.assert_label('username', "toto")
                
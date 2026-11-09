import pytest
import sys

from app.forms import FormTranslations, LoginForm
from app.locales import localei18n
from wtforms_test import FormTestCase

def test_path ():
    print (sys)
    print (sys.path)
    assert len(sys.path) > 2

"""
\brief test_form_creation test FormTranslations construction
"""
def test_form_creation ():
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

"""
\brief test_form_translation test the ability for a form to translate displayed text
"""
def test_form_translation ():
    locale = localei18n ()
    locale.set_locale ('en')

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
        
        print  (TestUserForm.form_class.username)
        self.assert_required ('username')
        self.assert_required ('password')
        self.assert_label('username', "toto")
        
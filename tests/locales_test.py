import pytest
#from app.locales import localei18n

@pytest.mark.skip(reason="need to solve import issue")
def locales_test ():
    loc = localei18n()

    assert loc != None
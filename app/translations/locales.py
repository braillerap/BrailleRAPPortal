"""
  
\file            locales.py
\brief           The file contain useful classes to internationalize the application


Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS LICENSED UNDER
                GNU GENERAL PUBLIC LICENSE
                    Version 3, 29 June 2007

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

This file is part of BrailleRAPPortal software.

SPDX-FileCopyrightText: 2026 Stephane GODIN <stephane@braillerap.org>

SPDX-License-Identifier: GPL-3.0 
  
"""

import json
import glob
import os
import i18n
"""class locales:
    def __init__(self):
        self.languages = {}
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        PATTERN = os.path.join(BASE_DIR, "languages/*.json")
        
        self.language_list= glob.glob (PATTERN )
        
        print (self.language_list)
        for lang in self.language_list:
            filename = lang.split('\\')
            lang_code = filename[-1].split('.')[0]
            
            with open(lang, 'r', encoding='utf8') as file:
                self.languages[lang_code] = json.loads(file.read())

    def get_locale_list (self):
        return self.language_list

    def get_locale_schema (self):
        english = self.languages['en']
        french = self.languages['fr']

        locschema = {
            "en":       {"lang":"en", dir:"ltr", "desc":"en - English",             "reverse":False, "data":self.languages['en'] },
            "fr":       {"lang":"fr", dir:'ltr', "desc":'fr - Français',            "reverse":False, "data":self.languages['fr'] },
        }

        return locschema
    
    def get_locale (self, lang):
        if lang in self.languages:
            for key in self.languages:
                print ("lang:", key)
            return self.languages[lang]

        return "??"

"""

class localei18n:
    """
    The class locali18n is a helper for python_i18n. The constructor load all locale files in the project
    and initialize python_i18n.
    """
    def __init__(self):
        """
            Constructor
        """
        self.languages = {}
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        PATTERN = os.path.join(BASE_DIR, "languages/*.json")
        
        self.language_list= glob.glob (PATTERN )


        # display locale definition file path
        print ()
        print ('#' * 40)
        print (self.language_list)
        print ('#' * 40)

        # set i18n option
        i18n.set('locale', 'fr')
        i18n.set('fallback', 'en')
        i18n.set('filename_format', '{locale}.{format}')
        i18n.set('skip_locale_root_data', True)
        i18n.load_path.append(os.path.join(BASE_DIR, './languages'))


    def get_locale_schema (self) -> dict:
        """
            The method get_locale_schema return a dict containing all loaded locales.
        """
        locschema = {}
        if 'en' in self.languages:
            english = self.languages['en']
            locschema['en'] = {"lang":"en", dir:"ltr", "desc":"en - English",             "reverse":False, "data":self.languages['en'] }
        if 'fr' in self.languages:
            french = self.languages['fr']
            locschema['fr'] = {"lang":"fr", dir:'ltr', "desc":'fr - Français',            "reverse":False, "data":self.languages['fr'] }

        return locschema

    def set_locale (self, locale):
        """
            The method set_locale define the current locale for use in translation method get_string().
        """
        i18n.set('locale', locale)
    
    def get_locale (self) -> str :
        """
            The method get_locale return the current locale used in translation method get_string().
        """
        return i18n.get ('locale')
    
    def get_string (self, key) -> str :
        """
            The method get_string return string associated with the current locale and the key parameter.

            Parameters:
            - key A key string associated with a string in translation files
        """
        return i18n.t(key)


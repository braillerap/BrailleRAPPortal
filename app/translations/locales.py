import json
import glob
import os
import i18n

class locales:
    def __init__(self):
        self.languages = {}
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        PATTERN = os.path.join(BASE_DIR, "languages/*.json")
        
        self.language_list= glob.glob (PATTERN )
        #self.language_list = glob.glob("./languages/*.json")
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


class localei18n:

    def __init__(self):
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


    def get_locale_schema (self):
        english = self.languages['en']
        french = self.languages['fr']

        locschema = {
            "en":       {"lang":"en", dir:"ltr", "desc":"en - English",             "reverse":False, "data":self.languages['en'] },
            "fr":       {"lang":"fr", dir:'ltr', "desc":'fr - Français',            "reverse":False, "data":self.languages['fr'] },
        }

    def set_locale (self, locale):
        i18n.set('locale', locale)

    def get_string (self, key) -> str :
            print ('search for key ', key)
            res = i18n.t (key)
            print (key, '=>', res)
            return i18n.t(res)


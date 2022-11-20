import locale
from lib.locale.init import translation
from lib.locale.ru import *

# The locale.getdefaultlocale() is obsolete, so this code should be updated
curr_lang = locale.getdefaultlocale()[0].split('_')[0]

def _(arg):
    if curr_lang in translation:
        if arg in translation[curr_lang]:
            return translation[curr_lang][arg]
    return arg

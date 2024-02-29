import locale
import sys
import os
from lib.locale import translation
from lib.locale.ru import *

if sys.platform != 'darwin':
    # The locale.getdefaultlocale() is obsolete, so this code should be updated
    curr_lang = locale.getdefaultlocale()[0].split('_')[0]
else:
    # Standard locale app doesn't work correct in the Mac OS, so use a hack
    sys_lang = os.popen("defaults read -g AppleLanguages").read()
    str_lang = sys_lang.translate({ord(i): None for i in '()"\n '})
    curr_lang = str_lang.split('-')[0]


def _(arg):
    if curr_lang in translation:
        if arg in translation[curr_lang]:
            return translation[curr_lang][arg]
    return arg

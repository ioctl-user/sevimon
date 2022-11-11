import locale

_emotions = {
    "en": ("Anger ", "Contm.", "Disgu.", "Fear  ", "Happs.", "Neutr.", "Sadns.", "Surpr."),
    "ru": ("Злость", "Презр.", "Отврщ.", "Страх ", "Радст.", "Нейтр.", "Грусть", "Удивл."),
}


# The locale.getdefaultlocale() is obsolete, so this code should be updated
curr_lang = locale.getdefaultlocale()[0].split('_')[0]
emotions = _emotions[curr_lang] if curr_lang in _emotions else _emotions["en"]

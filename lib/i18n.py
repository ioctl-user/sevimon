import locale

_emotions = {
    "C":           ("Anger ", "Contm.", "Disgu.", "Fear ", "Happs.",  "Neutr.", "Sadns.", "Surpr."),
    "ru_RU.UTF-8": ("Злость", "Презр.", "Отврщ.", "Страх ", "Радст.", "Нейтр.", "Грусть", "Удивл."),
}


curr_locale = '.'.join(locale.getlocale())
emotions = _emotions[curr_locale] if curr_locale in _emotions else _emotions["C"]

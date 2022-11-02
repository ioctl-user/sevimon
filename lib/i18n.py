import locale

_emotions = {
    "C" :           ["Anger ", "Contm.", "Disgu.", "Fear ", "Happs.",  "Neutr.", "Sadns.", "Surpr."],
    "ru_RU.UTF-8" : ["Злость", "Презр.", "Отврщ.", "Страх ", "Радст.", "Нейтр.", "Грусть", "Удивл."]
}

try:
    lang, enc = locale.getlocale()
    emotions = _emotions[lang + "." + enc]
except:
    emotions = _emotions["C"]

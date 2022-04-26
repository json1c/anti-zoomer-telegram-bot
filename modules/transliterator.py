import unicodedata
from transliterate import translit


class Transliterator:
    def __init__(self):
        self.mapping = {
            ord("@"): "а",
            ord("ґ"): "г",
            ord("0"): "о",
            ord("6"): "б",
            ord("4"): "ч"
        }
    
    def transliterate(self, text: str) -> str:
        text = text.lower()
        ru_text = translit(text, "ru")
        ru_text = ru_text.translate(self.mapping)

        return self.strip_accents(ru_text)
    
    def strip_accents(self, string, accents=('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT', 'COMBINING TILDE')):
        accents = set(map(unicodedata.lookup, accents))
        chars = [c for c in unicodedata.normalize('NFD', string) if c not in accents]

        return unicodedata.normalize('NFC', ''.join(chars))


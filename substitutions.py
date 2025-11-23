# _                                _                         
#| |substitutions.py              | |                        
#| | _____   _____  __ _ _ __   __| |_ ____      ___ __  ___ 
#| |/ _ \ \ / / _ \/ _` | '_ \ / _` | '_ \ \ /\ / / '_ \/ __|
#| | (_) \ V /  __/ (_| | | | | (_| | |_) \ V  V /| | | \__ \
#|_|\___/ \_/ \___|\__,_|_| |_|\__,_| .__/ \_/\_/ |_| |_|___/
#                                   | |                      
#                                   |_|  
import re

_DEBUG_PRINTS = False

PRONOUNS = {
    "male": {
        "he": "he", "she": "he",
        "him": "him", "her": "him",
        "his": "his",
        "himself": "himself", "herself": "himself",
    },
    "female": {
        "he": "she", "she": "she",
        "him": "her", "her": "her",
        "his": "her",
        "himself": "herself", "herself": "herself",
    },
}

def case_like(sample, word):
    if sample.isupper():
        return word.upper()
    if sample[:1].isupper():
        return word.capitalize()
    return word.lower()

def get_pronoun(base, gender):
    g = (gender or "").lower()
    if g not in PRONOUNS:
        return None
    return PRONOUNS[g].get(base.lower())

def get_trib(pool, n):
    i = n - 1
    return pool[i] if 0 <= i < len(pool) else None

class Substitutor:
    @staticmethod
    def normalize(text):
        if not text:
            return ""
        if _DEBUG_PRINTS:
            print(f"NORMALIZE IN: {text[:150]}")
        text = re.sub(r"\((?:Player|player)(\d+)\)", r"p\1", text)
        text = re.sub(r"\((?:Deadplayer|deadplayer)(\d+)\)", r"dp\1", text)
        text = re.sub(r"\b[Dd]ead[Pp](\d+)\b", r"dp\1", text)
        text = re.sub(r"\b[Dd][Pp](\d+)\b", r"dp\1", text)
        if _DEBUG_PRINTS:
            print(f"NORMALIZE OUT: {text[:150]}")
        return text

    @classmethod
    def expand(cls, text, tributes, dead_tributes=None):
        if not text:
            return ""
        if dead_tributes is None:
            dead_tributes = []

        def expand_slash(m):
            if _DEBUG_PRINTS:
                print(f"SLASH MATCHED: '{m.group(0)}'")
                print(f"  Groups: 1={m.group(1)}, 2={m.group(2)}, 3={m.group(3)}, 4={m.group(4)}, 5={m.group(5)}")
            is_dead = bool(m.group(1) or m.group(3))
            a_word = m.group(2)
            b_word = m.group(4)
            n = int(m.group(5))
            
            pool = dead_tributes if is_dead else tributes
            trib = get_trib(pool, n)
            if not trib:
                return "???"
            
            gender = (trib.get("gender") or "").lower()
            chosen = a_word if gender == "male" else b_word
            if _DEBUG_PRINTS:
                print(f"  Gender={gender}, chosen={chosen}")
            
            result = get_pronoun(chosen, gender)
            if result is None:
                return "???"
            final = case_like(chosen, result)
            if _DEBUG_PRINTS:
                print(f"  Returning: '{final}'")
            return final

        slash_pat = re.compile(
            r"\(([Dd])?(he|He|him|Him|his|His|himself|Himself|she|She|her|Her|herself|Herself)/"
            r"([Dd])?(he|He|him|Him|his|His|himself|Himself|she|She|her|Her|herself|Herself)(\d+)\)"
        )
        text = slash_pat.sub(expand_slash, text)

        def expand_single(m):
            is_dead = bool(m.group(1))
            word = m.group(2)
            n = int(m.group(3))
            
            pool = dead_tributes if is_dead else tributes
            trib = get_trib(pool, n)
            if not trib:
                return "???"
            
            result = get_pronoun(word, trib.get("gender"))
            if result is None:
                return "???"
            return case_like(word, result)

        single_pat = re.compile(
            r"\b([Dd])?(he|He|him|Him|his|His|himself|Himself|she|She|her|Her|herself|Herself)(\d+)\b"
        )
        text = single_pat.sub(expand_single, text)

        def expand_name(m):
            is_dead = m.group(1).lower() == "dp"
            n = int(m.group(2))
            
            pool = dead_tributes if is_dead else tributes
            trib = get_trib(pool, n)
            return trib.get("name", "???") if trib else "???"

        name_pat = re.compile(r"\b(dp|p)(\d+)\b")
        text = name_pat.sub(expand_name, text)

        return text

    @classmethod
    def process(cls, text, tributes, dead_tributes=None):
        return cls.expand(cls.normalize(text), tributes, dead_tributes or [])

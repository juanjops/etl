import re
from nltk.tokenize import TweetTokenizer
from spellchecker import SpellChecker


class JobsWords():

    def __init__(self, text, key_words, languages):

        self.text = text
        self.key_words = key_words
        self.languages = languages

    def get_key_misspelled_words(self):

        clean_tokens = self.get_clean_tokens()
        selected_key_words = self.get_key_words(clean_tokens)
        misspelled_words = self.get_misspelled_words(clean_tokens, selected_key_words)

        return " ".join(selected_key_words), " ".join(misspelled_words)

    def get_clean_tokens(self):

        clean_text = re.sub('[!#?¿,:";+.]', ' ', self.text)
        clean_text = re.sub(r"([a-z])([A-Z])", r"\1 \2", clean_text)
        clean_text = clean_text.lower()
        tknzr = TweetTokenizer()
        tokens = tknzr.tokenize(clean_text)

        return tokens

    def get_key_words(self, tokens):

        selected_key_words = [key_word for key_word in self.key_words if key_word in tokens]

        return selected_key_words

    def get_misspelled_words(self, tokens, selected_key_words):

        misspelled_words = {}

        for language in self.languages:
            spell = SpellChecker(language=language)
            misspelled_words[language] = list(spell.unknown(tokens))

        temp = min(map(len, misspelled_words.values()))
        min_key = [key for key in misspelled_words if len(misspelled_words[key]) == temp]
        minimum_misspelled_words = misspelled_words[min_key[0]]
        not_repeated_misspelled_words = [
            word for word in minimum_misspelled_words if word not in selected_key_words]

        return not_repeated_misspelled_words

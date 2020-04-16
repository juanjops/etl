import re
import spacy
from langdetect import detect
from spellchecker import SpellChecker


EN_NLP = spacy.load("en_core_web_sm")
ES_NLP = spacy.load("es_core_news_sm")

LANGUAGES = {
    "en": EN_NLP,
    "es": ES_NLP
}


class JobsWords():
    
    def __init__(self, text, key_words):

        self.text = text
        self.key_words = key_words
        self.language = detect(text)

    def get_key_misspelled_words(self):

        clean_text = self.get_reg()
        tokens = self.get_tokens(clean_text)
        selected_key_words = self.get_key_words(clean_text)
        misspelled_words = self.get_misspelled_words(tokens)

        return " ".join(selected_key_words), " ".join(misspelled_words)

    def get_reg(self):

        clean_text = re.sub('[)!#?¿,:";+./(•]|-', ' ', self.text)
        clean_text = re.sub(r"([a-z])([A-Z]|[0-9])", r"\1 \2", clean_text)
        clean_text = re.sub(r"([0-9])([A-Z]|[a-z])", r"\1 \2", clean_text)
        clean_text = re.sub(r"([A-Z])([A-Z])([a-z])", r"\1 \2\3", clean_text)
        clean_text = clean_text.lower()

        return clean_text

    def get_tokens(self, clean_text):

        nlp = LANGUAGES[self.language]
        tokens = [token.lemma_ for token in nlp(clean_text)]

        return tokens

    def get_key_words(self, clean_text):

        selected_key_words = [
            key_word for key_word in self.key_words if key_word in clean_text]

        return selected_key_words

    def get_misspelled_words(self, tokens):

        selected_key_words = [
            key_word for key_word in self.key_words if key_word in tokens]
        spell = SpellChecker(language=self.language)
        misspelled_words = list(spell.unknown(tokens))
        not_repeated_misspelled_words = [
            word for word in misspelled_words if word not in selected_key_words]

        return not_repeated_misspelled_words

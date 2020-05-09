import re
import spacy
from langdetect import detect
from spellchecker import SpellChecker
from collections import OrderedDict


class JobsWords():
    
    def __init__(self, key_words, models):

        self.key_words = key_words
        self.models = models

    def get_key_misspelled_words(self, text):

        language = detect(text)
        clean_text = JobsWords.get_reg(text)
        tokens = self.get_tokens(language, clean_text)
        selected_key_words = self.get_key_words(tokens)
        misspelled_words = JobsWords.get_misspelled_words(language, tokens, selected_key_words)
        sentence_experience = self.get_sentence_word_related(language, text, "Experience")

        return (
            " ".join(selected_key_words),
            " ".join(misspelled_words),
            ".".join(sentence_experience))

    @staticmethod
    def get_reg(text):

        clean_text = re.sub('[)!#?¿,:";+./(•]|-', ' ', text)
        clean_text = re.sub(r"([a-z])([A-Z]|[0-9])", r"\1 \2", clean_text)
        clean_text = re.sub(r"([0-9])([A-Z]|[a-z])", r"\1 \2", clean_text)
        clean_text = re.sub(r"([A-Z])([A-Z])([a-z])", r"\1 \2\3", clean_text)
        clean_text = clean_text.lower()

        return clean_text

    def get_tokens(self, language, clean_text):

        documents = self.models[language](clean_text)
        tokens = [token.lemma_ for token in documents]

        return tokens

    @staticmethod
    def get_plural_key_words(words):
        
        key_words_list = []
        for word in words:
            key_words_list.append(word)
            if word[-1]!= "s":
                key_words_list.append(word + "s")
            else:
                key_words_list.append(word[:-1])

        return key_words_list

    def get_key_words(self, tokens):

        tokens_sing_plu = JobsWords.get_plural_key_words(tokens)
        selected_key_words = [
            word for word in self.key_words if word in tokens_sing_plu]

        return list(dict.fromkeys(selected_key_words))

    @staticmethod
    def get_misspelled_words(language, tokens, selected_key_words):

        spell = SpellChecker(language=language)
        misspelled_words = list(spell.unknown(tokens))
        selected_key_words_plu = JobsWords.get_plural_key_words(selected_key_words)
        misspelled_words = [
            word for word in misspelled_words if word not in selected_key_words_plu]

        return list(dict.fromkeys(misspelled_words))

    def get_sentence_word_related(self, language, text, word):
        
        clean_text = re.sub('-', ' ', text)
        clean_text = re.sub(r"([.])([A-Z])", r"\1 \2", clean_text)
        clean_text = re.sub(r"([a-z])([A-Z])", r"\1, \2", clean_text)
        documents = self.models[language](clean_text)
        sentences = [
            str(sentence) for sentence in list(documents.sents)
            if (word in str(sentence)) or (word.lower() in str(sentence))]

        return sentences

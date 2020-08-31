import re
from itertools import chain
from collections import Counter
from langdetect import detect
from spellchecker import SpellChecker


class JobsWords():

    def __init__(self, key_words, models):

        self.key_words = key_words
        self.models = models

    def get_key_misspelled_words(self, text):

        language = JobsWords.get_language(text)
        clean_text = JobsWords.get_reg(text)
        tokens = self.get_tokens(language, clean_text)
        selected_key_words = self.get_key_words(tokens)
        misspelled_words = JobsWords.get_misspelled_words(language, tokens, selected_key_words)
        sentence_experience = self.get_sentence_word_related(language, text, "Experience")
        cluster = self.get_cluster(tokens)

        return (
            language,
            " ".join(tokens),
            " ".join(selected_key_words),
            " ".join(misspelled_words),
            ".".join(sentence_experience),
            Counter(cluster),
            language)

    @staticmethod
    def get_language(text):

        return detect(text)

    @staticmethod
    def get_reg(text):

        clean_text = re.sub('[)!#?¿,:"*&;+./(•€$£%…=™“]|-|–', ' ', text)
        clean_text = re.sub(r"([a-z])([A-Z]|[0-9])", r"\1 \2", clean_text)
        clean_text = re.sub(r"([0-9])([A-Z]|[a-z])", r"\1 \2", clean_text)
        clean_text = re.sub(r"([A-Z])([A-Z])([a-z])", r"\1 \2\3", clean_text)
        clean_text = re.sub(r"\b\d+\b", "", clean_text)
        clean_text = clean_text.lower()

        return clean_text

    def get_tokens(self, language, clean_text):

        documents = self.models[language](clean_text)
        tokens = [token.lemma_ for token in documents]
        all_stopwords = self.models[language].Defaults.stop_words
        tokens_without_sw = [word for word in tokens if word not in all_stopwords]
        tokens_without_sw = list(filter(("-PRON-").__ne__, tokens_without_sw))
        tokens_without_sw = [x.strip(' ') for x in tokens_without_sw]
        tokens_without_sw = list(filter(("").__ne__, tokens_without_sw))
        tokens_without_sw = list(dict.fromkeys(tokens_without_sw))

        return tokens_without_sw

    @staticmethod
    def get_plural_key_words(words):

        key_words_list = []
        for word in words:
            key_words_list.append(word)
            if word[-1] != "s":
                key_words_list.append(word + "s")
            else:
                key_words_list.append(word[:-1])

        return key_words_list

    def get_key_words(self, tokens):

        tokens_sing_plu = JobsWords.get_plural_key_words(tokens)
        key_words = sum(self.key_words.values(), [])
        selected_key_words = [
            word for word in key_words if word in tokens_sing_plu]

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

        clean_text = re.sub('[-–]', ' ', text)
        clean_text = re.sub(r"([.])([A-Z])", r"\1 \2", clean_text)
        clean_text = re.sub(r"([a-z])([A-Z])", r"\1, \2", clean_text)
        documents = self.models[language](clean_text)
        sentences = [
            str(sentence) for sentence in list(documents.sents)
            if (word in str(sentence)) or (word.lower() in str(sentence))]

        return sentences

    def get_cluster(self, tokens):

        cluster = [
            [key for token in tokens if token in self.key_words[key]]
            for key in self.key_words.keys()]
        cluster = list(chain(*cluster))

        return cluster

from sklearn.pipeline import Pipeline
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD, NMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pyLDAvis
import pyLDAvis.sklearn


class SklearnTopicModels():

    RANDOM_STATE = 42

    def __init__(self, n_clusters, vectorizer, estimator):
        """
        n_clusters is the desired number of topics
        """
        self.vector_options = {
            "Count": CountVectorizer(binary=True),
            "Tfidf": TfidfVectorizer()
        }

        self.model_options = {
            "LDA": LatentDirichletAllocation(n_components=n_clusters, random_state=self.RANDOM_STATE),
            "LSA": TruncatedSVD(n_components=n_clusters, random_state=self.RANDOM_STATE),
            "NMF": NMF(n_components=n_clusters, random_state=self.RANDOM_STATE)
        }

        self.model = Pipeline([
            ('vect', self.vector_options[vectorizer]),
            ('model', self.model_options[estimator])
        ])

    def fit_transform(self, documents):
        self.model.fit_transform(documents)
        return self.model

    def get_topics(self, n_top_words=25):
        """
        n_top_words is the number of top terms to show for each topic
        """
        vectorizer = self.model.named_steps['vect']
        model = self.model.steps[-1][1]
        names = vectorizer.get_feature_names()
        topics = dict()
        for idx, topic in enumerate(model.components_):
            features = topic.argsort()[:-(n_top_words - 1): -1]
            tokens = [names[i] for i in features]
            topics[idx] = tokens
        return topics

    def get_plot(self, documents, mds):
        """
        mds can be pca as default or tsne or mmds
        """
        pyLDAvis.enable_notebook()
        vectorizer = self.model.named_steps["vect"]
        vocab = self.model.named_steps['vect'].fit_transform(documents)
        model = self.model.named_steps['model'].fit(vocab)

        return pyLDAvis.sklearn.prepare(model, vocab, vectorizer, mds=mds)

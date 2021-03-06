from sklearn.pipeline import Pipeline
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD, NMF
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer
import pyLDAvis
import pyLDAvis.sklearn
import pandas as pd


class SklearnTopicModels():

    def __init__(self, vectorizer, estimator, **kwargs):
        """
        n_clusters is the desired number of topics
        """
        self.vector_options = (
            CountVectorizer(binary=True) if vectorizer == "Count" else
            HashingVectorizer(binary=True) if vectorizer == "Hash" else
            TfidfVectorizer() if vectorizer == "Tfidf" else
            None
        )

        self.estimator_options = (
            LatentDirichletAllocation(**kwargs) if vectorizer == "LDA" else
            TruncatedSVD(**kwargs) if vectorizer == "LSA" else
            NMF(**kwargs) if vectorizer == "NMF" else
            None
        )

        self.model = Pipeline([
            ('vect', self.vector_options),
            ('model', self.estimator_options)
        ])

    def fit_transform(self, documents):
        self.model.fit_transform(documents)
        return self.model

    def get_topics(self, n_top_words=15):
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
        return pd.DataFrame(topics)

    def get_plot(self, documents, mds):
        """
        mds can be pca as default or tsne or mmds
        """
        try:
            pyLDAvis.enable_notebook()
            vectorizer = self.model.named_steps["vect"]
            vocab = self.model.named_steps['vect'].fit_transform(documents)
            model = self.model.named_steps['model'].fit(vocab)

            return pyLDAvis.sklearn.prepare(model, vocab, vectorizer, mds=mds)

        except:
            print("ERROR pyLDAvis cannot print this model")

    def get_topic_documents(self, documents, jobs_id):

        topics_documents = self.model.transform(documents)
        topics = [
            [document.tolist().index(document.max()), document.max()]
            for document in topics_documents]
        jobs_topic = [
            {"job_id": element[0], "cluster": element[1][0], "probability": element[1][1]}
            for element in zip(jobs_id, topics)]

        return jobs_topic

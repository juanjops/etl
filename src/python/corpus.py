from sklearn.pipeline import Pipeline
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD, NMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pyLDAvis
import pyLDAvis.sklearn


class SklearnTopicModels():
    
    def __init__(self, n_clusters, vectorizer, estimator, mds):
        """
        n_clusters is the desired number of topics
        """
        self.vect = {
            "Count": CountVectorizer(binary=True),
            "Tfidf": TfidfVectorizer()
        }
        
        self.model_dict = {
            "LDA": LatentDirichletAllocation(n_components=n_clusters),
            "LSA": TruncatedSVD(n_components=n_clusters),
            "NMF": NMF(n_components=n_clusters)
        }
            
        self.model = Pipeline([
            ('vect', self.vect[vectorizer]),
            ('model', self.model_dict[estimator])
        ])
        
        self.mds = mds
    
    def fit_transform(self, documents):
        self.model.fit_transform(documents)
        return self.model

    def get_topics(self, n=25):
        """
        n is the number of top terms to show for each topic
        """
        vectorizer = self.model.named_steps['vect']
        model = self.model.steps[-1][1]
        names = vectorizer.get_feature_names()
        topics = dict()
        for idx, topic in enumerate(model.components_):
            features = topic.argsort()[:-(n - 1): -1]
            tokens = [names[i] for i in features]
            topics[idx] = tokens
        return topics
    
    def get_plot(self, documents):
        
        pyLDAvis.enable_notebook()
        vectorizer = self.model.named_steps["vect"]
        vocab = self.model.named_steps['vect'].fit_transform(documents)
        model = self.model.named_steps['model'].fit(vocab)

        return pyLDAvis.sklearn.prepare(model, vocab, vectorizer, mds=self.mds)

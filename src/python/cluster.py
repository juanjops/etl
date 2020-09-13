from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
import pandas as pd
from yellowbrick.cluster import SilhouetteVisualizer


class SklearnClusterModels():

    def __init__(self, vectorizer, clusterer, **kwargs):
        """
        n_clusters is the desired number of topics
        """
        self.vector_options = (
            CountVectorizer(binary=True) if vectorizer == "Count" else
            HashingVectorizer(binary=True) if vectorizer == "Hashing" else
            TfidfVectorizer() if vectorizer == "Tfidf" else
            None
        )

        self.clusterer_options = (
            KMeans(**kwargs) if clusterer == "KMeans" else
            KMedoids(**kwargs) if clusterer == "KMedoids" else
            None
        )

        self.model = Pipeline([
            ('vect', self.vector_options),
            ('clusterer', self.clusterer_options)
        ])

    def fit_transform(self, documents):
        self.model.fit_transform(documents)
        return self.model

    def get_silhouette_plot(self, documents):
        """
        mds can be pca as default or tsne or mmds
        """
        try:

            visualizer = SilhouetteVisualizer(self.model.named_steps["clusterer"])
            documents_vectorized = self.model.named_steps['vect'].fit_transform(documents)
            visualizer.fit(documents_vectorized)
            return visualizer.poof()

        except:
            print("ERROR silhoutte cannot print this model")

    def get_clusters(self, documents, jobs_id):

        clusters = self.model.named_steps["clusterer"].labels_
        jobs_clusters = [
            {"job_id": element[0], "cluster": element[1]}
            for element in zip(jobs_id, clusters)]

        return jobs_clusters

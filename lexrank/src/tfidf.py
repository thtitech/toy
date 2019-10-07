import gensim

class TfidfModel(object):
    def __init__(self):
        self.no_below = 10
        self.no_above = 0.5
        self.keep_n = 10000

    def generate(self, docs):
        dictionary = gensim.corpora.Dictionary(docs)
        dictionary.filter_extremes(no_below=self.no_below,
                                   no_above=self.no_above,
                                   keep_n=self.keep_n)
        corpus = [dictionary.doc2bow(doc) for doc in docs]
        tfidf_model = gensim.models.TfidfModel(corpus)
        return tfidf_model, dictionary

import gensim
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from preprocessing import *
from tfidf import *
from summarize import *
import numpy as np

def main(debug=False):
    file_name = "../data/report.txt"
    doc = load_data(file_name)
    sentences, corpus = preprocess(doc, debug)
    parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))
    summarizer = LexRankSummarizer()
    summarizer.stop_words = [' ']
    summary = summarizer(document=parser.document, sentences_count=3)
    for sentence in summary:
        print(sentences[corpus.index(sentence.__str__())])

def main2(debug=False, sent_limit=3, lambda_=0.7):
    docs = load_data("../data/database.txt")
    corpus = make_corpus(docs)
    tfidf = TfidfModel()
    model, dictionary = tfidf.generate(corpus)
    dictionary.save_as_text("../data/dict.txt")
    model.save("../data/model.model")

    """
    dictionary = gensim.corpora.Dictionary.load_from_text("../data/dict.txt")
    model = gensim.models.TfidfModel.load("../data/model.model")
    """

    target = read_file("../data/report.txt")
    target_sent, target_corpus = preprocess_target(target)

    indexes = summarize(target_corpus, model, dictionary, sent_limit=sent_limit, lambda_=lambda_)

    for index in sorted(indexes):
        print(target_sent[index])
    
if __name__ == "__main__":
    #numpy.set_printoptions(numpy.inf)
    main2()


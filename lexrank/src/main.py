import gensim
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from preprocessing import *
from tfidf import *
from summarize import *
import numpy

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

def main2(debug=False):
    """
    docs = load_data("../data/database.txt")
    sentences, corpus = preprocess2(docs)

    if debug:
        print("finish loading corpus")


    tfidf = TfidfModel()
    model, dictionary = tfidf.generate(corpus)

    dictionary.save_as_text("../data/dict.txt")
    model.save("../data/model.model")
    """
    dictionary = gensim.corpora.Dictionary.load_from_text("../data/dict.txt")
    model = gensim.models.TfidfModel.load("../data/model.model")
    
    if debug:
        print("finish loading tfidf")
    
    target = read_file("../data/report.txt")
    target_sent, target_corpus = preprocess2([target])
    
    if debug:
        print("finish loading target doc")

    print(len(target_corpus[0]), len(target_sent[0]))
    print(target_corpus[0])
    
    indexs = summarize(
        [line.split(" ") for line in target_corpus[0]], model, dictionary,
        sent_limit=10
    )

    print(len(target_sent[0]))
    print(indexs)
    print("\n".join([target_sent[0][i] for i in sorted(list(indexs))]))
    
if __name__ == "__main__":
    numpy.set_printoptions(numpy.inf)
    main2(debug=True)


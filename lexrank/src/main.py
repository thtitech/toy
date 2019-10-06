from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from preprocessing import preprocess
from preprocessing import load_data

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
    
if __name__ == "__main__":
    main()


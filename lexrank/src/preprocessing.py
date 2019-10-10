import copy
import re
import mojimoji

from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter

def preprocess(doc, debug=False):
    """
    ドキュメントを引数にとってそれを前処理した上で文のリストに分割する
    @param doc 対象のドキュメント
    @return 前処理されたドキュメントに含まれる文のリスト
    """

    doc = doc.lower()

    lines = re.split("\n|。", doc)
    lines = list(filter(lambda x: x != "", map(lambda x: x.strip(), lines)))
    sentences = copy.deepcopy(lines)
    lines = list(map(lambda x: mojimoji.zen_to_han(x), lines))
    
    analyzer = Analyzer(
        [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)､｡｢｣]', ' ')],
        JanomeTokenizer(),
        [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')])
    corpus = [' '.join(analyzer.analyze(l)) + '。' for l in lines]
    if debug:
        print("\n".join(corpus))

    return sentences, corpus

def load_data(file_name, cutoff=None):
    tmp = []
    c = 0
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            if cutoff is not None and c > cutoff:
                break
            tmp.append(line)
            c += 1
    return tmp

def read_file(file_name):
    tmp = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            tmp.append(line)
    return "\n".join(tmp)
    
def preprocess2(docs, debug=False):
    docs = list(map(lambda d: list(filter(lambda x: x.strip() != "", re.split("\n|。", d.lower()))), docs))

    sentences = copy.deepcopy(docs)

    docs = [list(map(lambda x: mojimoji.zen_to_han(x), lines)) for lines in docs]

    analyzer = Analyzer(
        [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)､｡｢｣]', ' ')],
        JanomeTokenizer(),
        [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')])

    corpus = []
    for lines in docs:
        for line in lines:
            tmp = []
            words = analyzer.analyze(line)
            for word in words:
                tmp.append(word)
            corpus.append(tmp)
    #corpus = [[list(analyzer.analyze(l)) for l in lines] for lines in docs]

    if debug:
        print("\n".join(corpus))
    
    return sentences, corpus

import copy
import re
import mojimoji
import itertools

from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter

def preprocess(doc, debug=False):
    """
    ドキュメントを引数にとってそれを前処理した上でトークナイズされた文のリストに分割する
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
    """
    対象のファイルを文のリストとして読み取る
    @param file_name 対象となるファイル名
    @param cutoff 途中で読み込みを中断する行数
    @return 各行が格納されたリスト
    """
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
    """
    対象のファイルを文字列として読み取る
    @param file_name 対象となるファイル名
    @return ファイルの内容の文字列
    """
    tmp = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            tmp.append(line)
    return "\n".join(tmp)
    
def make_corpus(docs, debug=False):
    """
    複数の文書からコーパスを作成する
    @docs 文書のリスト
    @return トークナイズされた文書のリスト
    """
    docs = list(map(lambda d: list(filter(lambda x: x.strip() != "", re.split("\n|。", d.lower()))), docs))

    docs = [list(map(lambda x: mojimoji.zen_to_han(x), lines)) for lines in docs]

    analyzer = Analyzer(
        [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)､｡｢｣]', ' ')],
        JanomeTokenizer(),
        [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')])

    corpus = [list(itertools.chain.from_iterable([list(analyzer.analyze(l)) for l in lines])) for lines in docs]

    if debug:
        print("\n".join(corpus))
    
    return corpus

def preprocess_target(doc, debug=False):
    doc = list(filter(lambda x: x.strip() != "", re.split("\n|。", doc.lower())))

    sentences = copy.deepcopy(doc)

    doc = [mojimoji.zen_to_han(line) for line in doc]

    analyzer = Analyzer(
        [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)､｡｢｣]', ' ')],
        JanomeTokenizer(),
        [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')])

    corpus = [list(analyzer.analyze(line)) for line in doc]

    if debug:
        print(corpus)
        
    return sentences, corpus

import numpy as np
import networkx
from sklearn.metrics.pairwise import cosine_similarity

def summarize(sentences, model, dictionary, sent_limit=10, lambda_=0.7):
    """
    文書要約をおこなう
    @param sentences 文のリスト
    @param model 学習モデル
    @param dictionary 辞書(gensim)
    @param sent_limit 抽出したい文の個数
    @param lambda_ ハイパーパラメータ
    @return 抽出された文のindexのリスト
    """
    sent_vecs = [model[dictionary.doc2bow(sent)] for sent in sentences]
    dim = len(dictionary.token2id)
    
    sentence_scores, sim_mat = lexrank(sent_vecs, dim)
    indexes = mmr_sort(lambda_, sentences, sent_limit,
                       sentence_scores, sim_mat)

    return indexes

def lexrank(sent_vecs, dim, alpha=0.85, max_iter=100000):
    """
    lexrank本体の実装
    @param sent_vecs 文書のdoc2vec表現のリスト
    @param dim 次元
    @param alpha ハイパーパラメータ
    @param max_iter 何回まで繰り返して固有値の収束を待つか
    """
    sent_vecs = np.array([convert_to_sparse_vector(sent_vec, dim) for sent_vec in sent_vecs])

    sim_mat = cosine_similarity(sent_vecs)
    sim_mat = normalize_mat(sim_mat, len(sim_mat[0]))
    
    linked_rows, linked_cols = np.where(sim_mat > 0)
    graph = networkx.DiGraph()
    graph.add_nodes_from(list(range(sent_vecs.shape[0])))
    for i, j in zip(linked_rows, linked_cols):
        if i == j:
            continue
        graph.add_edge(i, j, weight=sim_mat[i, j])

    scores = networkx.pagerank_scipy(graph, alpha=alpha, max_iter=max_iter)

    return scores, sim_mat

def mmr_sort(lambda_, sentences, sent_limit, sentence_scores, sim_mat):
    """
    mmrを加味したソートを行う
    @param lambda_ ハイパーパラメータで高いほど文書の重要度を重視
    @param sentences 対象となる文のリスト
    @param sent_limit 抽出する文の個数
    @param sentence_scores 各文のスコア
    @param sim_mat 類似度行列
    @return 抽出された分のインデックスのリスト
    """
    indexes = []
    sentence_ids = set(range(len(sentences)))
    while len(indexes) < sent_limit and set(indexes) != sentence_ids:
        remaining = sentence_ids - set(indexes)
        mmr_score = lambda x: (lambda_*sentence_scores[x] - (1-lambda_)*max([sim_mat[x, y] for y in set(indexes)-{x}] or [0]))
        next_selected = argmax(remaining, mmr_score)
        indexes.append(next_selected)
    return indexes

def argmax(keys, f):
    """
    argmaxを計算する
    """
    return max(keys, key=f)

def convert_to_sparse_vector(sent_vecs, dim):
    """
    gensimのdoc2vec表現からベクトル表現を作成する
    @param sent_vecs 対象となる文がgensim形式でdoc2vec表現されたもののリスト
    @param dim 表現ベクトルの次元
    @return 各文のベクトル表現のリスト
    """
    array = np.zeros(dim, dtype="float32")
    for index, count in sent_vecs:
        array[index] = count
    return array

def normalize_mat(sim_mat, dim):
    """
    まだスケルトン実装
    行列の正規化を行う
    @param sim_mat 正方行列
    @param dim 次元
    """
    result = np.zeros(sim_mat.shape)
    for i in range(dim):
        tmp_sum = 0
        for j in range(dim):
            tmp_sum += sim_mat[i][j]
        for j in range(dim):
            result[i][j] = sim_mat[i][j]/tmp_sum
    return sim_mat

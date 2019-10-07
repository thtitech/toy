import numpy as np
import networkx
from sklearn.metrics.pairwise import cosine_similarity

def summarize(sentences, model, dictionary, sent_limit=10, lambda_=0.7):
    sent_vecs = [model[dictionary.doc2bow(sent)] for sent in sentences]
    
    sentence_scores, sim_mat = lexrank(sent_vecs)
    indexes = mmr_sort(lambda_, sentences, sent_limit,
                       sentence_scores, sim_mat)

    return [sentences[i] for i in sorted(list(indexes))]

def mmr_sort(lambda_, sentences, sent_limit, sentence_scores, sim_mat):
    indexes = set()
    sentence_ids = set(range(len(sentences)))
    while len(indexes) < sent_limit and set(indexes) != sentence_ids:
        remaining = sentence_ids - set(indexes)
        mmr_score = lambda x: (lambda_*sentence_scores[x] - (1-lambda_)*max([sim_mat[x, y] for y in set(indexes)-{x}] or [0]))
        next_selected = argmax(remaining, mmr_score)
        indexes.add(next_selected)
    return indexes

def argmax(keys, f):
    return max(keys, key=f)

def lexrank(sent_vecs, alpha=0.85, max_iter=100000):
    #sent_vecs_sparse = convert_to_sparse_vector(sent_vecs)

    sim_mat = cosine_similarity(sent_vecs)
    linked_rows, linked_cols = np.where(sim_mat > 0)

    graph = networkx.DiGraph()
    graph.add_nodes_from(range(sent_vecs.shape[0]))
    for i, j in zip(linked_rows, linked_cols):
        if i == j:
            continue
        graph.add_edge(i, j, {'weight': sim_mat[i, j]})

    scores = networkx.pagerank_scipy(graph, alpha=alpha, max_iter=max_iter)

    return scores, sim_mat

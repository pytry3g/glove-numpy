from argparse import ArgumentParser
from functools import partial
import pickle
import numpy as np


def make_id2word(vocab):
    return dict((id, word) for word, (id, _) in vocab.items())


def merge_main_context(W, merge_fun=lambda m, c: np.mean([m, c], axis=0),
                       normalize=True):
    """
    Merge the main-word and context-word vectors for a weight matrix
    using the provided merge function (which accepts a main-word and
    context-word vector and returns a merged version).

    By default, `merge_fun` returns the mean of the two vectors.
    """

    vocab_size = len(W) // 2
    for i, row in enumerate(W[:vocab_size]):
        merged = merge_fun(row, W[i + vocab_size])
        if normalize:
            merged /= np.linalg.norm(merged)
        W[i, :] = merged

    return W[:vocab_size]


def most_similar(W, vocab, id2word, word, n=15):
    """
    Find the `n` words most similar to the given `word`. The provided
    `W` must have unit vector rows, and must have merged main- and
    context-word vectors (i.e., `len(W) == len(word2id)`).

    Returns a list of word strings.
    """

    assert len(W) == len(vocab)

    word_id = vocab[word][0]

    dists = np.dot(W, W[word_id])
    top_ids = np.argsort(dists)[::-1][:n + 1]

    return [id2word[id] for id in top_ids if id != word_id][:n]

def similar_sentences(W, vocab, sentence):
    """
    Find the 'n' similar sentences to the given 'sentence'.
    Return the similar sentences.
    """
    pass

def plain_glove_document_vector(W, vocab, tokens):
    bag_of_centroids = np.zeros(W.shape[1], dtype='float32')
    for token in tokens:
        try:
            word_id = vocab[token][0]
            temp = W[word_id]
        except:
            continue
        bag_of_centroids += temp
    bag_of_centroids = bag_of_centroids / len(tokens)
    return bag_of_centroids

def parse_args():
    parser = ArgumentParser(
        description=('Evaluate a GloVe vector-space model on a word '
                     'analogy test set'))

    parser.add_argument('vectors_path', type=partial(open, mode='rb'),
                        help=('Path to serialized vectors file as '
                              'produced by this GloVe implementation'))

    parser.add_argument('analogies_paths', type=partial(open, mode='r'),
                        nargs='+',
                        help=('Paths to analogy text files, where each '
                              'line consists of four words separated by '
                              'spaces `a b c d`, expressing the analogy '
                              'a:b :: c:d'))

    return parser.parse_args()

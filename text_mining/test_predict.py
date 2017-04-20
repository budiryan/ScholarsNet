from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
import string
import pandas as pd
import numpy as np
import pickle


def stem_tokens(tokens):
    stemmer = nltk.stem.porter.PorterStemmer()
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


with open('tfidf_vectorizer.pickle', 'rb') as f:
    tfidf_vectorizer = pickle.load(f)[0]

with open('nb_clf.pickle', 'rb') as f:
    # print 'nb_clf, just load it...'
    nb_clf = pickle.load(f)[0]

data = tfidf_vectorizer.transform(np.array(['Computer Vision']))
print('Prediction: ', nb_clf.predict(data))

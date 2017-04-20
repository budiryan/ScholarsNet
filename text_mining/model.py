from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
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


def train():
    '''
    READ FILE, TRANSFORM TRAINING DATA INTO TF-IDF
    '''
    # Pickle no 2: tfidf_vectorizer
    X = np.array(train_df['title'])
    y = np.array(train_df['category'])
    tfidf_vectorizer = None
    try:
        with open('tfidf_vectorizer.pickle', 'rb') as f:
            print('just load idf')
            tfidf_vectorizer = pickle.load(f)[0]
    except:
        pass

    if not tfidf_vectorizer:
        print('training tfidf')
        tfidf_vectorizer = TfidfVectorizer(
            tokenizer=normalize, stop_words='english'
            , analyzer='word', norm='l2')
        tfidf_vectorizer = tfidf_vectorizer.fit(X)
        with open('tfidf_vectorizer.pickle', 'wb') as f:
            pickle.dump([tfidf_vectorizer], f)

    # Pickle no 3: Naive Bayes Classifier
    clf = None
    try:
        with open('clf.pickle', 'rb') as f:
            print('clf, just load it...')
            clf = pickle.load(f)[0]
    except:
        pass

    if not clf:
        print('training')
        X = tfidf_vectorizer.transform(X)
        clf = MultinomialNB(alpha=1.0).fit(X, y)
        # clf = SVC().fit(X, y)
        with open('clf.pickle', 'wb') as f:
            pickle.dump([clf], f)
    return tfidf_vectorizer, clf


if __name__ == '__main__':
    X = np.array(train_df['title'])
    y = np.array(train_df['category'])
    train_df = pd.read_csv('json/train.csv')
    tfidf, clf = train()
    print('predicting now:..')
    X = tfidf.transform(X)
    res = clf.predict(X)
    print('res is: ', res)
    print(accuracy_score(y, res))

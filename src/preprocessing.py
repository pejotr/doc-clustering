import os
import logging
import re
import math

import numpy
import nltk

from nltk.cluster import *
from nltk.tokenize import *
from nltk.cluster.util import *
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.probability import FreqDist

def compute_tfidf(document, documents):
    logging.info("Computing tfidf values for document: " + document['docname'])

    tfidf = {}
    d = len(documents)

    for term in document['terms']:
        occ = [ x for x, y in documents.iteritems() if y['tf'][term] > 0 ]
        val = document['tf'][term] * math.log10( d / len(occ) )
        tfidf[term] = val

    return tfidf


def process_documents(path):
    logging.info("Using documents from \"" + path + "\" directory ")
    
    if path[-1] != "/" :
        path + "/"

    documents = {}
    allterms  = {}
    stemmer   = PorterStemmer()
    listing   = os.listdir(path)

    # retriving document content - discarding structure
    for infile in listing:
        raw_doc    = nltk.clean_html(open(path + infile, 'r').read())
        word_list  = nltk.word_tokenize(re.sub('[^A-Za-z0-9 ]', '', raw_doc))
        terms_list = [ x.lower() for x in word_list if x.lower() not in stopwords.words('english')]

        stemmes = []
        for term in terms_list :
            stemmes[len(stemmes):] = [stemmer.stem(term)]
            allterms[stemmer.stem(term)] = 0

        fdist = FreqDist(word.lower() for word in stemmes)
        documents[infile] = { 'docname': infile,  'terms': stemmes, 'tf': fdist, 'tfidf': None  }

    for key, doc in documents.iteritems():
        doctfidf = compute_tfidf(doc ,documents)
        documents[key]['tfidf'] = dict(allterms.items() + doctfidf.items())

    return documents, allterms

# term musi zawierac liste wszystkich termow wraz z liczba wystapien !!!
# Tylko 2000 najczesciej wystepujacych wyrazow !!!

def cluster(documents, terms):
    logging.info("Performing clustering procedure")

    order = sorted(terms.iteritems(), key = lambda x: x[1])[:2000]

    print order

    """
    vectors = []
    sortedterms = {}

    for key, doc in documents.iteritems():
        vectors[len(vectors):] = [ numpy.array([ doc['tfidf'][o[0]] for o in order ]) ]  # posortowane alfabetycznie termy do numpy.array'a

    clusterer = KMeansClusterer(4, euclidean_distance)
    clusters  = clusterer.cluster(vectors, True, trace = False)

    print clusters
    """

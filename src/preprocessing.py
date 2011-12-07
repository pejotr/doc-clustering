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

        print term + " : " + str(len(occ)) 

        val = document['tf'].freq(term) * math.log10( d / len(occ) )
        tfidf[term] = val

    return tfidf

def evaluate_html():
    pass

def process_documents(path):
    logging.info("Using documents from \"" + path + "\" directory ")
    
    if path[-1] != "/" :
        path + "/"

    documents = {}
    allterms  = {}
    stemmer   = PorterStemmer()
    listing   = os.listdir(path)
    allfreq   = FreqDist()

    # retriving document content - discarding structure
    logging.info("Processing files...")
    for infile in listing:
        logging.info("\tReading document " + infile)
        raw_doc    = nltk.clean_html(open(path + infile, 'r').read())
        #raw_doc    = open(path + infile, 'r').read()
        word_list  = nltk.word_tokenize(re.sub('[^A-Za-z0-9 ]', ' ', raw_doc))
        terms_list = [ x.lower() for x in word_list if x.lower() not in stopwords.words('english')]

        stemmes = []
        logging.info("\tStemming words...")
        for term in terms_list :
            stemmes[len(stemmes):] = [stemmer.stem(term)]
            allterms[stemmer.stem(term)] = 0

        fdist = FreqDist(word.lower() for word in stemmes)
        allfreq.update(word.lower() for word in stemmes)
    
        documents[infile] = { 'docname': infile,  'terms': stemmes, 'tf': fdist, 'tfidf': None  }

    for key, doc in documents.iteritems():
        doctfidf = compute_tfidf(doc ,documents)
        documents[key]['tfidf'] = dict(allterms.items() + doctfidf.items())

    return documents, allfreq

def cluster(documents, terms, mostfreq = 2000):
    logging.info("Performing clustering procedure")

    order = [ x[0] for x in terms.items()[:mostfreq] ]

    vectors = []
    docnames = []

    for key, doc in documents.iteritems():
        logging.info("Creating documnet vector for " + key )
        vectors[len(vectors):] = [ numpy.array([ doc['tfidf'][o] for o in order ]) ]  # posortowane alfabetycznie termy do numpy.array'a
        docnames[len(docnames):] = [key]

    clusterer = KMeansClusterer(7, euclidean_distance)
    clusters  = clusterer.cluster(vectors, True, trace = False)

    for i in range(len(clusters)) :
        print "[" + docnames[i] + "] -> " + str(clusters[i])

    print clusters

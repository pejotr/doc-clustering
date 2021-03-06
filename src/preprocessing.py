import os
import logging
import re
import math
import lxml

import numpy
import nltk

from lxml import etree
from nltk.cluster import *
from nltk.tokenize import *
from nltk.cluster.util import *
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.probability import FreqDist

from Bio.Cluster import *

DEF_HTML_USE_TAGS      = False
DEF_HTML_TITLE_WEIGHT  = 1 
DEF_HTML_H1_WEIGHT     = 1 
DEF_TOP_FREQ_TERMS     = 2000
DEF_GROUP_CNT          = 3

DEF_REPEATS            = 20

DEF_USE_EUCLIDEAN      = 'e' 
DEF_USE_CORRELATION    = 'c'
DEF_USE_ABSCORRELATION = 'a'
DEF_USE_UNCCORRELATION = 'u'
DEF_USE_SPEARMAN       = 's'
DEF_USE_KENDALL        = 'k'
DEF_USE_MANHATTAN      = 'b'

DEF_USE_ARITHMETIC     = 'a'
DEF_USE_MEDIAN         = 'm'

def compute_tfidf(document, documents):
    logging.info("Computing tfidf values for document: " + document['docname'])

    tfidf = {}
    d = len(documents)

    for term in document['terms']:
        occ = [ x for x, y in documents.iteritems() if y['tf'][term] > 0 ]
        val = document['tf'].freq(term) * math.log10( d / len(occ) )
        tfidf[term] = val

    return tfidf

def evaluate_html(content, html_conf):
    fdist = FreqDist()
    if html_conf['usehtml'] == False:
        logging.info('Discarding HTML tags')
        return fdist
 
    logging.info("\tEvaluating HTML")
     
    # try with TITLE tag
    titles = re.findall("<title>[A-Za-z0-9 ]+</title>", content)
    for title in titles:
        root = etree.fromstring(title)
        words_list = nltk.word_tokenize(re.sub('[^A-Za-z0-9 ]', ' ', root.text))
        terms_list = [ x for x in words_list if x.lower() not in stopwords.words('english')]
        stems = steming(terms_list)

        for i in range(html_conf['title']):
            fdist.update(stems)

    # try with H1 tag
    headers = re.findall("<h1>[A-Za-z0-9 ]+</h1>", content)
    for header in headers:
        root = etree.fromstring(header)
        words_list = nltk.word_tokenize(re.sub('[^A-Za-z0-9 ]', ' ', root.text))
        terms_list = [ x for x in words_list if x.lower() not in stopwords.words('english')]
        stems = steming(terms_list)

        for i in range(html_conf['h1']):
            fdist.update(stems)

    return fdist

def steming(terms) :
    stemmer = PorterStemmer()
    stemmes = []
    logging.info("\tStemming words...")

    for term in terms :
        stemmes[len(stemmes):] = [stemmer.stem(term)]

    return stemmes

def process_documents(path, html_conf):
    logging.info("Using documents from \"" + path + "\" directory ")
    
    if path[-1] != "/" :
        path + "/"

    documents = {}
    allterms  = {}
    listing   = os.listdir(path)
    allfreq   = FreqDist()

    # retriving document content - discarding structure
    logging.info("Processing files...")
    for infile in listing:
        logging.info("\tReading document " + infile)
        raw_doc     = open(path + infile, 'r').read()
        nonhtml_doc = nltk.clean_html(raw_doc)
        word_list   = nltk.word_tokenize(re.sub('[^A-Za-z0-9 ]', ' ', raw_doc))
        terms_list  = [ x.lower() for x in word_list if x.lower() not in stopwords.words('english')]

        stemmes = steming(terms_list)

        for stem in stemmes :
            allterms[stem] = 0

        fdist = FreqDist(word.lower() for word in stemmes)
        allfreq.update(word.lower() for word in stemmes)

        htmldist = evaluate_html(raw_doc.lower(), html_conf)
        fdist.update(htmldist)
        allfreq.update(htmldist)
    
        documents[infile] = { 'docname': infile,  'terms': stemmes, 'tf': fdist, 'tfidf': None  }

    for key, doc in documents.iteritems():
        doctfidf = compute_tfidf(doc ,documents)
        documents[key]['tfidf'] = dict(allterms.items() + doctfidf.items())

    return documents, allfreq

def cluster(documents, terms, mostfreq, groups, distfun, repeats, centrfun ):
    logging.info("Performing clustering procedure")

    order = [ x[0] for x in terms.items()[:mostfreq] ]

    vectors = []
    docnames = []

    for key, doc in documents.iteritems():
        logging.info("Creating documnet vector for " + key )
        vectors[len(vectors):] = [ [ doc['tfidf'][o] for o in order ] ]  # posortowane alfabetycznie termy do numpy.array'a
        docnames[len(docnames):] = [key]

    clusters, error, nfound = kcluster(vectors, nclusters=groups, dist=distfun, npass=repeats, method=centrfun)

    clustering_result = zip(docnames, clusters)
    return clustering_result



import sys
import logging
import getopt
import preprocessing

DEF_HTML_USE_TAGS      = True
DEF_HTML_TITLE_WEIGHT  = 5 
DEF_HTML_H1_WEIGHT     = 2 
DEF_TOP_FREQ_TERMS    = 2000

def usage():
    pass

def main(argv):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    opts, extraparams = getopt.getopt(argv[1:])

    html_use_tags     = DEF_HTML_USE_TAGS
    html_title_weight = DEF_HTML_TITLE_WEIGHT
    html_h1_weight    = DEF_H1_HEADER_WEIGHT
    top_freq_terms    = DEF_TOP_FREQ_TERMS

    for o,p in opts :
        if   o in ['--nohtml'] :
            html_use_tags = False 
        elif o in ['--title']  :
            html_title_weight = p
        elif o in ['--h1']     : 
            html_h1_weight = p
        elif o in ['--freq']   :
            top_freq_terms = p

    html_conf = {'usehtml': html_use_tags, 'title': html_title_weight, 'h1': html_h1_weight}

    docs, terms = preprocessing.process_documents(argv[0], html_conf)
    preprocessing.cluster(docs, terms)

if __name__ == "__main__" :
    main(sys.argv[1:])

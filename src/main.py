import sys
import logging
import getopt
import preprocessing

DEF_HTML_USE_TAGS      = True
DEF_HTML_TITLE_WEIGHT  = 5 
DEF_HTML_H1_WEIGHT     = 2 
DEF_TOP_FREQ_TERMS     = 2000
DEF_GROUP_CNT          = 3
DEF_USE_COSINE         = False
DEF_REPEATS            = 20

def usage():
    pass

def main(argv):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    print argv[1:]
    opts, extraparams = getopt.getopt(argv[1:], "",['nohtml', 'cosine', 'title=', 'h1=', 'freq=', 'groups=', 'repeats='])


    html_use_tags     = DEF_HTML_USE_TAGS
    html_title_weight = DEF_HTML_TITLE_WEIGHT
    html_h1_weight    = DEF_HTML_H1_WEIGHT
    top_freq_terms    = DEF_TOP_FREQ_TERMS
    group_cnt         = DEF_GROUP_CNT
    use_cosine        = DEF_USE_COSINE

    for o,p in opts :
        if   o in ['--nohtml'] :
            html_use_tags = False 
        elif o in ['--title']  :
            html_title_weight = int(p)
        elif o in ['--h1']     : 
            html_h1_weight = int(p)
        elif o in ['--freq']   :
            top_freq_terms = p
        elif o in ['--groups'] :
            group_cnt = int(p)
        elif o in ['--cosine'] :  
            use_cosine = True
        elif o in ['--repeats'] :
            repeats = int(p)
            
            

    html_conf = {'usehtml': html_use_tags, 'title': html_title_weight, 'h1': html_h1_weight}

    docs, terms = preprocessing.process_documents(argv[0], html_conf)
    result = preprocessing.cluster(docs, terms, top_freq_terms, group_cnt, use_cosine, repeats)
    
    r = sorted(result, key = lambda i: i[0])
    print "\n".join( v[0] + ", " + str(v[1]) for v in r)


if __name__ == "__main__" :
    main(sys.argv[1:])

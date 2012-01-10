import sys
import logging
import preprocessing
import argparse

DEF_HTML_USE_TAGS      = False
DEF_HTML_TITLE_WEIGHT  = 1 
DEF_HTML_H1_WEIGHT     = 1 
DEF_TOP_FREQ_TERMS     = 2000
DEF_GROUP_CNT          = 3
DEF_USE_COSINE         = False
DEF_REPEATS            = 20

def main(argv):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    parser = argparse.ArgumentParser(description='Cluster given HTML and plaintext documents.')
    parser.add_argument('datadir', metavar='datadir', help='directory where documents for clustering are stored')

    parser.add_argument('--usehtml', dest='html_use_tags', action='store_true', default=DEF_HTML_USE_TAGS,
                       help='use HMTL tags for text analysis (default: false)')

    parser.add_argument('--cosine', dest='use_cosine', action='store_true', default=DEF_USE_COSINE, 
                       help='use cosine similarity instead of euclidean (default: false)')

    parser.add_argument('--title', dest='html_title_weight', action='store', type=int, default=DEF_HTML_TITLE_WEIGHT, 
                       help='title weight (default: 1)')

    parser.add_argument('--h1', dest='html_h1_weight', action='store', type=int, default=DEF_HTML_TITLE_WEIGHT, 
                       help='title weight (default: 1)')

    parser.add_argument('--freq', dest='top_freq_terms', action='store', type=int, default=DEF_TOP_FREQ_TERMS, 
                       help='number of top fequent terms for clustering (default: 2000)')
    
    parser.add_argument('--groups', dest='group_cnt', action='store', type=int, default=DEF_GROUP_CNT, 
                       help='number of groups (default: 3)')

    parser.add_argument('--repeats', dest='repeats', action='store', type=int, default=DEF_REPEATS, 
                       help='repeats in KMeans algorithm (default: 20)')

    args = parser.parse_args()
    html_use_tags     = args.html_use_tags
    html_title_weight = args.html_title_weight
    html_h1_weight    = args.html_h1_weight
    top_freq_terms    = args.top_freq_terms
    group_cnt         = args.group_cnt
    use_cosine        = args.use_cosine
    repeats           = args.repeats

    html_conf = {'usehtml': html_use_tags, 'title': html_title_weight, 'h1': html_h1_weight}

    docs, terms = preprocessing.process_documents(argv[0], html_conf)
    result = preprocessing.cluster(docs, terms, top_freq_terms, group_cnt, use_cosine, repeats)
    
    r = sorted(result, key = lambda i: i[0])
    print "\n".join( v[0] + ", " + str(v[1]) for v in r)


if __name__ == "__main__" :
    main(sys.argv[1:])

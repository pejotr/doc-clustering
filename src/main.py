import sys
import logging
import preprocessing
import argparse

def main(argv):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    parser = argparse.ArgumentParser(description='Cluster given HTML and plaintext documents.')
    parser.add_argument('datadir', metavar='datadir', help='directory where documents for clustering are stored')

    parser.add_argument('--usehtml', dest='html_use_tags', action='store_true', default=DEF_HTML_USE_TAGS,
                       help='use HMTL tags for text analysis (default: false)')

    # { ------- DISTANCE FUNCTION SETUP
    dist_group = parser.add_mutually_exclusive_group(required=True)
    dist_group.add_argument('--euclidean', dest='sim_fun', action='store_const', const=preprocessing.DEF_USE_CORRELATION, 
                       help='use euclidean similarity')

    dist_group.add_argument('--correlation', dest='sim_fun', action='store_const', const=preprocessing.DEF_USE_CORRELATION, 
                       help='use correlation similarity')
    
    dist_group.add_argument('--abscorrelation', dest='sim_fun', action='store_const', const=preprocessing.DEF_USE_ABSCORRELATION, 
                       help='use abscorrelation similarity')

    dist_group.add_argument('--unccorrelation', dest='sim_fun', action='store_const', const=preprocessing.DEF_USE_UNCCORRELATION, 
                       help='use uncentered correlation similarity')

    dist_group.add_argument('--spearman', dest='sim_fun', action='store_const', const=preprocessing.DEF_USE_SPEARMAN, 
                       help='use Spearman\'s similarity')
    
    dist_group.add_argument('--kendall', dest='sim_fun', action='store_const', const=preprocessing.DEF_USE_KENDALL, 
                       help='use Kendall\'s similarity')

    dist_group.add_argument('--manhattan', dest='sim_fun', action='store_const', const=preprocessing.DEF_USE_MANHATTAN, 
                       help='use Manhattan similarity')

    # DISTANCE FUNCTION SETUP ------- }

    # { ------- CLUSTER CENTER METHOD
    method_group = parser.add_mutually_exclusive_group(required=True)
    method_group.add_argument('--arithmetic', dest='center_method', action='store_const', const=preprocessing.DEF_USE_ARITHMETIC, 
                       help='use arithmetic mean to find cluster center')

    method_group.add_argument('--median', dest='center_method', action='store_const', const=preprocessing.DEF_USE_MEDIAN, 
                       help='use median to find cluster center')
    # CLUSTER CENTER METHOD ------- }

    parser.add_argument('--title', dest='html_title_weight', action='store', type=int, default=preprocessing.DEF_HTML_TITLE_WEIGHT, 
                       help='title weight (default: 1)')

    parser.add_argument('--h1', dest='html_h1_weight', action='store', type=int, default=preprocessing.DEF_HTML_TITLE_WEIGHT, 
                       help='title weight (default: 1)')

    parser.add_argument('--freq', dest='top_freq_terms', action='store', type=int, default=preprocessing.DEF_TOP_FREQ_TERMS, 
                       help='number of top fequent terms for clustering (default: 2000)')
    
    parser.add_argument('--groups', dest='group_cnt', action='store', type=int, default=preprocessing.DEF_GROUP_CNT, 
                       help='number of groups (default: 3)')

    parser.add_argument('--repeats', dest='repeats', action='store', type=int, default=preprocessing.DEF_REPEATS, 
                       help='repeats in KMeans algorithm (default: 20)')

    args = parser.parse_args()
    html_use_tags     = args.html_use_tags
    html_title_weight = args.html_title_weight
    html_h1_weight    = args.html_h1_weight
    top_freq_terms    = args.top_freq_terms
    group_cnt         = args.group_cnt
    repeats           = args.repeats
    use_simfun        = args.sim_fun
    center_method     = args.center_method

    html_conf = {'usehtml': html_use_tags, 'title': html_title_weight, 'h1': html_h1_weight}

    docs, terms = preprocessing.process_documents(argv[0], html_conf)
    result = preprocessing.cluster(docs, terms, top_freq_terms, group_cnt, use_simfun, repeats, center_method)
    
    r = sorted(result, key = lambda i: i[0])
    print "\n".join( v[0] + ", " + str(v[1]) for v in r)


if __name__ == "__main__" :
    main(sys.argv[1:])

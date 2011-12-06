import sys
import logging
import preprocessing

def usage():
    pass

def main(argv):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


    docs, terms = preprocessing.process_documents(argv[0])
    preprocessing.cluster(docs, terms)

if __name__ == "__main__" :
    main(sys.argv[1:])

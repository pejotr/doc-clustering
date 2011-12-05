import sys
import logging
import preprocessing

def usage():
    pass

def main(argv):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    preprocessing.process_documents(argv[0])

if __name__ == "__main__" :
    main(sys.argv[1:])

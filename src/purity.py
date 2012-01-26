import re
import math
import operator


def purity(clustering_res, groups) :

    classify = {}

    for i in range(0,groups) :
        classify[i] = {} 

    for doc in clustering_res :
        m = re.search("[A-Za-z]+", doc[0])
        docclass = m.group(0)

        if docclass in classify[doc[1]] :
            classify[doc[1]][docclass] = classify[doc[1]][docclass] + 1
        else:
            classify[doc[1]][docclass] = 1


    print classify
    
    suma = 0
    for i in range(0, len(classify)) :
        c = max(classify[i].iteritems(), key = operator.itemgetter(1))[1]
        suma = suma + c 


    print suma
    print float(suma) / float(len(clustering_res))
    

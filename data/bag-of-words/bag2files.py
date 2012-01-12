
if __name__ == "__main__" :


    # reading vocabfile
    vocab = open("vocab.nips.txt", "r")
    content = vocab.readlines()

    words = []
    for line in content :
        word = line.strip('\n')
        words.append(word)


    # reading docword file
    docword = open("docword.nips.mini.txt", "r")
    content = docword.readlines()
    

    nnz = content[3:]
    for line  in nnz :
        triple = line.strip('\n').split(" ")
        print triple

        # not so smart but opening all files at beginig either :)   
        destfile = open("files/file" + triple[0], "w+")

        for i in range(0, int(triple[2])) :
            destfile.write(words[int(triple[1]) - 1] + " \n")

        destfile.close()
        


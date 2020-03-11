import os
from bs4 import BeautifulSoup
import re
import csv
import operator
import timeit
import math

numOfDocs = 0
docFreq = {}
tf = {}


def calc_weight(word):
    idf = math.log(numOfDocs / docFreq[word])
    return tf * idf


if __name__ == '__main__':
    # start timer
    # start = timeit.default_timer()
    print('what the')
    files = os.listdir("html_files")

    # get term frequency, number of files, and doc frequency of each word
    for x in files:
        wordCount = {}
        numOfDocs += 1

        currFile = "html_files/" + x

        # opens file and strips html
        file = open(currFile)
        soup = BeautifulSoup(file.read(), "html.parser")
        file.close()
        justText = soup.get_text()
        cleanString = re.sub('\W+', ' ', justText)

        newFile = os.path.splitext(x)[0]

        for y in cleanString.lower().split():
            if y.isnumeric():
                continue
            if y in wordCount:
                # Increment count of word by 1
                wordCount[y] = wordCount[y] + 1
            else:
                # Add the word to dictionary with count 1
                wordCount[y] = 1
                # add to total doc frequency only once per document
                if y in docFreq:
                    docFreq[y] = docFreq[y] + 1
                else:
                    docFreq[y] = 1

        # add term frequency of current file to dictionary of all tf dictionaries
        tf[newFile] = wordCount

    print(docFreq['the'])

    # print(timeit.default_timer() - start)

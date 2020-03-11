import os
from bs4 import BeautifulSoup
import re
import csv
import timeit
import math

numOfDocs = 0
docFreq = {}
tf = {}
l1 = []


def calc_weight(word, freq):
    idf = math.log(float(numOfDocs) / float(docFreq[word]))
    return float(freq) * float(idf)


if __name__ == '__main__':
    # start timer
    start = timeit.default_timer()
    stop_file = open('stopwords.txt', 'r')
    for line in stop_file.readlines():
        for i in line.split('\n'):
            l1.append(i)
    stop_file.close()

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

        for k, v in list(wordCount.items()):
            if v == 1:
                del wordCount[k]
        for k, v in list(wordCount.items()):
            if k in l1:
                del wordCount[k]
        for k, v in list(wordCount.items()):
            if len(k) == 1:
                del wordCount[k]

        # add term frequency of current file to dictionary of all tf dictionaries
        tf[newFile] = wordCount

    # loop through dic of tf dic and create doc weights
    for t in tf:
        weights = {}

        # only look at current tf
        name = t
        curr = tf[t]

        # calc weight of each word in each doc
        for x in curr:
            weights[x] = calc_weight(x, curr[x])

        csv_file = name + '.csv'
        create = "output/" + csv_file
        os.makedirs(os.path.dirname(create), exist_ok=True)
        w = csv.writer(open(create, "w"))
        for key, val in weights.items():
            w.writerow([key, val])

    print(timeit.default_timer() - start)

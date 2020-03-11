import os
from bs4 import BeautifulSoup
import re
import csv
import operator
import timeit

def sort_dict_by_key(unsorted_dict):
    sorted_keys = sorted(unsorted_dict.keys(), key=lambda x: x.lower())

    sorted_dict = {}
    for key in sorted_keys:
        sorted_dict.update({key: unsorted_dict[key]})

    return sorted_dict


if __name__ == '__main__':
    #start timer
    start = timeit.default_timer()

    files = os.listdir("html_files")
    numOfFiles = len(files)
    wordList = dict()
    numbers = '0123456789'

    #counter is for calculating different times for different number of files
    # counter = 0
    for x in files:
        # counter += 1
        currFile = "html_files/" + x

        # opens file and stripes html
        file = open(currFile)
        soup = BeautifulSoup(file.read(), "html.parser")
        file.close()
        justText = soup.get_text()
        cleanString = re.sub('\W+', ' ', justText)

        newFile = os.path.splitext(x)[0]
        # writes to txt file
        create = "text_files/" + newFile + ".txt"
        os.makedirs(os.path.dirname(create), exist_ok=True)
        with open(create, "w") as f:
            f.write(justText)
        f.close()

        for y in cleanString.lower().split():
            if (y.isnumeric()):
                continue
            if y in wordList:
                # Increment count of word by 1
                wordList[y] = wordList[y] + 1
            else:
                # Add the word to dictionary with count 1
                wordList[y] = 1
        # if counter == 250:
        #     break

    sortedNum = dict(sorted(wordList.items(), key=operator.itemgetter(1), reverse=True))
    w = csv.writer(open("quantity.csv", "w"))
    for key, val in sortedNum.items():
        w.writerow([key, val])

    sortedAlpha = sort_dict_by_key(wordList)
    z = csv.writer(open("alphabetical.csv", "w"))
    for key, val in sortedAlpha.items():
        z.writerow([key, val])

    print(timeit.default_timer()-start)
import sys
import re

from pyspark import SparkContext

def flatMapFunc(document):
    """
    Takes in document, which is a key, value pair, where document[0] is the
    document ID and document[1] is the contents of the document.
    HINT: You need to keep track of three things, word, document ID, and the
    index inside of the document, but you are working with key, value pairs.
    Is there a way to combine these three things and make a key, value pair?
    """
    x =  re.findall(r"\w+", document[1])
    m = []
    for i in range(0, len(x)):
        m.append(((str(x[i])), i))
    return m

def mapFunc(arg):
    """ Your code here. """
    return (arg[0], arg[1])

def reduceFunc(arg1, arg2):
    """ Your code here. """
    return str(arg1) + " " +  str(arg2)

def index(file_name, output="spark-wc-out-index"):
    sc = SparkContext("local[8]", "Index")
    file = sc.sequenceFile(file_name)

    indices = file.flatMap(flatMapFunc) \
                  .map(mapFunc) \
                  .reduceByKey(reduceFunc)

    indices.coalesce(1).saveAsTextFile(output)

""" Do not worry about this """
if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 2:
        index(argv[1])
    else:
        index(argv[1], argv[2])
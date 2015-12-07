# loadTrec.py
# Example of loading the TREC SPAM dataset (including the gold annotations), doing very simple preprocessing, and
#  converting each message to a vector format.

import math
import string
import re
from collections import Counter

# Filenames
# filenameIndex = "E:\\trec_data\\trec07p\\partial\\index"
# filenameMessagePrefix = "E:\\trec_data\\trec07p\\data\\inmail."
filenameIndex = 'goldData\index.txt'
filenameMessagePrefix = 'data\inmail.'

# Maximum messages to load
MAX_MESSAGES = 3000

# Defines
SPAM_MESSAGE = 1
NORMAL_MESSAGE = 2

# These three lists contain the central data for each message -- the original text, a vector representing that text, and the gold annotations.
# List of original text
messageText = []

# List of vectors
messageVecs = []

# List of gold data (i.e. whether a message is spam or normal)
messageGold = []


#
# Functions supporting loading in the TREC dataset
#

# filename: name of TREC index file
# maxNum: Maximum number of elements to read (e.g. 3000).  If it's zero, read in the whole index.
# returns: list of whether each item is spam or ham
def loadGoldIndex(filename, maxNum):
    fp = open(filename, 'r')
    goldOut = []

    count = 0
    for line in fp:
        split = line.lower().split()
        if (split[0] == "spam"):
            goldOut.append(SPAM_MESSAGE)
        else:
            goldOut.append(NORMAL_MESSAGE)

        count += 1
        if (maxNum > 0) and (count >= maxNum):
            fp.close()
            return goldOut

    fp.close()
    return goldOut


# filename: filename of message
# returns: string, with header stripped
def loadMessage(filename):
    fp = open(filename, 'r')
    stringIn = ""

    isHeader = 1
    for line in fp:
        if (isHeader == 0):
            stringIn += line

        # Check to see if the header has ended
        if (isHeader == 1) and (len(line) < 2):
            isHeader = 0

    # Make it easier to segment or filter HTML tags
    stringIn = stringIn.replace("<", " <")
    stringIn = stringIn.replace(">", "> ")

    # Optional: Strip HTML (from StackOverflow)
    stringIn = re.sub('<[^<]+?>', '', stringIn)

    # Optional: Collapse whitespaces to single whitespace
    stringIn = re.sub('\s+', ' ', stringIn)

    # Optional Add more preprocessing / filtering...
    # ...

    # print ("stringIn: " + stringIn)
    fp.close()
    return stringIn


def loadMessages(filenamePrefix, maxNum):
    text = []
    vecs = []

    print (" * loadMessages: Started... (this may take a moment) ")

    for i in range(1, maxNum + 1):
        filename = filenamePrefix + str(i)
        msgText = loadMessage(filename)
        text.append(msgText)
        vecs.append(text2vec(msgText))

        # Progress bar for long loads
        if (i % 500 == 0):
            print (" * loadMessages: at " + str(i) + " messages... ")

    print (" * loadMessages: Complete...  (loaded " + str(len(text)) + " messages) ")

    # Return
    return (text, vecs)


#
# IR Vector Functions
#

# Cosine simularity
# input: vec1, vec2: Counters representing word vectors.
#  These vectors must be unit length (i.e. normalized) before hand.
# returns: cosine similarity of vec1 and vec2
def cosine(vec1, vec2):
    return dotProduct(vec1, vec2)


# Dot Product
def dotProduct(vec1, vec2):
    runningSum = float(0.0)
    for key in vec1:
        value1 = vec1[key]
        value2 = vec2[key]
        prod = float(value1) * float(value2)
        runningSum += prod

    return runningSum


# Calculate Length
def vecLength(vec):
    runningSum = float(0.0)
    for key in vec:
        exp = vec[key] ** 2
        runningSum += exp

    length = math.sqrt(runningSum)
    return length


# Normalize
def normalize(vec):
    length = vecLength(vec)
    for key in vec:
        vec[key] = vec[key] / length


#
# Supporting Functions (IR)
#

# Input: string of text.  Can be a single word, sentence, or series of sentences.
#  Note: Automatically strips punctuation, and converts to lower case
# Output: normalized vector (counter), representing stringIn.
def text2vec(stringIn):
    # Remove punctuation
    filteredString1 = stringIn.translate(string.maketrans("", ""), string.punctuation)

    # Convert to lower-case
    filteredString2 = filteredString1.lower()

    # split
    words = filteredString2.split()

    # Convert to vector
    outVec = Counter()
    for word in words:
        outVec[word] += 1

    # Automatically normalize
    normalize(outVec)

    # Return
    return outVec


'''
#
# Main Program
#

# Load gold data
messageGold = loadGoldIndex(filenameIndex, MAX_MESSAGES)

# Load message text and IR vectors
(messageText, messageVecs) = loadMessages(filenameMessagePrefix, MAX_MESSAGES)

# Example showing how to use the data, for the first 10 messages
print ("\n\n")

for i in range(0, 10):
    print ("Message " + str(i + 1))
    print ("Class: " + str(messageGold[i]))
    print ("Text: " + messageText[i])
    print ("Vector: " + str(messageVecs[i]))

    print ("Cosine Similarities with other messages: ")
    for j in range(0, 10):
        print(str(j + 1) + ": %.4f  " % cosine(messageVecs[i], messageVecs[j])),

    print ("")
    print ("")
'''

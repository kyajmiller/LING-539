# Information Retrieval (IR) Vector example

import string
import math
from collections import Counter


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
# Supporting Functions
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


#
# Main Program
#

# Example from Lecture 23, Slide 15
sampleVec1 = text2vec("The man said that a space age man appeared")
sampleVec2 = text2vec("Those men appeared to say their age")
sampleVec3 = text2vec("This is, a test! of punctuation -- removal!")

print sampleVec1
print sampleVec2
print sampleVec3
print ("")

# Cosine similarity
print ("cos (vec1, vec2): " + str(cosine(sampleVec1, sampleVec2)))
print ("cos (vec1, vec3): " + str(cosine(sampleVec1, sampleVec3)))
print ("cos (vec2, vec3): " + str(cosine(sampleVec2, sampleVec3)))

# Cosine similarity of a vector and itself
print ("cos (vec1, vec1): " + str(cosine(sampleVec1, sampleVec1)))

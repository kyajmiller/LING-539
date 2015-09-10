__author__ = 'Kya'
from nltk.book import *
from pylab import *

maxLength = 20
lengths = arange(1, maxLength+1, 1)
counts = [0] * maxLength
wordLengths = [len(w) for w in text1]

#count
for len in wordLengths:
    safeLen = len
    if safeLen > maxLength:
        safeLen = maxLength - 1
    counts[safeLen-1] += 1

#plot
bar(lengths, counts)
xlabel("Word Lengths")
ylabel("Counts")
grid(True)
show()

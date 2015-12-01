'''
gender classifier, lecture code
see chapter 6 in book
name/gender classifier
Kya --> Female, Peter --> Male
'''
import nltk
from nltk.corpus import names
import random


def gender_features(name):
    features = {}
    features['lastLetter'] = name[-1]
    return features


features = gender_features('peter')
print features

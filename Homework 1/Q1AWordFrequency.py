__author__ = 'Kya'

brownTagNoLines = open('browntag_nolines.txt', 'r')
brownTagNoLines = brownTagNoLines.read()

tokensPOSTagged = brownTagNoLines.split(' ')
print(tokensPOSTagged[0])

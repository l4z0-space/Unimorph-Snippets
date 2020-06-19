

# 0.a) declare the dictonray to map labels to features and features to dimensions -> findFeature={}, findDimension={}
# 0.b) read the file (Appendix) and map each label to its feature and dimension


# 1.a) create the class (for each word/row)
# 1.b) create a list of objects (words) -> allWords=[]

# 2) read from the file
    # 2.a) for each line
        # keep a dict of current line features & dimensions -> currentDimensions={}
        # 2.b) take the 3rd (last) block of words (semicolon separated)
            # 2.c) for each 3rd block of words
                # 2.d) for each of the labels
                    # 2.e) map label to its feature (0.b) and add (label:feature) and (feature:dimension) to currentDimensions

        # create object for the current word and add it to allWords (1.b)

#
# sample line from words-> megadose	megadoses	V;3;SG;PRS
# third block of words -> V;3;SG;PRS
# for example, take first label -> V
#   from (0.a) and (2.e) ->  findFeature[V] = Verb and findDimension[Verb] = Part of Speech
#   so far
#    allWords = {
#                megadose: {
#                          Part of Speech=[Verb], (V)
#                          Person=[3], (3)
#                          Number=[Singular], (SG)
#                          Tense=[Present] (PRS)
#                             }
#               }
#
# 3) once all the words/rows along with their features are in the allWords (1.b) list
# we are ready to ?migrate? the data in the database

from collections import defaultdict
import json


# Dictionaries for finding features and dimensions
findFeature={}
findDimension={}



class Word:
    def __init__(self,wordContent,rootWord,language,availableDimensions,dimensions):
        self.wordContent = wordContent
        self.rootWord = rootWord
        self.language = language
        self.availableDimensions = availableDimensions
        self.dimensions = dimensions


    def json(self):
        word_dict={
        "wordContent": self.wordContent,
        "rootWord": self.rootWord,
        "language": self.language,
        "dimensions":self.dimensions
        }
        return word_dict

    def showDimensions(self):
        print(f"{self.wordContent} | root: {self.rootWord}")

        for aD in self.availableDimensions:
            print(f" > {aD}: {self.dimensions[aD]}")
        print("\n")


# ALL THE WORD OBJECT WILL BE STORED HERE
allWords=[]

def readAppendix():
    fileContent = open("wordFiles/appendix.txt","r")
    for row in fileContent:
        rowWords = row.split(";");
        dimension = rowWords[0]
        feature = rowWords[1]
        label =(rowWords[2].rstrip()).upper()
        findFeature[label]=feature # assign feature to label
        findDimension[feature]=dimension # assign dimension to feature
    fileContent.close()

    # Parsing below...
# parse the each line of words files
def parseLine(line):
    rowContent = line.split();

    if(len(rowContent)>=3): # checks if line is valid
        rootWord = rowContent[0]
        currWordList = rowContent[1:-1] # it can be more than a single words

        currWord = ""
        for temp in currWordList:
            currWord += temp + " "
        currWord = currWord[:-1] # remove last space

        allDimensions = defaultdict(list) # make this a dictionary mapping to lists (dimension can have multiple features)
        availableDimensions=[]


        allLabels = rowContent[-1].split(";") # last block of words corrensponds to allLabels

        for currLabel in allLabels: # assign feature and dimension of current label
            try:
                currFeature = findFeature[currLabel.upper()]
                currDimension = findDimension[currFeature] # find the dimension

                if currDimension not in availableDimensions:
                    availableDimensions.append(currDimension) # add to available dimensions

                allDimensions[currDimension].append(currFeature)  # map the dimension

            except KeyError:
                print(f"{currLabel} label doesn't exist.")

        wordObject  = Word(currWord,rootWord,'English',availableDimensions,allDimensions)

        allWords.append(wordObject)


def importLanguage():
    wordContent = open("wordFiles/english.txt","r")
    it=0

    for x in wordContent:
        parseLine(x)
        if it==100:
            break
        it+=1
    wordContent.close()


allJSON =[]

readAppendix()
importLanguage()


for word in allWords:
    #word.showDimensions()
    allJSON.append(word.json())

# migrate to the database


# print(len(allWords))

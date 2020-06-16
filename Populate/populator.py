import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","eureka.settings.development")
django.setup()

from django.contrib.auth.models import User
from django.contrib import admin
from wordDictionary.models import Genus, Word, Feature, Dimension, Language, Lemma, Family, TagSet, POS


# Dimensions
def dimensionPop():
    with open("data/models/dimensions.txt","r") as dimData:
        for x in dimData:
            a = x.split("\n")
            dimName = a[0]
            # Create Object
            nextDim = Dimension(name=dimName)
            nextDim.save()
    print("Dimension done")


# Features
def featurePop():
    with open("data/models/features.txt","r") as featData:
        for x in featData:
            line = x.split(";")
            featName = line[1]
            dimName = line[0]
            # Create Object
            nextFeature = Feature(name=featName)
            dimObject = Dimension.objects.get(name=dimName)
            nextFeature.dimension = dimObject
            nextFeature.save()
    print("Feature done")


# Part of Speech
def posPop():
    with open("data/models/POS.txt","r") as posData:
        for x in posData:
            line = x.split(";")
            posName = line[1]
            # Create Object
            nextPOS = POS(name=posName)
            nextPOS.save()
    print("Part of Speech done")


# Genus
def genusPop():
    with open("data/models/genus.txt","r") as genusData:
        for x in genusData:
            genusName = x.split("\n")[0]
            # Create Object
            nextGenus = Genus(name=genusName)
            nextGenus.save()
    print("Genus done")


# Family
def familyPop():

    with open("data/models/families.txt","r") as famData:
        for x in famData:
            FamilyName = x.split(";")[0]
            # Create Object
            nextFamily = Family(name=FamilyName)
            nextFamily.save()
    print("Family done")


def languagePop():
    # pass
    nextLang = Language(name="English")
    nextLang.walsCode = "bul"
    nextLang.genus = Genus.objects.get(name="Germanic")
    nextLang.family = Family.objects.get(name="Indo-European")
    nextLang.save()
    print("Language done")




def lemmaPop():
    with open("data/models/lemmas.txt","r",encoding="utf8") as lemmaData:
        it = 0
        for x in lemmaData:
            it += 1
            if it % 100 == 0:
                break
            x = x.split("\n")
            lemmaName = x[0]
            nextLemma = Lemma(name=lemmaName)
            langName = Language.objects.get(name="English")
            nextLemma.language = langName
            posName = POS.objects.get(name="Verb")
            nextLemma.pos = posName
            nextLemma.save()
    print("Lemma done")


findFeature={}
def readAppendix():
    with open("data/models/features.txt","r") as fileContent:

        for row in fileContent:
            rowWords = row.split(";")
            dimension = rowWords[0]
            feature = rowWords[1]
            label =(rowWords[2].rstrip()).upper()
            findFeature[label]=feature
    print("\nStarting with words...")


usedTagset = {}

def wordPop():

    with open("data/langs/Complete/English.txt","r",encoding="utf8") as wordData:
        it = 0
        for line in wordData:
            # To get some feedback
            it += 1
            if it % 100 == 0:
                break

            rowContent = line.split()
            if(len(rowContent)>=3): # checks if line is valid
                tagsetName = rowContent[-1]
                tagSetObject = None
                try:
                    if usedTagset[tagsetName] == 1:
                        someTagset = TagSet.objects.get(name=tagsetName)
                        tagSetObject = someTagset
                except KeyError:
                    usedTagset[tagsetName]=1
                    tagSetObject = TagSet(name=tagsetName)
                tagSetObject.save()
                lemmaName = rowContent[0]
                currWordList = rowContent[1:-1] # it can be more than a single words
                currWord = " ".join(currWordList)

                allLabels = tagsetName.split(";") # last block of words corrensponds to allLabels
                for currLabel in allLabels:
                    try:
                        currFeature = findFeature[currLabel.upper()]
                        featObject = Feature.objects.get(name=currFeature)
                        tagSetObject.features.add(featObject)
                    except KeyError:
                        print(f"{currLabel} label doesn't exist.")
            # tagSetObject.save()
            # Defining the Word/For
                wordObject = Word(name=currWord)
                lemmaObject = Lemma.objects.get(name=lemmaName)

                wordObject.lemma  = lemmaObject
                wordObject.tagset = tagSetObject
                wordObject.language = lemmaObject.language
                wordObject.save()


# *  uncomment below to populate !!in order!! *

# dimensionPop()
# featurePop()
# genusPop()
# posPop()
# familyPop()
#
# languagePop()
# lemmaPop()
#
# readAppendix()
# wordPop()


# Just in case it goes wrong

def emptyDatabase():

    Word.objects.all().delete()
    Lemma.objects.all().delete()
    TagSet.objects.all().delete()
    Language.objects.all().delete()
    Feature.objects.all().delete()
    Family.objects.all().delete()
    Dimension.objects.all().delete()
    Genus.objects.all().delete()
    POS.objects.all().delete()

    print("Database is empty...")


# emptyDatabase()

#Words.objects.to_csv("words.csv",'name','lemma')

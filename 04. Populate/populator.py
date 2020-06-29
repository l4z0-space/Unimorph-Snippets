import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","eureka.settings.development")
django.setup()

from django.contrib.auth.models import User
from django.contrib import admin
from api.models import Genus, Word, Feature, Dimension, Language, Lemma, Family, TagSet, POS


# Dimensions
def dimensionPop():
    with open("data/models/dimensions.txt","r") as dimData:
        for x in dimData:
            dimension = x.split("\n")
            # Create Object
            nextDim = Dimension(name=dimension[0])
            nextDim.save()
    print("Dimension done")


# Features
def featurePop():
    with open("data/models/features.txt","r") as featData:
        for line in featData:
            current_line = line.split(";")
            # Create Object
            nextFeature = Feature(name=current_line[1])
            dimObject = Dimension.objects.get(name=current_line[0])
            nextFeature.dimension = dimObject
            nextFeature.save()
    print("Feature done")


# Part of Speech
def posPop():
    with open("data/models/POS.txt","r") as posData:
        for line in posData:
            current_line = line.split(";")
            # Create Object
            nextPOS = POS(name=current_line[1])
            nextPOS.save()
    print("Part of Speech done")


# Genus
def genusPop():
    with open("data/models/genus.txt","r") as genusData:
        for line in genusData:
            genusName = line.split("\n")[0]
            # Create Object
            nextGenus = Genus(name=genusName)
            nextGenus.save()
    print("Genus done")


# Family
def familyPop():

    with open("data/models/families.txt","r") as famData:
        for line in famData:
            FamilyName = line.split(";")[0]
            # Create Object
            nextFamily = Family(name=FamilyName)
            nextFamily.save()
    print("Family done")


def languagePop():
    # pass
    nextLang = Language(name="Bulgarian")
    nextLang.walsCode = "bul"
    nextLang.genus = Genus.objects.get(name="Germanic")
    nextLang.family = Family.objects.get(name="Indo-European")
    nextLang.save()
    print("Language done")


def lemmaPop():
    with open("data/langs/lemmas/bulgarian.txt","r",encoding="utf8") as lemmaData:
        # it = 0
        for x in lemmaData:
            # it += 1
            # if it % 100 == 0:
            #     break
            x = x.split(",")

            lemmaName = x[0]
            POSName = x[1].split('\n')[0]

            langName = Language.objects.get(name="Bulgarian")
            posName = POS.objects.get(name=POSName)
            #print(f'{langName}, {posName}')
            nextLemma = Lemma(name=lemmaName)
            nextLemma.language = langName
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
            label = (rowWords[2].rstrip()).upper()
            findFeature[label]=feature
    print("\nStarting with words...")


def wordPop():

    with open("data/langs/words/bulgarian.txt","r",encoding="utf8") as wordData:
        # it = 0
        for line in wordData:
           # To get some feedback
            # it += 1
            # if it % 100 == 0:
            #     break

            rowContent = line.split()
            if(len(rowContent)>=3): # checks if line is valid

                tagsetName = rowContent[-1]
                tagSetObject, created = TagSet.objects.get_or_create(name=tagsetName)

                lemmaName = rowContent[0]
                currWordList = rowContent[1:-1] # it can be more than a single word
                currWord = " ".join(currWordList)

                allLabels = tagsetName.split(";") # last block of words corrensponds to allLabels
                for currLabel in allLabels:
                    currFeature = findFeature[currLabel.upper()]
                    featObject = Feature.objects.get(name=currFeature)
                    tagSetObject.features.add(featObject)

                    # Defining the Word
                posName = findFeature[allLabels[0]]
                lemmaPOS = POS.objects.get(name=posName)
                wordObject = Word(name=currWord)

                try:
                    lemmaObject = Lemma.objects.get(name=lemmaName,pos=lemmaPOS.id)
                    wordObject.language = lemmaObject.language
                except Lemma.DoesNotExist:
                    lemmaObject = None

                wordObject.lemma  = lemmaObject
                wordObject.tagset = tagSetObject
                wordObject.save()


# *  uncomment below to populate !!in order!! *
def popAll():

    #dimensionPop()
    #featurePop()
    #genusPop()
    #posPop()
    #familyPop()
    languagePop()
    lemmaPop()
    readAppendix()
    wordPop()


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
popAll()

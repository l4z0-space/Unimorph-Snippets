import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","eureka.settings.development")
django.setup()

from django.contrib.auth.models import User
from django.contrib import admin
from api.models import Genus, Word, Feature, Dimension, Language, Lemma, Family, TagSet, POS

LANGUAGE_TO_POPULATE = 'Bulgarian'

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
            nextFeature.label = current_line[2].rstrip().upper()
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
            genusName = line.split("\n")[0].rstrip()
            # Create Object
            nextGenus = Genus(name=genusName)
            nextGenus.save()
    print("Genus done")


# Family
def familyPop():

    with open("data/models/families.txt","r") as famData:
        for line in famData:
            FamilyName = line.split(";")[0].rstrip()
            nextFamily = Family(name=FamilyName)
            nextFamily.save()
    print("Family done")


def languagePop():
    with open("data/models/avLanguages.csv","r") as lanData:
        # langName, walsCode, Genus, Family
        for line in lanData:
            currLine = line.split(',')
            nextLang = Language(name=currLine[0])
            nextLang.walsCode = currLine[1]
            nextGenus = currLine[2].rstrip()
            nextFamily = currLine[3].rstrip()
            # print(f'{nextGenus} {nextFamily}')
            try:
                nextLang.genus = Genus.objects.get(name=nextGenus)
            except Genus.DoesNotExist:
                nextLang.genus = None
            try:
                nextLang.family = Family.objects.get(name=nextFamily)
            except Family.DoesNotExist:
                nextLang.family = None

            nextLang.save()
    print("Language done")


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
    fileName = ''.join(['data/langs/Complete/',LANGUAGE_TO_POPULATE,'.txt'])
    languageObject = Language.objects.get(name=LANGUAGE_TO_POPULATE)
    with open(fileName,"r",encoding="utf8") as wordData:
     
        for line in wordData:
            # Lemma Word Tagset - delimiter ('/t')
            rowContent = line.split('\t')
            # print(rowContent)
            if(len(rowContent)>=3): # checks if line is valid
                tagsetName = rowContent[-1].rstrip()
                tagSetObject, created = TagSet.objects.get_or_create(name=tagsetName)
                lemmaName = rowContent[0]
                wordName = rowContent[1]

                allLabels = tagsetName.split(";") # last block of words corrensponds to allLabels
                for currLabel in allLabels:
                    try:
                        currFeature = findFeature[currLabel.upper()]
                        featObject = Feature.objects.get(name=currFeature)
                        tagSetObject.features.add(featObject)
                    except KeyError:
                        print(f'{currLabel}  - not exist')
                

                posName = findFeature[allLabels[0].upper()]
                posObject = POS.objects.get(name=posName)
            
                # If lemma exists
                try:
                    lemmaObject = Lemma.objects.get(name=lemmaName,pos=posObject.id,language=languageObject.id)
                # If not create a new one
                except Lemma.DoesNotExist:
                    lemmaObject = Lemma(name=lemmaName)
                    lemmaObject.language = languageObject
                    lemmaObject.pos = posObject
                    lemmaObject.save()
                finally:
                    wordObject = Word(name=wordName)
                    wordObject.lemma  = lemmaObject
                    wordObject.tagset = tagSetObject
                    wordObject.language = languageObject
                    wordObject.save()


# *  uncomment below to populate !!in order!! *
def popAll():

    dimensionPop()
    featurePop()
    genusPop()
    posPop()
    familyPop()
    languagePop()

    # To populate only words and lemmas
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


if __name__ == "__main__":
    # emptyDatabase()
    # popAll()

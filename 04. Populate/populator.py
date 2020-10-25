import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","eureka.settings.development")
django.setup()

from django.contrib.auth.models import User
from django.contrib import admin
from api.models import Genus, Word, Feature, Dimension, Language, Lemma, Family, TagSet, POS



# Dimensions
def dimensionPop():
    ''' Populate -Dimension- '''

    with open("data/models/dimensions.txt","r") as dimData:
        for x in dimData:
            dimension = x.split("\n")
            dimensionName = dimension[0]
            # Create Object
            nextDim, created = Dimension.objects.get_or_create(name=dimensionName)
            if created:
                nextDim.save()
    print("Dimension done")


# Features
def featurePop():
    ''' Populate -Features- '''

    with open("data/models/features.txt","r") as featData:
        for line in featData:
            # Dimentsion ; Feature ; Label
            currLine = line.split(";")
            featureName = currLine[1]
            dimensionName = currLine[0]
            # Create Object
            featureObject, created = Feature.objects.get_or_create(name=featureName)
            if created:
                dimensionObject = Dimension.objects.get(name=dimensionName)
                featureObject.dimension = dimensionObject
                featureObject.label = currLine[2].rstrip().upper()
                featureObject.save()
            
    print("Feature done")


# Part of Speech
def posPop():
    ''' Populate -Part of Speech- '''

    with open("data/models/POS.txt","r") as posData:
        for line in posData:
            currLine = line.split(";")
            posName = currLine[1]
            # Create Object
            posObject, created = POS.objects.get_or_create(name=posName)
            if created:
                posObject.save()
    print("Part of Speech done")


# Language
def languagePop():
    ''' Populate the -Languages- with their -Family- and -Genus- '''

    with open("data/models/languages.txt","r") as lanData:
        # langName, walsCode, Genus, Family
        for line in lanData:
            currLine = line.split(',')
            languageObject, created = Language.objects.get_or_create(name=currLine[0])
            if created:
                # languageObject.walsCode = currLine[1]
                genusName = currLine[2].rstrip()
                familyName = currLine[3].rstrip()
            
                # Genus
                languageObject.genus, created = Genus.objects.get_or_create(name=genusName)
                if(languageObject.genus.name == ""):
                    languageObject.genus = None
                
                # Family
                languageObject.family, created = Family.objects.get_or_create(name=familyName)
                if(languageObject.family.name == ""):
                    languageObject.family = None

                languageObject.save()

    print("Language done")


def lang_codePop():
    ''' Populate languages code (wals_code ISO)'''

    with open("data/models/ISO.txt","r") as fileContent:
        for row in fileContent:
            row_words = row.split(' ')
            iso = row_words[0].rstrip()
            languageName = ' '.join(row_words[1:]).rstrip()
            # print(f'|{iso}|{languageName}|')
            languageObject = Language.objects.get(name=languageName)
            languageObject.walsCode = iso
            # print(languageObject.walsCode, languageObject.name)
            languageObject.save()
    print('ISO done')

findFeature={}
def readAppendix():
    ''' Read the appendix to map features with their labels '''

    with open("data/models/features.txt","r") as fileContent:
        for row in fileContent:
            rowWords = row.split(";")
            dimension = rowWords[0]
            feature = rowWords[1]
            label = (rowWords[2].rstrip()).upper()
            findFeature[label]=feature
    print("\nStarting with words...")

# Words and Lemma
def wordPop(LANGUAGE_TO_POPULATE):
    ''' Populate the -Words- and -Lemmas- '''

    fileName = ''.join(['data/langs/',LANGUAGE_TO_POPULATE,'.txt'])
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
                

                posName = findFeature[allLabels[0].upper()].rstrip()
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
                # Finally create the word
                finally:
                    wordObject = Word(name=wordName)
                    wordObject.lemma  = lemmaObject
                    wordObject.tagset = tagSetObject
                    wordObject.language = languageObject
                    wordObject.save()


# *  uncomment below to populate !!in order!! *
def popAll():
    ''' Populate the database '''

    dimensionPop()
    featurePop()
    posPop()
    languagePop()
    lang_codePop()
    # To populate only words and lemmas

    # readAppendix()
    # wordPop()


# Just in case it goes wrong
def emptyDatabase():
    ''' Empty the databse '''

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

#   -   -   -   -   -   -   -   -   -   -   -   -  #

def showPopulated():
    allLanguages = Language.objects.all()
    print('Populated languages: ')
    for language in allLanguages:
        langID = language.id
        words = Word.objects.filter(language=langID).count()
        if (words > 0):
            print(f'\t+ {language.name}: {words} words')

def validateLanguage(LANGUAGE_TO_POPULATE):
    response = True
    try:
        Language.objects.get(name=LANGUAGE_TO_POPULATE)
    except Language.DoesNotExist:
        print('Language does not exists...')
        response = False

    return response

def menu():
    ch = 100
    while (ch!='0'):
        print(' 1 - show populated \n 2 - empty db \n 3 - populate lang data')
        ch = input('> ')

        if(ch=='1'):
            showPopulated()
        elif(ch=='2'):
            print('Are you sure to delete all data?')
            c = input('Press y to delete: ')

            if (c=='y'):
                emptyDatabase()
        elif(ch=='3'):
            LANGUAGE_TO_POPULATE = input('Language name: ')
            if (validateLanguage(LANGUAGE_TO_POPULATE)):
                
                readAppendix()
                wordPop(LANGUAGE_TO_POPULATE)
        


if __name__ == "__main__":
    popAll()
    menu()
    # showPopulated()
    # emptyDatabase()
    # popAll()

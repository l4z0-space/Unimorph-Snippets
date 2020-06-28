from django.http import Http404, HttpResponse
from rest_framework import status, generics
from rest_framework.response import Response
import csv
from rest_framework.views import APIView
from django.db import connection
from django.utils import timezone
from django.db.models import F
from django.db.models import Case, When, Value, CharField
from ..models import Genus, Dimension, Feature, Language, Family, Lemma, Word
from ..utils import Response

class GenusDownload(APIView):
    """ Download a .csv file with all the Genuses """
    def get(self, request, format=None):
        filename = 'genuses'
        querySet =  Genus.objects.all().values(
            'name',
        )
        response = Response()
        return response.csvResponse(querySet, filename)


class DimensionDownload(APIView):
    """ Download a .csv file with all the Dimensions """
    def get(self, request, format=None):
        filename = 'dimensions'
        querySet =  Dimension.objects.all().values(
            'name',
        )
        response = Response()
        return response.csvResponse(querySet, filename)


class FeatureDownload(APIView):
    """ Download a .csv file with all the Features """
    def get(self, request, format=None):
        filename = 'features'
        querySet =  Feature.objects.all().values(
            'name',
            dimension_name = F('dimension__name'),
        )
        response = Response()
        return response.csvResponse(querySet, filename)


class LanguageDownload(APIView):
    """ Download a .csv file with all the Languages available """
    def get(self, request, format=None):
        filename = 'languages'
        querySet =  Language.objects.all().values(
            'name',
            'walsCode',
            family_name = F('family__name'),
            genus_name = F('genus__name'),
        )
        response = Response()
        return response.csvResponse(querySet, filename)


class WordDownload(APIView):
    """ Download a file with all the words of a language - api/download/word/languageName """
    def get(self, request, format=None,**kwargs):
        languageName = self.kwargs['languageName']
        languageName = "".join([languageName[0].upper(), languageName[1:].lower()])
        languageObject = Language.objects.get(name=languageName)
        querySet =  Word.objects.filter(language=languageObject.id).values(
            'name',
            lemma_name = F('lemma__name'),
            tagset_name = F('tagset__name'),
        )
        response = Response()
        return response.csvResponse(querySet, languageObject)


class FamilyQueryDownload(APIView):
    """ Download a zipped folder with all the languages of a given family - api/download/families/familyName """
    def get(self, request, format=None,**kwargs):
        familyName = self.kwargs['familyName']
        familyObject  = Family.objects.get(name=familyName)
        allLanguages = Language.objects.filter(family=familyObject.id)
        filename = '-'.join(["Family",familyName])
        response = Response()
        return response.zipResponse(allLanguages, filename)


class GenusQueryDownload(APIView):
    """ Download a zipped folder with all the languages of a given genus - api/download/genuses/genusName """
    def get(self, request, format=None,**kwargs):
        genusName = self.kwargs['genusName']
        genusObject  = Genus.objects.get(name=genusName)
        allLanguages = Language.objects.filter(genus=genusObject.id)
        filename = '-'.join(["Genus",genusName])
        response = Response()
        return response.zipResponse(allLanguages, filename)


class AllLanguagesDownload(APIView):
    """ Donwload all languages in the database """
    def get(self, request, format=None):
        filename = "all-languages"
        allLanguages = Language.objects.all()
        response = Response()
        return response.zipResponse(allLanguages, filename)

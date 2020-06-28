from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Genus, Word, Feature, Dimension, Language, Lemma, Family, TagSet, POS

# Register your models here.
admin.site.register(Word)
admin.site.register(Feature)
admin.site.register(Dimension)
admin.site.register(Language)
admin.site.register(Lemma)
admin.site.register(Family)
admin.site.register(TagSet)
admin.site.register(POS)
admin.site.register(Genus)

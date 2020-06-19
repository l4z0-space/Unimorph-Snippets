from django.db import connection
from django.utils import timezone
import csv
from django.db.models import F
from django.db.models import Case, When, Value, CharField
from django.http import Http404, FileResponse, HttpResponse


class WordDownload(generics.ListAPIView):
    """ Download a file with all the words of a language - api/download/word/LANGUAGE """
    def get(self, request, format=None,**kwargs):
        lang = Language.objects.get(name='English')
        qs =  Word.objects.filter(language=lang.id).values(
            'name',
            lemma_name = F('lemma__name'),
            tagset_name = F('tagset__name'),
        )
        return qs_to_csv_response(qs,"bulgarian")


def qs_to_csv_response(qs, filename):
    """ Get the queryset and creates the file """
    sql, params = qs.query.sql_with_params()

    sql = f"COPY ({sql}) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER E'\t')"
    filename = f'{filename}.txt'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    with connection.cursor() as cur:
        sql = cur.mogrify(sql, params)
        cur.copy_expert(sql, response)
    return response

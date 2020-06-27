

class Response():
    """ Class to help with responses """

    def qs_to_csv_response(self,querySet, filename):
        """ Get the queryset and creates the csv file """
        sql, params = querySet.query.sql_with_params()
        sql = f"COPY ({sql}) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER E',')"
        filename = f'{filename}.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        with connection.cursor() as cur:
            sql = cur.mogrify(sql, params)
            cur.copy_expert(sql, response)
        return response

    def qs_to_zip_response(self,allLanguages, filename):
        """ Get the languages queryset and create the zip file """
        in_memory = BytesIO()
        zip = ZipFile(in_memory, "a")
        languageList = list(allLanguages)
        for language in languageList:
            # Determine the queryset
            querySet =  Word.objects.filter(language=language.id).values(
                'name',
                lemma_name = F('lemma__name'),
                tagset_name = F('tagset__name'),
            )
            sql, params = querySet.query.sql_with_params()
            sql = f"COPY ({sql}) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER E',')"
            subfileName = f'{language}.txt'
            response = HttpResponse(content_type='text/csv')
            with connection.cursor() as cur:
                sql = cur.mogrify(sql, params)
                cur.copy_expert(sql, response)
                zip.writestr(subfileName, response.content)
        zip.close()
        # Creates the zip file response
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = f"attachment; filename={filename}.zip"
        in_memory.seek(0)
        response.write(in_memory.read())
        return response

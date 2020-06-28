from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView


class APIRootList(APIView):
    def get(self, request, format=None):
        data = {
            'languages': reverse('languages', request=request),
            'words': reverse('words', request=request),
            'features': reverse('features', request=request),
            'dimensions': reverse('dimensions', request=request),
            'lemmas': reverse('lemmas', request=request),
            'tagsets': reverse('tagsets', request=request),
            'families': reverse('families', request=request),
            'genuses': reverse('genuses', request=request)
        }
        return Response(data)

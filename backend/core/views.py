from django.http import HttpResponse
from rest_framework import status

def healthcheck(request):
    return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
from django.http import JsonResponse
from rest_framework import status

def healthcheck(request):
    return JsonResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
import os
import requests
import json

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
# pylint: disable=wildcard-import,unused-wildcard-import
from rest_framework.status import *

@api_view(["GET"])
@permission_classes((AllowAny,))
def check(request):
    return JsonResponse({"Ok?": "Ok!"}, status=HTTP_200_OK)

@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    r = requests.post(os.environ.get('USERS_URL'), json.loads(request.body))
    return JsonResponse(r.json(), status=r.status_code)

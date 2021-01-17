# pylint: disable=no-member,wildcard-import,unused-wildcard-import
import os
import requests
import json

from django.http import JsonResponse
from django.db import connections
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import *

from .models import Report, ReportSerializer, View

def token_is_valid(token):
    token = token.replace('Token ', '')
    r = requests.post(f'{os.environ.get("USERS_URL")}verify/', {'token': token})
    return r.status_code == HTTP_200_OK

@api_view(["GET"])
def check(request):
    return JsonResponse({"Ok?": "Ok!"}, status=HTTP_200_OK)

@api_view(["POST"])
def login(request):
    r = requests.post(os.environ.get('USERS_URL'), json.loads(request.body))
    return JsonResponse(r.json(), status=r.status_code)

@api_view(["POST"])
def refresh(request):
    r = requests.post(f'{os.environ.get("USERS_URL")}refresh/', json.loads(request.body))
    return JsonResponse(r.json(), status=r.status_code)

@api_view(["GET", "POST"])
def reports(request):
    if not token_is_valid(request.headers['Authorization']):
        return JsonResponse({'detail': 'Token is invalid or expired'}, status=HTTP_401_UNAUTHORIZED)
    
    data = Report.objects.all()
    reports = {}
    with connections['mainDB'].cursor() as cursor:
        for report in data:
            periods = set()
            views = View.objects.filter(reportviewrelation__report=report.id)
            for v in views:
                if v.main_period == '':
                    periods.add('Todos los periodos')
                else:
                    cursor.execute('select distinct {} from {};'.format(v.main_period, v.name))
                    for row in cursor:
                        periods.add(row[0])

            reports[report.name] = sorted(list(periods), reverse=True)

    return JsonResponse(reports, safe=False, status=HTTP_200_OK)

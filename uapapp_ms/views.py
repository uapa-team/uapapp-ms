# pylint: disable=no-member,wildcard-import,unused-wildcard-import
import os
import requests
import json
import xlsxwriter
import jwt

from django.http import JsonResponse
from django.db import connections
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import *
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Report, View, ReportTypes, Format
from .helpers import get_report_periods, get_role

def get_token(request):
    jwt_obj = JWTAuthentication()
    header = jwt_obj.get_header(request)
    return jwt_obj.get_raw_token(header)

def decode_token(token):
    return jwt.decode(token, options={"verify_signature": False})

def token_is_valid(request):
    token = get_token(request)
    r = requests.post(f'{os.environ.get("USERS_URL")}verify/', {'token': token})
    return r.status_code == HTTP_200_OK

@api_view(["GET"])
def check(request):
    return JsonResponse({"Ok?": "Ok!"}, status=HTTP_200_OK)

@api_view(["POST"])
def login(request):
    r = requests.post(os.environ.get('USERS_URL'), json.loads(request.body))
    payload = r.json()
    user_info = decode_token(payload['access'])
    payload['username'] = user_info['username']
    payload['full_name'] = user_info['full_name']
    payload['role'] = get_role(user_info['groups'])

    return JsonResponse(payload, status=r.status_code)

@api_view(["POST"])
def refresh(request):
    r = requests.post(f'{os.environ.get("USERS_URL")}refresh/', json.loads(request.body))
    return JsonResponse(r.json(), status=r.status_code)

@api_view(["GET"])
def reports(request):
    if not token_is_valid(request):
        return JsonResponse({'detail': 'Token is invalid or expired.'}, status=HTTP_401_UNAUTHORIZED)
    
    data = Report.objects.filter(category=ReportTypes.REPORTE)

    return JsonResponse(get_report_periods(data), safe=False, status=HTTP_200_OK)

@api_view(["POST"])
def report(request, code):
    if not token_is_valid(request):
        return JsonResponse({'detail': 'Token is invalid or expired.'}, status=HTTP_401_UNAUTHORIZED)
    
    try:
        report = Report.objects.get(id=code)
    except Report.DoesNotExist:
        return JsonResponse({'detail': 'The requested report does not exist.'}, status=HTTP_404_NOT_FOUND)

    filters = json.loads(request.body)

    if not ('periods' in filters and 'programs' in filters) or len(filters.keys()) != 2:
        return JsonResponse({'detail': "The body keys must be 'periods' and 'programs' only"}, 
            status=HTTP_400_BAD_REQUEST)

    file_name = f'public/{report.name}.xlsx'
    with connections['mainDB'].cursor() as cursor, xlsxwriter.Workbook(file_name) as book:
        title_format = book.add_format()
        title_format.set_center_across()
        title_format.set_bold()

        views = View.objects.filter(reportviewrelation__report=report.id)
        for v in views:
            sheet = book.add_worksheet(v.sheet_name)
            cursor.execute(
                "select column_name from information_schema.columns \
                 where table_name = '{}' order by ordinal_position;".format(v.name))

            columns = [row[0] for row in cursor]
            sheet.write_row(0, 0, columns)
            sheet.set_row(0, None, title_format)

            for i in range(len(columns)):
                sheet.set_column(i, i, len(columns[i]) + 5)
            
            query = 'select * from {} '.format(v.name)
            and_f = False
            if v.main_period != '':
                query += 'where {} in ({})'.format(
                    v.main_period, ','.join([str(p) for p in filters['periods']]))
                and_f = True
            if v.main_program != '':
                query += ' and ' if and_f else ' where '
                query += '{} in ({})'.format(
                    v.main_program, ','.join([str(p) for p in filters['programs']]))

            counter = 1
            cursor.execute(query)
            for row in cursor:
                sheet.write_row(counter, 0, row)
                counter += 1

    return JsonResponse({"url": file_name}, status=HTTP_200_OK)

@api_view(["GET"])
def formats(request):
    if not token_is_valid(request):
        return JsonResponse({'detail': 'Token is invalid or expired.'}, status=HTTP_401_UNAUTHORIZED)
    
    formats = [f[1] for f in Format.choices]

    return JsonResponse({'Formatos': formats}, status=HTTP_200_OK)

@api_view(["GET"])
def subformats(request, fr):
    if not token_is_valid(request):
        return JsonResponse({'detail': 'Token is invalid or expired.'}, status=HTTP_401_UNAUTHORIZED)
    
    data = Report.objects.filter(category=ReportTypes.FORMATO_DE_RECOLECCION, _format=fr)

    return JsonResponse(get_report_periods(data), safe=False, status=HTTP_200_OK)

@api_view(["GET"])
def programs(request):
    if not token_is_valid(request):
        return JsonResponse({'detail': 'Token is invalid or expired.'}, status=HTTP_401_UNAUTHORIZED)

    if request.GET.get('level', 'PRE') == 'PRE':
        modifier = 'where fk_niv = 1'
    else:
        modifier = 'where fk_niv != 1'

    programs = []
    with connections['mainDB'].cursor() as cursor:
        cursor.execute(f'select * from programs_info {modifier};')
        for p in cursor:
            programs.append(p[:2])
    return JsonResponse({'Programs': programs}, status=HTTP_200_OK)

# pylint: disable=no-member,wildcard-import,unused-wildcard-import
from django.db import connections

from .models import View

def get_role(groups):
    if 'UAPApp - Administradores' in groups:
        return 'Administrador' # 1
    if 'UAPApp - Auxiliares' in groups:
        return 'Auxiliar' # 2
    if 'UAPApp - Coordinadores' in groups:
        return 'Coordinador' # 3
    if 'UAPApp - Miembros UAPA' in groups:
        return 'UAPA' # 4
    if 'UAPApp - Miembros Dependencia' in groups:
        return 'Dependencia' # 5
    return 'Sin rol asignado' # 0

def get_report_periods(data):
    reports = {}
    with connections['mainDB'].cursor() as cursor:
        for report in data:
            periods = set()
            views = View.objects.filter(reportviewrelation__report=report.id)
            for v in views:
                if v.main_period == '':
                    periods.add((0, 'Todos los periodos'))
                else:
                    cursor.execute('select distinct {}, {} from {};'.format(v.main_period, v.text_period, v.name))
                    for row in cursor:
                        periods.add((row[0], row[1]))

            reports[report.name] = {
                'code': report.id,
                'description': report.description,
                'periods': sorted(list(periods), key=lambda x: x[0], reverse=True)
                }
    return reports

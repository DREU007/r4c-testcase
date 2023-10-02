from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from django.db.models import Count, ExpressionWrapper, F, CharField
from datetime import timedelta
import json
from openpyxl import Workbook
from .forms import RobotForm
from .models import Robot


class PostJson(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = RobotForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Data received successfully'})
        errors = form.errors.as_join()
        return JsonResponse({'errors': errors}, status=400)


class RobotsExcelView(View):
    def get(self, request, *args, **kwargs):
        # Generate report within report_delta
        report_delta = {'weeks': 1}

        # TODO: Feat: Synchronize timezone
        report_time_end = datetime.datetime.now()
        report_time_start = report_time_end - timedelta(**report_delta)

        robots = Robot.objects.filter(
            created__gte=report_time_start
        ).values('model', 'version').annotate(
            num_counted=Count('id', distinct=True)
        ).order_by('model', 'version')
        
        # TODO: Generate Excel file
        report_wb = Workbook()
        report_date = report_time_end.strftime('%d.%m.%Y')

        report_ws = report_wb.create_sheet(f"Wk robots @{report_date}")
        report_file_title = f"wk-rep-robots-{report_date}"

        col_titles = {
            "model": "Модель",
            "version": "Версия",
            "num_counted": "Количество за неделю"
        }

        for row in report_ws.iter_rows(min_row=1, max_row=1, max_col=len(col_titles)):
            for cell, title in zip(row, col_titles):
                cell.value = title

        # TODO: Return direct download link to excel

from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from django.db.models import Count, ExpressionWrapper, F, CharField

from datetime import timedelta
import json
from openpyxl import Workbook
from openpyxl import Border

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
        
        grouped_robots = {}
        for key, group in itertools.groupby(robots, lambda k: k["model"]):
            grouped_robots[key] = list(group)
            
        # Generate Excel file
        report_wb = Workbook()
        report_wb.remove(report_wb.active)
        report_date = report_time_end.strftime('%d.%m.%Y')

        report_file_title = f"wk-rep-robots-{report_date}"

        # Fill column titles
        col_titles = [  
                {"key": "model", "name": "Модель", "col_num": 1},
                {"key": "version", "name": "Версия", "col_num": 2},
                {"key": "num_counted", "name": "Количество за неделю", "col_num": 3},
        ]

        for model, group in grouped_robots.items():
            report_ws = report_wb.create_sheet(model)
            set_ws_column_titles(report_ws, col_titles)
            set_ws_data(report_ws, group, col_titles)
        # TODO: Return direct download link to excel

        def set_ws_column_titles(ws, col_titles):
            for title in col_titles:
                ws.cell(
                    row=1,
                    column=title["col_num"],
                    value=title["name"],
                )
        def set_ws_data(ws, data, col_titles):
            current_row = 2
            for item in data:
                for title in col_titles:
                    ws.cell(
                        row=current_row,
                        column=title["col_num"],
                        value=item[title["key"]],
                    )
                current_row += 1
            
            

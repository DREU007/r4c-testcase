from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from django.db.models import Count, ExpressionWrapper, F, CharField
from datetime import timedelta
import json
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
        # TODO: SQL query within a week, paged by model with all versions and quantity
        report_delta = {'weeks': 1}

        robots = Robot.objects.filter(
            created__gte=F('created') + timedelta(**report_delta)
        ).order_by('model', 'version').annotate(
            combined=ExpressionWrapper(
                F('model') + F('version'),
                output_field=CharField(max_length=4)
            )
        )

        # SELECT DISTINCT ON (model, version) model, version, count(version) ORDER BY model, version;
        robots = Robot.objects.get()
        # TODO: Generate Excel file
        # TODO: Return direct download link to excel

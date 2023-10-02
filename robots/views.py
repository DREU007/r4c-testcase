from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
import json
from .forms import RobotForm


class PostJson(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = RobotForm(data)
        if form.is_valid():
            serial = (
                f'{form.cleaned_data["model"]}-{form.cleaned_data["version"]}'
            )
            form.instance.serial = serial
            form.save()
            return JsonResponse({'message': 'Data received successfully'})
        errors = form.errors.as_join()
        return JsonResponse({'errors': errors}, status=400)

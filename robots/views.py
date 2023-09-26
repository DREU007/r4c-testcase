from django.shortcuts import render
from django.views import View
import json


class PostJson(View):
    def post(self, request, *args, **kwargs):
        data = request.body
        try:
            json_data = json.loads(data)
        except Exception as error:
            return render(request, 'index.html', {'errors': error}

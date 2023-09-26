from django.shortcuts import path
from .views import views


urlpatterns = [
    path('post_json/', views.PostJson.as_view(), name='post_json'),
]

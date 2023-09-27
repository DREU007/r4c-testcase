from django.urls import path
from .views import PostJson


urlpatterns = [
    path('post_json/', PostJson.as_view(), name='post_json'),
]

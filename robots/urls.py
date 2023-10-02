from django.urls import path
from .views import PostJson, RobotsExcelDownloadView


urlpatterns = [
    path('post_json/', PostJson.as_view(), name='post_json'),
    path(
        'download/weekly/',
        RobotsExcelDownloadView.as_view(),
        name="download_robot_wk_report"
    ),
]

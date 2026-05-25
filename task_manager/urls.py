from django.urls import path
from task_manager.views import IndexView

app_name = "task_manager"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
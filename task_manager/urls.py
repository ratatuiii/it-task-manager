from django.urls import path
from task_manager.views import IndexView, WorkerDetailView, WorkerUpdateFieldView

app_name = "task_manager"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/<str:field>/", WorkerUpdateFieldView.as_view(), name="worker-update-field"),
]

from django.urls import path
from task_manager.views import IndexView, TaskListView, WorkerDetailView, WorkerListView, WorkerUpdateFieldView

app_name = "task_manager"

from task_manager.views import (
    IndexView,
    WorkerDetailView,
    WorkerUpdateFieldView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateFieldView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/<str:field>/", WorkerUpdateFieldView.as_view(), name="worker-update-field"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/<str:field>/", TaskUpdateFieldView.as_view(), name="task-update-field"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
]
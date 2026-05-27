from django.urls import path
app_name = "task_manager"

from task_manager.views import (
    AssignYourselfView,
    IndexView,
    PositionAssignView,
    PositionCreateView,
    PositionDeleteView,
    PositionListView,
    TaskTypeCreateView,
    TaskTypeDeleteView,
    TaskTypeListView,
    WorkerDetailView,
    WorkerListView,
    WorkerUpdateFieldView,
    WorkerRegisterView,
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
    path("accounts/register/", WorkerRegisterView.as_view(), name="register"),
    path(
        "tasks/<int:pk>/assign-yourself/",
        AssignYourselfView.as_view(),
        name="assign-yourself",
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
    path("task-types/", TaskTypeListView.as_view(), name="tasktype-list"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="tasktype-create"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="tasktype-delete"),
    path("positions/<int:pk>/assign/", PositionAssignView.as_view(), name="position-assign"),
]
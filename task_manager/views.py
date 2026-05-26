from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Q, Count

from task_manager.models import Worker, Task, TaskType
from task_manager.forms import WorkerCreationForm

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "task_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}

        active_tasks = (
            user.tasks.filter(is_completed=False)
            .order_by("deadline")
            .select_related("task_type")
        )

        active_tasks_sorted = sorted(
            active_tasks,
            key=lambda t: (t.deadline, priority_order.get(t.priority, 99))
        )[:5]

        today = timezone.now().date()

        completed = user.tasks.filter(is_completed=True)
        completed_by_priority = {
            "urgent": completed.filter(priority="urgent").count(),
            "high": completed.filter(priority="high").count(),
            "medium": completed.filter(priority="medium").count(),
            "low": completed.filter(priority="low").count(),
        }

        context["active_tasks"] = active_tasks_sorted
        context["completed_by_priority"] = completed_by_priority
        context["tasks_in_work"] = user.tasks.filter(is_completed=False).count()
        context["tasks_past_deadline"] = user.tasks.filter(
            is_completed=False, deadline__lt=today
        ).count()
        return context


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "task_manager/worker_detail.html"
    context_object_name = "worker"


class WorkerUpdateFieldView(LoginRequiredMixin, View):
    def post(self, request, pk, field):
        if request.user.pk != pk:
            raise PermissionDenied

        worker = get_object_or_404(Worker, pk=pk)

        if field == "username":
            worker.username = request.POST.get("username", worker.username)
        elif field == "legal_name":
            worker.first_name = request.POST.get("first_name", worker.first_name)
            worker.last_name = request.POST.get("last_name", worker.last_name)
        elif field == "email":
            worker.email = request.POST.get("email", worker.email)

        worker.save()
        return redirect("task_manager:worker-detail", pk=pk)


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    context_object_name = "workers"

    def get_queryset(self):
        return Worker.objects.annotate(
            completed_tasks=Count(
                "tasks", filter=Q(tasks__is_completed=True)
            )
        ).order_by("-completed_tasks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_ranked = list(self.get_queryset())
        top10 = all_ranked[:10]

        user = self.request.user
        user_in_top10 = any(w.pk == user.pk for w in top10)

        user_entry = None
        if not user_in_top10:
            for rank, worker in enumerate(all_ranked, start=1):
                if worker.pk == user.pk:
                    user_entry = (rank, worker)
                    break

        context["top10"] = list(enumerate(top10, start=1))
        context["user_entry"] = user_entry
        context["current_user"] = user
        return context


class WorkerRegisterView(CreateView):
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10




class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_types"] = TaskType.objects.all()
        return context


from django.http import JsonResponse
import json


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "task_manager/task_form.html"
    fields = ["name", "description", "deadline", "priority"]
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_types"] = TaskType.objects.all()
        return context

    def form_valid(self, form):
        task = form.save(commit=False)

        # handle task_type: match existing or create new
        task_type_input = self.request.POST.get("task_type_input", "").strip()
        if task_type_input:
            task_type, _ = TaskType.objects.get_or_create(name=task_type_input)
            task.task_type = task_type

        task.save()

        # optionally assign self
        if self.request.POST.get("assign_self"):
            task.assignees.add(self.request.user)

        return redirect(self.success_url)


class TaskUpdateFieldView(LoginRequiredMixin, View):
    def post(self, request, pk, field):
        task = get_object_or_404(Task, pk=pk)

        if field == "name":
            task.name = request.POST.get("name", task.name)
        elif field == "description":
            task.description = request.POST.get("description", task.description)
        elif field == "deadline":
            task.deadline = request.POST.get("deadline", task.deadline)
        elif field == "priority":
            task.priority = request.POST.get("priority", task.priority)
        elif field == "task_type":
            task_type_id = request.POST.get("task_type")
            if task_type_id:
                task.task_type = get_object_or_404(TaskType, pk=task_type_id)
        elif field == "is_completed":
            task.is_completed = request.POST.get("is_completed") == "true"

        task.save()
        return redirect("task_manager:task-detail", pk=pk)
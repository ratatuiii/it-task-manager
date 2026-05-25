from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied

from task_manager.models import Worker

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "task_manager/index.html"


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
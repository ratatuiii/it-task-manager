from django.contrib.auth.forms import UserCreationForm
from django import forms


from task_manager.models import Position, TaskType, Worker


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ["username", "first_name", "last_name", "email", "position"]


class PositionCreateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]


class TaskTypeCreateForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ["name"]
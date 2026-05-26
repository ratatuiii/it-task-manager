from django.contrib.auth.forms import UserCreationForm
from task_manager.models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ["username", "first_name", "last_name", "email", "position"]

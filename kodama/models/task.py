from django.db import models
from django.db import models
from django.utils import timezone
from django.utils import timezone



class TaskAudit(models.Model):
    task_name = models.CharField(max_length=255)
    run_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ])
    result = models.TextField(null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)

    @classmethod
    def create_audit(cls, task_name):
        audit = cls.objects.create(
            task_name=task_name,
            status='PENDING',
        )
        return audit

    def __str__(self):
        return f"{self.task_name} ({self.status}) @ {self.run_at}"
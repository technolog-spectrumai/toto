from django.contrib import admin
from kodama.models import TaskAudit


@admin.register(TaskAudit)
class TaskAuditAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'status', 'run_at')
    list_filter = ('status', 'run_at')
    search_fields = ('task_name', 'result', 'traceback')
    readonly_fields = ('task_name', 'status', 'run_at', 'result', 'traceback')

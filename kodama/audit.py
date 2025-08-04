from contextlib import contextmanager
from .models import TaskAudit

@contextmanager
def task_audit(task_name):
    audit = TaskAudit.create_audit(task_name=task_name)
    audit.save()
    try:
        yield audit  # control goes to the task logic
    except Exception as e:
        audit.status = 'FAILURE'
        audit.result = str(e)
        audit.traceback = getattr(audit, 'traceback', '')  # Optional fallback
        audit.save()
        raise
    else:
        audit.status = 'SUCCESS'
        audit.save()

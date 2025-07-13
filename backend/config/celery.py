import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("hr_system")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Configuration
app.conf.update(
    # Broker settings
    broker_url=os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//"),
    # Result backend (not using it)
    result_backend=None,
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    # Timezone
    timezone="UTC",
    enable_utc=True,
    # Task execution settings
    task_always_eager=os.environ.get("CELERY_TASK_ALWAYS_EAGER", "False").lower() == "true",
    task_eager_propagates=True,
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    # Task settings
    task_annotations={
        "core.tasks.send_email_task": {
            "rate_limit": "10/m",
        },
    },
    # Error handling
    task_acks_late=True,
    worker_disable_rate_limits=False,
)


@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup."""
    print(f"Request: {self.request!r}")
    return "Celery is working!"

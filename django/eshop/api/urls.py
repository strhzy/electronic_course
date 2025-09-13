from django.urls import path, include
from .routers import AutoRegisterRouter

router = AutoRegisterRouter()
router.register_models(
    exclude_models=[
        'logentry',  # admin.LogEntry
        'session',   # sessions.Session
        'contenttype',  # contenttypes.ContentType
        'permission',  # auth.Permission
        'group',  # auth.Group
        'user'  # auth.User - лучше создать кастомный ViewSet
    ]
)

urlpatterns = [
    path('', include(router.urls)),
]
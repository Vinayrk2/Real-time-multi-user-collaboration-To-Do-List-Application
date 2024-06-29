# asgi.py

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import asynctodo.routing
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TodoApp.settings')
django.setup()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            asynctodo.routing.websocket_urlpatterns
        )
    ),
})

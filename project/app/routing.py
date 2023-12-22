from django.urls import path
from . import consumers
websocket_urlpatters = [
    path('ws/sc/<str:groupname>/', consumers.MySyncConsumer.as_asgi()),
]   
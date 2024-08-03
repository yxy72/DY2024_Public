from django.urls import re_path
from app import consumers
websocket_urlpatterns = [
    re_path(r'connect/(?P<group>\w+)/$',consumers.DYConsumer.as_asgi()),
    re_path(r'upload/(?P<group>\w+)/$',consumers.DY_UploadRawDataConsumer.as_asgi()),
]
from django.conf.urls import url
from incidents import consumers

websocket_urlpatterns = [
    url(r'^ws/$', consumers.UpdateConsumer)
]
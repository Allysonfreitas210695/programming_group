from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path('ws/group/<uuid:group_id>/', consumers.GroupChatConsumer.as_asgi()),
    path('ws/private/<uuid:user_id>/', consumers.PrivateChatConsumer.as_asgi()),
]

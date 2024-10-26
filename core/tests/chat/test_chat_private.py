import pytest
import uuid
from channels.testing import WebsocketCommunicator
from core.models import University, User
from programming_group.asgi import application
from channels.db import database_sync_to_async
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_private_chat_connection():
    # Limpar o banco de dados e criar dados necessários
    await database_sync_to_async(call_command)('flush', verbosity=0, interactive=False)

    university = await database_sync_to_async(University.objects.create)(name='Test University')

    unique_email1 = f'user1-{uuid.uuid4()}@example.com'
    unique_email2 = f'user2-{uuid.uuid4()}@example.com'

    user1 = await database_sync_to_async(User.objects.create_user)(
        email=unique_email1,
        password='password123',
        name='User One',
        cpf='12345678901',
        dateOfBirth='1990-01-01',
        university=university
    )
    user2 = await database_sync_to_async(User.objects.create_user)(
        email=unique_email2,
        password='password123',
        name='User Two',
        cpf='09876543210',
        dateOfBirth='1992-02-02',
        university=university
    )

    # Criar um cliente WebSocket autenticado
    communicator = WebsocketCommunicator(
        application,
        f'/ws/private/{user2.id}/'
    )
    # Simular autenticação para o WebSocket
    communicator.scope['user'] = user1
    connected, _ = await communicator.connect()
    assert connected

    # Enviar uma mensagem e verificar a resposta
    await communicator.send_json_to({'message': 'Hello, private!'})
    response = await communicator.receive_json_from()
    assert response['message'] == 'Hello, private!'

    await communicator.disconnect()

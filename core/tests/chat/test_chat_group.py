import pytest
import uuid
from channels.testing import WebsocketCommunicator
from core.models import University, User, Group
from programming_group.asgi import application
from channels.db import database_sync_to_async
from django.core.management import call_command

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_websocket_connection():
    # Limpar o banco de dados
    await database_sync_to_async(call_command)('flush', verbosity=0, interactive=False)

    # Criar universidade
    university = await database_sync_to_async(University.objects.create)(name='Test University')

    # Criar usuários
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

    # Criação do grupo com um criador definido
    group = await database_sync_to_async(Group.objects.create)(
        name='Test Group',
        creator=user1
    )

    # Adicione os usuários ao grupo
    await database_sync_to_async(group.members.add)(user1)
    await database_sync_to_async(group.members.add)(user2)

    # Criar e conectar um WebSocket para user1
    communicator1 = WebsocketCommunicator(
        application,
        f'/ws/group/{group.id}/'
    )
    communicator1.scope['user'] = user1
    connected1, _ = await communicator1.connect()
    assert connected1, "Failed to connect communicator1"

    # Criar e conectar um WebSocket para user2
    communicator2 = WebsocketCommunicator(
        application,
        f'/ws/group/{group.id}/'
    )
    communicator2.scope['user'] = user2
    connected2, _ = await communicator2.connect()
    assert connected2, "Failed to connect communicator2"

    # Verificar se ambos os WebSockets estão conectados
    assert communicator1.scope['user'] is not None, "communicator1 user is None"
    assert communicator2.scope['user'] is not None, "communicator2 user is None"

    # Testar desconexão
    await communicator1.disconnect()
    await communicator2.disconnect()

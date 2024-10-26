from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from core.serializers.task_serializer import TaskSerializer
from core.services.task_service import TaskService
from core.shared.customAPIException import CustomAPIException
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

class TaskPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class TaskViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = TaskPagination

    def list(self, request, group_id=None):
        try:
            if group_id is not None:
                tasks = TaskService.list_tasks_by_group(group_id)
            else:
                tasks = TaskService.list_all_tasks()

            paginator = self.pagination_class()
            paginated_tasks = paginator.paginate_queryset(tasks, request)

            serializer = TaskSerializer(paginated_tasks, many=True)
            return paginator.get_paginated_response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def retrieve(self, request, pk=None):
        try:
            task = TaskService.retrieve_task(pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Atualizando os dados validados para incluir o criador (usuário autenticado)
                validated_data = serializer.validated_data
                validated_data['created_by'] = request.user  # Adiciona o request.user como criador

                task = TaskService.create_task(validated_data)
                response_serializer = TaskSerializer(task)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({'detail': str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        try:
            task = TaskService.retrieve_task(pk)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            
            if serializer.is_valid():
                # Atualizando os dados da tarefa sem os campos Many-to-Many diretamente
                validated_data = serializer.validated_data
                
                # Atualiza os campos normais
                task.title = validated_data.get('title', task.title)
                task.description = validated_data.get('description', task.description)
                task.deadline = validated_data.get('deadline', task.deadline)
                task.group = validated_data.get('group', task.group)
                task.is_completed = validated_data.get('is_completed', task.is_completed)

                # Atualizando campos Many-to-Many com o método .set()
                if 'responsible' in validated_data:
                    task.responsible.set(validated_data['responsible'])
                
                task.save()

                # Serializar e retornar a resposta
                response_serializer = TaskSerializer(task)
                return Response(response_serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def destroy(self, request, pk=None):
        try:
            TaskService.delete_task(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)
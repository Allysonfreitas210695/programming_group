from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from core.models.task_comment_model import TaskComment
from core.serializers.task_comment_serializer import CommentSerializer
from core.services.task_comment_service import CommentService
from core.shared.customAPIException import CustomAPIException
from rest_framework.response import Response
from rest_framework import status

class TaskCommentViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def list_comments_by_task(self, request, task_id=None):
        try:
            comments = CommentService.list_comments_by_task(task_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                task_id = validated_data['task'].id

                author = request.user
                validated_data.pop('author', None)

                comment = CommentService.add_comment_to_task(task_id, validated_data, author)
                
                response_serializer = CommentSerializer(comment)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({'detail': str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        try:
            CommentService.delete_comment(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def update(self, request, pk=None):
        try:
            comment = CommentService.get_comment_by_id(pk)
            serializer = CommentSerializer(comment, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)
        
    def list(self, request):
        try:
            comments = TaskComment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=500)
        
    def retrieve(self, request, pk=None):
        try:
            comment = CommentService.get_comment_by_id(pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)


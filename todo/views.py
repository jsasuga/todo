from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'is_complete', 'parent', 'children']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # todo = Todo.objects.get(*args, **kwargs)
        serializer = TodoSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def branch_status(self, request, *args, **kwargs):
        instance = self.get_object()
        tree_status = instance.tree_status()
        serializer = self.get_serializer(instance)

        return Response(
            {"branch_completed": tree_status},
            status=status.HTTP_200_OK
        )

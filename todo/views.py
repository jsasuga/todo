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

    @action(detail=True, methods=['get'])
    def branch_status(self, request, *args, **kwargs):
        instance = self.get_object()
        tree_status = instance.tree_status()
        return Response(
            {"branch_completed": tree_status},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'])
    def update_status(self, request, *args, **kwargs):
        instance = self.get_object()
        children_ids = instance.get_children_ids()
        Todo.objects.filter(pk__in=children_ids).update(is_complete=not instance.is_complete)
        instance.is_complete = not instance.is_complete
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_parent_status(self, request, *args, **kwargs):
        instance = self.get_object()
        parent_ids = instance.get_parent_ids()
        if "is_complete" not in request.data:
            return Response(
                {"message": "is_complete field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Todo.objects.filter(pk__in=parent_ids).update(is_complete=request.data["is_complete"])
        instance.is_complete = request.data["is_complete"]
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from .import enums
from config.paginators import CustomPagination
from .models import Task
from .serializers import (
    TaskSerializer,
    TaskStatusSerializer
)


User = get_user_model()


class Checkpoint(APIView):

    def get(self, request, format=None):
        response_data = {
            'message': "This is a test message"
        }
        return Response(response_data, status=status.HTTP_200_OK)


class TaskListCreate(generics.GenericAPIView):
    '''
    View to list all tasks if method is GET,
    or create a task if method is POST.

    * Requires token authentication.
    '''
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    # serializer_class = TaskSerializer
    # queryset = Task.objects.all()

    def get(self, request, format=None):
        '''
        Returns paginated list of all tasks.
        '''
        tasks = Task.objects.all()

        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = TaskSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


    def post(self, request):
        '''
        Create a task.
        '''
        task_serializer = TaskSerializer(data=request.data)

        if task_serializer.is_valid():
            task = Task(**task_serializer.validated_data)
            task.reporter = request.user
            task.save()

            return Response(
                TaskSerializer(task).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            task_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TaskDetail(APIView):
    '''
    Get, update or delete a task.

    * Requires token authentication.
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        '''
        Get task detail.
        '''
        task = get_object_or_404(Task, pk=pk)
        task_serializer = TaskSerializer(task)

        return Response(task_serializer.data)

    def put(self, request, pk):
        '''
        Update a task's
        name, description.
        '''
        task = get_object_or_404(Task, pk=pk)
        task_serializer = TaskSerializer(
            instance=task,
            data=request.data,
            partial=True
        )

        return Response(
            task_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        '''
        Delete task.
        '''
        task = get_object_or_404(Task, pk=pk)
        task.delete()

        return Response(
            {'id': '{}'.format(pk)},
            status=status.HTTP_200_OK
        )


class TaskAssign(APIView):
    '''
    Assign a task to a User.

    * Requires token authentication.
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user = request.data.get('user')

        # Check if user is an empty string.
        try:
            user = get_object_or_404(User, pk=user)
        except ValueError:
            user = None

        # Check if user same as existing assignee.
        if task.assignee == user:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            task.assignee = user
            task.save()

            return Response(
                TaskSerializer(task).data
            )

class TaskReview(APIView):
    '''
    Assign a task to review.

    * Requires token authentication.
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user = request.data.get('user')

        # Check if user is an empty string.
        try:
            user = get_object_or_404(User, pk=user)
        except ValueError:
            user = None

        # Check if user same as existing rewiew.
        if task.review == user:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            task.review = user
            task.save()

            return Response(
                TaskSerializer(task).data
            )

class TaskChangeStatus(APIView):
    '''
    Change the status of a Task.

    * Requires token authentication.
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task_serializer = TaskStatusSerializer(
            task,
            data=request.data,
            partial=True
        )

        if task_serializer.is_valid():

            # Check if new status same as existing status.
            if task_serializer.validated_data.get('status') == task.status:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                task = task_serializer.save()

                return Response(TaskSerializer(task).data)

        return Response(
            task_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TasksViewSetName(APIView):
    '''
    Filtering tasks by name
    '''
    permission_classes = (IsAuthenticated,)

    serializer_class = TaskSerializer

    def filter_queryset(self, queryset):

        task_name = self.request.query_params.get('name', None)

        if task_name:
            queryset = queryset.filter(task__name=task_name)

        return queryset

class TasksViewSetAssignee(APIView):
    '''
    Filtering tasks by user
    '''
    permission_classes = (IsAuthenticated,)

    user = request.data.get('user')
    model = self.serializer_class.Meta.model  # This is Task model
    queryset = model.objects.filter(task__assignee=user)
    # queryset = model.objects.all()

    return queryset

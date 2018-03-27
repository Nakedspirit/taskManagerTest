from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from tasks.models import Task
from tasks import enums

from .models import User
from .serializers import UserSerializer

class UserReports(APIView):
    '''
    Reporting task info for authenticated user.

    Counts tasks for each user that are
      - created
      - assigned
      - completed
      - incompleted

    * Requires token authentication.
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        # Get queryset of tasks that user has created or assigned to.
        tasks = Task.objects.all()

        # Count the created tasks for a user.
        created_count = tasks.filter(reporter=user).count()

        # Count the assigned, completed, incompleted tasks for a user.
        # Derived from queryset of assigned tasks.
        assigned_tasks = tasks.filter(assignee=user)
        assigned_count = assigned_tasks.count()
        completed_count = assigned_tasks.filter(
            status=enums.STATUS_DONE
        ).count()
        incompleted_count = assigned_tasks.filter(
            status__in=[enums.STATUS_TODO, enums.STATUS_IN_PROGRESS]
        ).count()

        # Create response object.
        response = {}
        response['created'] = created_count
        response['assigned'] = assigned_count
        response['completed'] = completed_count
        response['incompleted'] = incompleted_count

        return Response(response, status=status.HTTP_200_OK)

class UserCreate(generics.GenericAPIView):

    def create_user(request):
        serialized = UserSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    '''
    Get, update or delete a user.

    * Requires token authentication.
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        '''
        Get user detail.
        '''
        user = get_object_or_404(User, pk=pk)
        user_serializer = UserSerializer(task)

        return Response(user_serializer.data)

    def put(self, request, pk):
        '''
        Update a user's
        name, role.
        '''
        user = get_object_or_404(User, pk=pk)
        user_serializer = UserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )

        return Response(
            user_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        '''
        Delete user.
        '''
        user = get_object_or_404(User, pk=pk)
        user.delete()

        return Response(
            {'id': '{}'.format(pk)},
            status=status.HTTP_200_OK
        )

class UserViewSetRole(APIView):
    '''
    Filtering user by role
    '''
    permission_classes = (IsAuthenticated,)

    serializer_class = UserSerializer

    def filter_queryset(self, queryset):

        user_role = self.request.query_params.get('role', None)

        if user_role:
            queryset = queryset.filter(user__role=user_role)

        return queryset

class UserViewSetAssignee(APIView):
    '''
    Filtering users by assignee task
    '''
    permission_classes = (IsAuthenticated,)

    task = request.data.get('task')
    model = self.serializer_class.Meta.model  # This is User model
    queryset = model.objects.filter(user=task_assignee)
    # queryset = model.objects.all()

    return queryset


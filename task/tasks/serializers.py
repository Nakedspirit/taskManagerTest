from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id', 'name', 'description', 'status', 'reporter', 'assignee', 'review'
        )
        read_only_fields = ('id', 'status', 'reporter', 'assignee', 'review')


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('status',)


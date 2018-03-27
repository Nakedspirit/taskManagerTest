from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from .enums import (
    STATUS_CHOICES, STATUS_TODO
)


class Task(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)

    modified_on = models.DateTimeField(auto_now=True)

    name = models.CharField(
        max_length=300,
        verbose_name='Name',
        help_text='Task name'
    )

    description = models.TextField(
        max_length=2000,
        verbose_name='Description',
        help_text='Task description',
        blank=True
    )

    status = models.PositiveIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_TODO,
        verbose_name='Status',
        help_text='Task status'
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_tasks',
        on_delete=models.PROTECT,
        verbose_name='Reporter',
        help_text='User that created the task'
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tasks',
        on_delete=models.PROTECT,
        verbose_name='Assignee',
        help_text='User that is assigned to the task',
        blank=True,
        null=True
    )

    review = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='review_tasks',
        on_delete=models.PROTECT,
        verbose_name='Review',
        help_text='User that is review the task',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return '{}'.format(self.name[:20])

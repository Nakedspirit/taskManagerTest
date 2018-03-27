from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Task name', max_length=300, verbose_name='Name')),
                ('description', models.TextField(blank=True, help_text='Task description', max_length=2000, verbose_name='Description')),
                ('status', models.PositiveIntegerField(choices=[(1, b'Todo'), (2, b'In Progress'), (3, b'Done')], default=1, help_text='Task status', verbose_name='Status')),
                ('assignee', models.ForeignKey(blank=True, help_text='User that is assigned to the task', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Assignee')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='reporter',
            field=models.ForeignKey(help_text='User that created the task', on_delete=django.db.models.deletion.PROTECT, related_name='created_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Reporter'),
        ),
    ]

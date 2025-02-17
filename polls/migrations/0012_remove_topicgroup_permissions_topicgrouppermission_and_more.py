# Generated by Django 5.1.4 on 2025-02-08 23:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_permissionoptions_remove_topic_new_subjects_allowed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicgroup',
            name='permissions',
        ),
        migrations.CreateModel(
            name='TopicGroupPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.permissionoptions')),
                ('topic_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.topicgroup')),
            ],
            options={
                'unique_together': {('topic_group', 'permission')},
            },
        ),
        migrations.AddField(
            model_name='topicgroup',
            name='permissions',
            field=models.ManyToManyField(related_name='topic_groups', through='polls.TopicGroupPermission', to='polls.permissionoptions'),
        ),
    ]

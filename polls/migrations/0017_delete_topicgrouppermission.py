# Generated by Django 5.1.4 on 2025-02-09 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_remove_topicgroup_permission_sets_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TopicGroupPermission',
        ),
    ]

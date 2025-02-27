# Generated by Django 5.1.4 on 2025-02-09 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_topicgroup_can_add_users_to_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicgroup',
            name='permission_sets',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_add_users_to_group',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_create_group',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_create_subjects',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_delete_subjects',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_delete_topic',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_rename_topic',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_set_group_permissions',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_suggest_subjects',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_update_group',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_update_topic_subject_rules',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_update_topic_visible',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_update_topic_votable',
        ),
        migrations.RemoveField(
            model_name='permissionoptions',
            name='can_vote_on_subjects',
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_add_users_to_group',
            field=models.BooleanField(default=False, help_text='Can add users to groups.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_create_group',
            field=models.BooleanField(default=False, help_text='Can create groups for the topic.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_create_subjects',
            field=models.BooleanField(default=False, help_text='Can create subjects in the topic.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_delete_subjects',
            field=models.BooleanField(default=False, help_text='Can delete subjects in the topic.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_delete_topic',
            field=models.BooleanField(default=False, help_text='Can delete the topic.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_rename_topic',
            field=models.BooleanField(default=False, help_text='Can rename the topic.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_set_group_permissions',
            field=models.BooleanField(default=False, help_text='Can set permissions for groups.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_suggest_subjects',
            field=models.BooleanField(default=False, help_text='Can suggest subjects in the topic.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_update_group',
            field=models.BooleanField(default=False, help_text='Can update groups for the topic.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_update_topic_subject_rules',
            field=models.BooleanField(default=False, help_text='Can update the rules for subjects in the topic.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_update_topic_visible',
            field=models.BooleanField(default=False, help_text='Can update the topic visibility from public to private.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_update_topic_votable',
            field=models.BooleanField(default=False, help_text='Can update the topic to be votable.'),
        ),
        migrations.AlterField(
            model_name='topicgroup',
            name='can_vote_on_subjects',
            field=models.BooleanField(default=False, help_text='Can vote on subjects in the topic.'),
        ),
        migrations.DeleteModel(
            name='PermissionSet',
        ),
    ]

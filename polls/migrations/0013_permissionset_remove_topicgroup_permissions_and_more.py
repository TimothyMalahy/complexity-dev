# Generated by Django 5.1.4 on 2025-02-09 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_remove_topicgroup_permissions_topicgrouppermission_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('can_create_group', models.BooleanField(default=False)),
                ('can_update_group', models.BooleanField(default=False)),
                ('can_add_users_to_group', models.BooleanField(default=False)),
                ('can_set_group_permissions', models.BooleanField(default=False)),
                ('can_rename_topic', models.BooleanField(default=False)),
                ('can_delete_topic', models.BooleanField(default=False)),
                ('can_update_topic_visible', models.BooleanField(default=False)),
                ('can_update_topic_votable', models.BooleanField(default=False)),
                ('can_update_topic_subject_rules', models.BooleanField(default=False)),
                ('can_create_subjects', models.BooleanField(default=False)),
                ('can_suggest_subjects', models.BooleanField(default=False)),
                ('can_delete_subjects', models.BooleanField(default=False)),
                ('can_vote_on_subjects', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='topicgroup',
            name='permissions',
        ),
        migrations.AddField(
            model_name='topicgroup',
            name='permission_sets',
            field=models.ManyToManyField(to='polls.permissionset'),
        ),
    ]

# Generated by Django 5.1.4 on 2025-02-02 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_vote_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='date_voted',
            field=models.DateTimeField(blank=True, help_text="Date the vote was submitted - null if they didn't submit from last change", null=True),
        ),
    ]

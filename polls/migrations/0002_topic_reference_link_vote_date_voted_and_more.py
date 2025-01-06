# Generated by Django 5.1.4 on 2025-01-05 18:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='reference_link',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='date_voted',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='topic',
            constraint=models.UniqueConstraint(condition=models.Q(('topic_text__iexact', models.F('topic_text'))), fields=('topic_text',), name='unique_topic_text_lower'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import json_field.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_key', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
                ('session_data', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object')),
            ],
        ),
    ]

# Generated by Django 5.1.7 on 2025-03-11 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countdown', '0003_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='busy',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('code', models.TextField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='countdown.session')),
            ],
        ),
    ]

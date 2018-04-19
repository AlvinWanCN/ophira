# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sophiroth', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(default=0),
        ),
    ]

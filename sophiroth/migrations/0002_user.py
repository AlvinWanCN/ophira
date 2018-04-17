# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sophiroth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=32)),
                ('nickname', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, null=True)),
                ('brithday', models.DateField(null=True)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('role', models.IntegerField(default=0, max_length=3)),
            ],
        ),
    ]

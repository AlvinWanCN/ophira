# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('application', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=254)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('path', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=254)),
                ('uid', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=32)),
                ('nickname', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, null=True)),
                ('birthday', models.DateField(null=True)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('role', models.IntegerField(default=0)),
            ],
        ),
    ]

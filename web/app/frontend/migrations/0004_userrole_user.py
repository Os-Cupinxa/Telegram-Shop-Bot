# Generated by Django 5.1.1 on 2024-11-09 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_orderstatus_order_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.userrole')),
            ],
        ),
    ]

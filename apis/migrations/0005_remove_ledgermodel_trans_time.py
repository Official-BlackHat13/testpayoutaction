# Generated by Django 3.2 on 2021-06-13 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0004_auto_20210613_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ledgermodel',
            name='trans_time',
        ),
    ]
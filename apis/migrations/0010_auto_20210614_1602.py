# Generated by Django 3.2 on 2021-06-14 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0009_iphittingrecordmodel_ipwhitelistedmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ipwhitelistedmodel',
            old_name='client',
            new_name='client_model',
        ),
        migrations.RemoveField(
            model_name='ipwhitelistedmodel',
            name='client_code',
        ),
    ]

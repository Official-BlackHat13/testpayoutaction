# Generated by Django 3.2 on 2021-06-11 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.IntegerField()),
                ('client_code', models.CharField(max_length=60)),
                ('auth_key', models.CharField(max_length=60)),
                ('auth_iv', models.CharField(max_length=60)),
            ],
        ),
    ]

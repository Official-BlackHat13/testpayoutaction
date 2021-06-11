# Generated by Django 3.2 on 2021-06-11 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('bank_code', models.CharField(max_length=100)),
                ('nodal_account_number', models.CharField(max_length=300)),
                ('nodal_ifsc', models.CharField(max_length=300)),
                ('nodal_account_name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ClientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.IntegerField()),
                ('client_code', models.CharField(max_length=60)),
                ('auth_key', models.CharField(max_length=60)),
                ('auth_iv', models.CharField(max_length=60)),
                ('bank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LedgerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.IntegerField()),
                ('client_code', models.CharField(max_length=60)),
                ('amount', models.IntegerField()),
                ('trans_type', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=60)),
                ('bank_ref_no', models.CharField(max_length=1000)),
                ('customer_ref_no', models.CharField(max_length=1000)),
                ('bank', models.ImageField(upload_to='')),
                ('trans_time', models.DateTimeField()),
            ],
        ),
    ]

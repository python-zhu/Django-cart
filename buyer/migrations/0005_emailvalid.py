# Generated by Django 2.1.2 on 2019-08-28 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0004_order_ordergoods'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailValid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_name', models.CharField(max_length=32)),
                ('value', models.CharField(max_length=32)),
                ('time', models.DateTimeField()),
            ],
        ),
    ]

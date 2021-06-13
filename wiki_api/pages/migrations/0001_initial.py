# Generated by Django 3.2.4 on 2021-06-13 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.TextField(verbose_name='page_id')),
                ('page_name', models.TextField(verbose_name='page_name')),
                ('created_at', models.DateTimeField(verbose_name='created_at')),
                ('user_id', models.TextField(verbose_name='user_id')),
                ('domain_name', models.TextField(verbose_name='domain_name')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(unique=True, verbose_name='user_id')),
                ('user_name', models.TextField(unique=True, verbose_name='user_name')),
                ('user_is_bot', models.BooleanField(verbose_name='user_id_bot')),
            ],
        ),
    ]

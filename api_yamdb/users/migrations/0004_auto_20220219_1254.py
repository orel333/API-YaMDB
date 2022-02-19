# Generated by Django 2.2.16 on 2022-02-19 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220219_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('USER', 'Пользователь'), ('MODERATOR', 'Модератор'), ('ADMIN', 'Администратор')], default='USER', max_length=16, verbose_name='Роль'),
        ),
    ]

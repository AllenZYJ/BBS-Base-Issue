# Generated by Django 3.2.3 on 2021-05-24 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs_v01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='COMMENT_USER',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.CharField(max_length=20)),
                ('user_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='user_data',
            name='password',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='user_id',
            field=models.CharField(max_length=20),
        ),
    ]

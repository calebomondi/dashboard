# Generated by Django 5.0.6 on 2024-07-01 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsrCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usrname', models.CharField(max_length=100)),
                ('llat', models.CharField(max_length=500)),
                ('pgat', models.CharField(max_length=500)),
                ('iguserid', models.IntegerField()),
                ('fbpageid', models.IntegerField()),
                ('appid', models.IntegerField()),
                ('appsecret', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'meta_usrcredentials',
            },
        ),
    ]
